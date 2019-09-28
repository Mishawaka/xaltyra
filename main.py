import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse, Media
from decouple import config
from flask import Flask, request, session
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world!'

@app.route('/sms', methods=['GET', 'POST'])
def reply():
    answer(request, session)
    return 'Идет обработка данных...'

def answer(request, session):
    client = Client(config('ACCOUNT_SID'), config('AUTH_TOKEN'))
    
    user = request.values.get('From')
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users").fetchall()

    if user == config('ADMIN'):
        return 0
    else:
        isset = any(i[1] == user for i in users)
        if isset:
            client.messages.create(from_='whatsapp:+14155238886', to=user, body='HIIII MAAARK!')
        else:
            cur.execute("INSERT INTO users (number, status) VALUES (?, ?)", (user, 'name'))
            conn.commit()
            client.messages.create(from_='whatsapp:+14155238886', to=user, body='Hello! What\'s your name?')
    # reader = list(csv.reader(open('list.csv', 'r'), delimiter=','))


    
    # if request.values.get('From') == config('ADMIN'):
    #     if request.values.get('MediaUrl0'):
    #         return 'Media message', request.values.get('MediaUrl0')
    #     return 'You are admin', None
    # else:
    #     return 'You are plain user!', None


if __name__ == "__main__":
    app.run(debug=True)