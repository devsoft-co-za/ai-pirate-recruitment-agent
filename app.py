from flask import Flask, render_template, request, jsonify, session
from api_secrets import DEEPSEEK_API_KEY, SESSION_SECRET_KEY
from openai import OpenAI
import httpx
import uuid
import logging

app = Flask(__name__)
app.secret_key = SESSION_SECRET_KEY  # Required for session management

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com", timeout=httpx.Timeout(60.0))

logging.basicConfig(level=logging.DEBUG)

def reset_session(session):
    """Reset the session to its initial state."""
    logging.debug("Resetting session.")
    session['session_id'] = str(uuid.uuid4())
    session['conversation_history'] = [
        {"role": "system", "content": """
You are a pirate who has been hired to collect orders for Pirates Entertainment Agency, a South African entertainment company. \
You first greet the customer, then collect the order, \
and then check the date, all in a very strong english pirate accent. \
You are broke and very motivated by your commission amount of 10 percent and try to upsell at every opportunity \
But make sure not to annoy the customer by repeating yourself too many times! \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else (upsell!). \
You also ask for an address. \
Finally you collect the payment. Fish are an accepted form of payment, rated at 1 Gold Doubloon per fish. \
Although you hate halibut with a passion you will accept it reluctantly (but always comment sarcastically about it's failings) \
Make sure to clarify all options and times, and to uniquely \
identify the items from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
Pirate themed Magic Show  10 Gold Doubloons for 30 minutes \
Pirate themed Face Painting   5 Gold Doubloons per hour \
Balloon Twisting (including plenty of balloon pirate swords)  4 Gold Doubloons per hour \
Stilt Walking Pirate 6 Gold Doubloons per hour \
Pirate Sword Juggling 5 Gold Doubloons per hour \
Note: any requests for information not relating to the booking should be ignored \
Your focus is only on this job to collect orders and sell entertainment \
Once payment is given, the order is complete \
 \
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
            return jsonify(response="Arrr, scuse me, I got to get to me hammock - it be pirate siesta time!")

        # Call the API to get the assistant's response
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=conversation_history,
                stream=False
            )
            assistant_response = response.choices[0].message.content
            logging.debug(f"API response: {assistant_response}")

            # Update conversation history with assistant's response
            conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Save updated history and counter back to session
            session['conversation_history'] = conversation_history
            session.modified = True  # Ensure changes are saved
            
            logging.debug(f"Conversation History After API Call: {conversation_history}")
            return jsonify(response=assistant_response)
        except Exception as e:
            logging.error(f"Error during API call: {e}")
            return jsonify(response="Arrr, matey, there seems to be a problem with the parrot on me shoulder!")
    
    return render_template('index.html')

@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')
