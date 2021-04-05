import os
from flask import Flask, send_from_directory, json, request
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # This is to load your env variables from .env

app = Flask(__name__, static_folder='./build/static')
# Point SQLAlchemy to your Heroku database

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 0) or 0
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# IMPORTANT: This must be AFTER creating db variable to prevent
# circular import issues
import models
db.create_all()

cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app,
                    cors_allowed_origins="*",
                    json=json,
                    manage_session=False)


@app.route('/', defaults={"filename": "index.html"})
@app.route('/<path:filename>')
def index(filename):
    return send_from_directory('./build', filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        add_user(username)
        all_users = get_all_users()
        return {
            'users': all_users
        }
    else:
        all_users = get_all_users()
        return {
            'users': all_users
        }

# When a client connects from this Socket connection, this function is run
@socketio.on('connect')
def on_connect():
    print('User connected!')
    all_users = get_all_users()
    socketio.emit('user_list', {'users': all_users})


# When a client disconnects from this Socket connection, this function is run
@socketio.on('disconnect')
def on_disconnect():
    print('User disconnected!')


# When a client emits the event 'chat' to the server, this function is run
# 'chat' is a custom event name that we just decided
@socketio.on('chat')
def on_chat(data):  # data is whatever arg you pass in your emit call on client
    print(str(data))
    # This emits the 'chat' event from the server to all clients except for
    # the client that emmitted the event that triggered this function
    socketio.emit('chat', data, broadcast=True, include_self=False)


@socketio.on('join')
def on_join(data):  # data is whatever arg you pass in your emit call on client
    print(str(data))
    add_user(data['user'])
    all_users = get_all_users()
    socketio.emit('user_list', {'users': all_users})


def add_user(username):
    new_user = models.Person(username=username,
                             email='{0}@stuff.com'.format(username))
    db.session.add(new_user)
    db.session.commit()

def get_all_users():
    all_people = models.Person.query.all()
    users = []
    for person in all_people:
        users.append(person.username)
    return users


# Note we need to add this line so we can import app in the python shell
if __name__ == "__main__":
    # Note that we don't call app.run anymore. We call socketio.run with app arg
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )
