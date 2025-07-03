from api_secrets import DEEPSEEK_API_KEY, resume_details

# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import httpx

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com", timeout=httpx.Timeout(60.0))

# Pirate recruitment chat:
conversation_history = [
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

is_first_prompt = True

while True:
    if is_first_prompt:
        prompt = input("Arrr! Ready to hear about our stellar candidate, matey? What ye be wantin' to know? ")
        is_first_prompt = False
    else:
        prompt = input("Ask another question, landlubber: ")

    if prompt.lower() == "exit":
        break

    # Add user message to history and get response
    conversation_history.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="deepseek-reasoner",  # Changed model to match app.py
        messages=conversation_history,
        stream=False
    )

    assistant_response = response.choices[0].message.content
    print(assistant_response)
    
    # Add assistant response to history
    conversation_history.append({"role": "assistant", "content": assistant_response})

    # Simple interaction counter (matches app.py's 10-interaction limit)
    if len(conversation_history) >= 20:  # 10 interactions (user + assistant pairs)
        print("Arrr, this scallywag's talents be endless! Let's start fresh...")
        conversation_history = [conversation_history[0]]  # Reset to system message

#example from another model: 
"""
is_first_prompt = True
prompt = ""

while True:
    if is_first_prompt:
        prompt = input("Ahoy there matey welcome to Big Top Entertainment, how can I help ye? ")
        is_first_prompt = False
    else:
        prompt = input("Enter text: ")

    if prompt.lower() == "exit":
        break

    response, context = collect_messages(prompt, context)

    if response.lower() == "exit":
        break
"""
