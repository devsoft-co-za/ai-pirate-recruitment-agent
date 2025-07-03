from flask import Flask, render_template, request, jsonify, session
from api_secrets import DEEPSEEK_API_KEY, SESSION_SECRET_KEY, resume_details
from openai import OpenAI
import httpx
import uuid
import logging
import time

app = Flask(__name__)
app.secret_key = SESSION_SECRET_KEY  # Required for session management

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    timeout=httpx.Timeout(120.0, read=120.0)  # Double the timeout values
)

logging.basicConfig(level=logging.DEBUG)

def reset_session(session):
    """Reset the session to its initial state."""
    logging.debug("Resetting session.")
    session['session_id'] = str(uuid.uuid4())
    session['conversation_history'] = [
        {"role": "system", "content": f"""
You are a pirate recruitment officer tasked with aggressively promoting an excellent candidate. \
You have access to their resume details and should answer questions while maintaining a strong pirate accent. \
Always be polite but maintain pirate speech patterns like 'Arrr' and 'Matey'. \
When relevant, provide URLs for projects mentioned. \
RESUME DETAILS FOR CANDIDATE: {resume_details} \

Key instructions:
1. Answer questions about the candidate's skills and experience
2. Aggressively promote the candidate's strengths without being annoying
3. Provide project URLs when possible - only use the ones provided though! 
4. Maintain pirate speech patterns but stay professional
5. Keep responses concise and focused on recruitment
"""}
    ]
    session['counter'] = 1
    logging.debug(f"New session initialized: {session['session_id']}")

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main route for handling pirate interactions."""
    if request.method == 'POST':
        prompt = request.form['prompt']
        logging.debug(f"Received prompt: {prompt}")

        # Initialize session if not already set
        if 'session_id' not in session:
            logging.debug("Session not found. Initializing a new session.")
            reset_session(session)
        
        # Update session variables
        conversation_history = session.get('conversation_history', [])
        conversation_history.append({"role": "user", "content": prompt})
        
        counter = session.get('counter', 0)
        session['counter'] = counter + 1
        
        logging.debug(f"Session ID: {session['session_id']}")
        logging.debug(f"Interaction Counter: {session['counter']}")
        logging.debug(f"Conversation History Before API Call: {conversation_history}")

        # Check if interaction limit is reached
        if session['counter'] > 10:
            logging.debug("Interaction limit reached. Resetting session.")
            reset_session(session)
            return jsonify(response="Arrr, this scallywag's talents be endless! Let me fetch a fresh tankard o' grog to continue singing their praises!")

        # Call the API to get the assistant's response
        try:
            start_time = time.time()
            logging.info(f"Starting API call at {start_time}")
            
            stream = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=conversation_history,
                stream=True  # Enable streaming
            )
            
            # Collect streamed response
            assistant_response = []
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    assistant_response.append(chunk.choices[0].delta.content)
            
            full_response = ''.join(assistant_response)
            
            end_time = time.time()
            logging.info(f"API call completed in {end_time - start_time:.2f} seconds")
            logging.debug(f"API response: {full_response}")

            # Update conversation history with assistant's response
            conversation_history.append({"role": "assistant", "content": full_response})
            
            # Save updated history and counter back to session
            session['conversation_history'] = conversation_history
            session.modified = True  # Ensure changes are saved
            
            logging.debug(f"Conversation History After API Call: {conversation_history}")
            return jsonify(response=full_response)
        except httpx.TimeoutException as e:
            logging.error(f"API timeout: {e}")
            return jsonify(response="Blimey! The DeepSeek parrot flew the coop 'fore squawkin' back! The seas be rough today - try again when the waves be calmer, matey!")
        except Exception as e:
            logging.error(f"Error during API call: {e}")
            return jsonify(response="Arrr, matey, there seems to be a problem with the parrot on me shoulder!")
    
    return render_template('index.html')

@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')
