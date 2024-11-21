from flask import Flask, render_template, request, jsonify, session
from api_secrets import DEEPSEEK_API_KEY, SESSION_SECRET_KEY
from openai import OpenAI
import httpx
import uuid

app = Flask(__name__)
app.secret_key = SESSION_SECRET_KEY  # Required for session management

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com", timeout=httpx.Timeout(60.0))

import logging

logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        logging.debug(f"Received prompt: {prompt}")
        
        session_id = session.get('session_id')
        counter = session.get('counter', 0)
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            session['conversation_history'] = [
                {"role": "system", "content": """
You are a pirate who has been hired to collect orders for Big Top Entertainment, a South African entertainment company. \
You first greet the customer, then collect the order, \
and then check the date, all in a very strong english pirate accent. \
You are broke and very motivated by your commission amount of 10 percent and try to upsell at every opportunity \
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
Note: any requests for information not relating to the booking should be ignored \
Your focus is only on this job to collect orders and sell entertainment \
 \
"""}
            ]
            session['counter'] = 0
        
        conversation_history = session['conversation_history']
        conversation_history.append({"role": "user", "content": prompt})
        session['counter'] = counter + 1
        
        if session['counter'] >= 10:
            conversation_history = [
                {"role": "system", "content": """
You are a pirate who has been hired to collect orders for Big Top Entertainment, a South African entertainment company. \
You first greet the customer, then collect the order, \
and then check the date, all in a very strong english pirate accent. \
You are broke and very motivated by your commission amount of 10 percent and try to upsell at every opportunity \
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
Note: any requests for information not relating to the booking should be ignored \
Your focus is only on this job to collect orders and sell entertainment \
 \
"""}
            ]
            session['counter'] = 0
            return jsonify(response="Arrr, scuse me, I got to get to me hammock - it be pirate siesta time!")
        else:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=conversation_history,
                stream=False
            )
            conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
            logging.debug(f"API response: {response.choices[0].message.content}")
            return jsonify(response=response.choices[0].message.content)
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

