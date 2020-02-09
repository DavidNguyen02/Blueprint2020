from pymongo import MongoClient
from flask import Flask, render_template, request, session
from random import randint

app = Flask(__name__)

client = MongoClient('mongodb+srv://admin:<password>@cluster0-w1ulm.mongodb.net/test?retryWrites=true&w=majority')
db = client['hackathon']
playerScores = db['playerScores']

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html',
    messages=messages.find({}),
    loggedIn='username' in session,
    username=session.get('username','')
    )

@app.route('/login', methods=['POST'])
def login():
    session['username'] = request.form['username']
    return "success"

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return "success"

@app.route('game', methods=['POST'])
def game():
    comp = randint(1,3)
    player = request.form['selection']
    username = session['username']
    for item in playerScores:
        wins = item['wins']
        losses = item['losses']
    query = {'username': username, 'wins': wins, 'losses': losses}
    if comp == 3 and player == 1:
        update = {'username': username, 'wins': wins + 1, 'losses': losses }
    elif player == 3 and comp == 1:
        update = {'username': username, 'wins': wins, 'losses': losses + 1 }
    elif player > comp:
        update = {'username': username, 'wins': wins + 1, 'losses': losses }
    elif comp > player:
        update = {'username': username, 'wins': wins, 'losses': losses + 1 }
    else:
        update = {'username': username, 'wins': wins, 'losses': losses }
    playerScores.update_one(query, update)
    return "success"
    

app.run(port=3000, debug=True)