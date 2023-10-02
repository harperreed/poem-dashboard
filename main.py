from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
import feedparser
import openai
import random
import requests
import string

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/app/database/database.db'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Add timestamp field

def fetch_json(url):
    # Send HTTP GET request
    response = requests.get(url)
    
    # Check for a valid response (HTTP Status Code 200)
    response.raise_for_status()
    
    # Parse JSON response
    data = response.json()
    
    return data

def get_random_headlines(url):
    # Parse the RSS feed
    feed = feedparser.parse(url)
    
    # Extract headlines
    headlines = [entry.title for entry in feed.entries]
    
    # Check if there are at least two headlines to choose from
    if len(headlines) < 2:
        raise ValueError("Not enough headlines in the feed.")
    
    # Randomly select two distinct headlines
    headline1, headline2 = random.sample(headlines, 2)
    
    return headline1, headline2

def get_prompt():
     # letters = string.ascii_lowercase
    # return ''.join(random.choice(letters) for i in range(length))
    headlines =  get_random_headlines('http://feeds.bbci.co.uk/news/world/rss.xml')  # Get random headlines from the Guardian
    weather_ai = fetch_json("https://dud.org/api/weather_ai.json")
    print(weather_ai)

    prompt = f"""
    Headlines: 
      - {headlines[0]}
      - {headlines[1]}
    Weather info: 
      - Current Temp: {weather_ai['weatherData']['currentRealtime']['values']['temperature']}
      - Today's Low Temp: {weather_ai['Temperatures']['LowTemp']}
      - Today's High Temp: {weather_ai['Temperatures']['HighTemp']}
      - {weather_ai['CurrentMetrics'][0]['Name']}: {weather_ai['CurrentMetrics'][0]['Value']} {weather_ai['CurrentMetrics'][0]['Unit']}
      - {weather_ai['CurrentMetrics'][1]['Name']}: {weather_ai['CurrentMetrics'][1]['Value']} {weather_ai['CurrentMetrics'][1]['Unit']}
      - {weather_ai['CurrentMetrics'][2]['Name']}: {weather_ai['CurrentMetrics'][2]['Value']} {weather_ai['CurrentMetrics'][2]['Unit']}

    """

    return prompt

def generate_poem(length=20):
  
  system_prompt = """
  You are an amazing poet. 
  You are writing a poem that will be displayed on an office wall. 
  your job is to use all the info that the human gives you in a beautiful poem. 
  You sometimes are profane, and rude
  Keep the poem short, and sweet. Under 5 lines.
  """
  prompt = get_prompt()

  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": prompt}
    ]
  )

  return (completion.choices[0].message['content'])

def generate_and_store_message():
    with app.app_context():
      latest_message = Message.query.order_by(Message.id.desc()).first()
      if latest_message and (datetime.utcnow() - latest_message.timestamp) < timedelta(minutes=2):
          # If a message was generated within the last hour, do nothing
          message = Message.query.order_by(Message.id.desc()).first()  # Get the latest message
          socketio.emit('message_update', {'message': message.content})

          return message.content
      
      # Otherwise, generate and store a new message
      message_content = generate_poem()
      message = Message(content=message_content)
      db.session.add(message)
      db.session.commit()
      socketio.emit('message_update', {'message': message_content})

@app.route('/message')
def message():
    message = generate_and_store_message()
    print(message)
    return message


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create the tables defined in your models
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_and_store_message, 'interval', minutes=1)  # Set interval here
    scheduler.start()
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
