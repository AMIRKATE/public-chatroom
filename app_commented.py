# Hey buddy! This is a chat app code, explained super simple
# for you. We’re making a website where people chat instantly,
# like texting on a webpage. I’ll break each line into shorter
# bits so it fits your screen, but keep every comment. You’ll
# be a pro at this code soon!

# Brings tools from Flask to make our website.
# Flask is a magic box for building websites easily.
# It handles showing pages and talking to visitors.
# - Flask: Makes the website work.
# - render_template: Shows HTML files (webpages).
# - request: Grabs info visitors type.
# Why? We need tools for the website and chat page.
# How? We borrow toys from Flask’s toybox.
from flask import Flask, render_template, request

# Grabs tools from flask_socketio for fast chatting.
# flask_socketio sends messages super quick, like
# passing notes instantly in class.
# - SocketIO: Main tool for fast chatting.
# - emit: Sends messages to website users.
# Why? For instant chat without waiting.
# How? Borrow tools from flask_socketio, Flask’s buddy.
from flask_socketio import SocketIO, emit

# Makes a new website app called “app”.
# Flask(__name__) says “start a new website”.
# __name__ helps Flask find files, like webpages.
# Why? “app” is the heart of our website.
# How? Flask sets up behind-the-scenes stuff.
app = Flask(__name__)

# Gives our website a secret password.
# app.config stores website settings.
# “SECRET_KEY” keeps things safe, like a diary lock.
# “secret!” is the password (not great for real apps).
# Why? Protects the website and chat.
# How? We put the key in settings, Flask locks it.
app.config['SECRET_KEY'] = 'secret!'

# Connects fast-chatting tool (SocketIO) to our app.
# SocketIO(app) plugs a walkie-talkie into the website.
# Why? Makes chat instant, messages pop up fast.
# How? SocketIO teams up with Flask for quick talk.
socketio = SocketIO(app)

# Makes an empty list for saving chat messages.
# chat_history is a notebook for all messages.
# Each message has who sent it and what they said.
# Why? Saves messages for new people to see.
# How? We make an empty list to add messages later.
chat_history = []

# Sets what happens when someone visits the main page.
# @app.route('/') says “if at front door, do this”.
# The “index” function runs for visitors.
# Why? Shows the chat webpage.
# How? Flask sees the main page and runs “index”.
@app.route('/')
def index():
    # Sends the chat webpage (index.html) to visitors.
    # render_template('index.html') hands over the chat design.
    # index.html is in a “templates” folder.
    # Why? People need the chat page to chat.
    # How? Flask finds index.html and sends it to browsers.
    return render_template('index.html')

# Sets up what happens when someone joins the chat.
# @socketio.on('join') listens for “I’m here!” signals.
# The “on_join” function runs when someone joins.
# Why? Welcomes new people, shows old messages.
# How? SocketIO hears “join” from browsers and runs this.
@socketio.on('join')
def on_join(data):
    # Grabs the person’s name from their info.
    # “data” is a package, like {'username': 'CoolMonkey'}.
    # username = data['username'] gets their name.
    # Why? To say “CoolMonkey joined!”.
    # How? Browser sends a package, we get the name.
    username = data['username']
    
    # Sends old chat messages to the new person.
    # emit('chat history', chat_history) gives our notebook.
    # “chat history” is what browsers listen for.
    # Why? New person sees past messages.
    # How? SocketIO sends chat_history to their browser.
    emit('chat history', chat_history)
    
    # Makes a message saying someone joined.
    # join_msg says “Server: CoolMonkey joined”.
    # We pretend “Server” is talking.
    # Why? Tells everyone a new friend joined.
    # How? Make a note with “Server” and their name.
    join_msg = {'user': 'Server', 'msg': f'{username} has joined the chat'}
    
    # Saves “someone joined” in our notebook.
    # chat_history.append(join_msg) adds the message.
    # Why? Future joiners see who joined before.
    # How? Stick the note in chat_history list.
    chat_history.append(join_msg)
    
    # Sends “joined” message to ALL in chat.
    # emit('message', join_msg, broadcast=True) shouts it.
    # “message” is what browsers show as new messages.
    # broadcast=True sends to everyone.
    # Why? Everyone sees “CoolMonkey joined!”.
    # How? SocketIO sends to all connected browsers.
    emit('message', join_msg, broadcast=True)

# Sets up what happens when someone sends a message.
# @socketio.on('message') listens for chat messages.
# The “handle_message” function runs for messages.
# Why? To save and share messages with all.
# How? SocketIO hears “message” and runs this.
@socketio.on('message')
def handle_message(data):
    # Makes a note of the sent message.
    # chat_entry has who sent it and what they said.
    # Like {'user': 'CoolMonkey', 'msg': 'Hi!'}.
    # Why? Formats message to share.
    # How? Takes browser info and makes a note.
    chat_entry = {'user': data['user'], 'msg': data['msg']}
    
    # Saves the message in our notebook.
    # chat_history.append(chat_entry) adds it.
    # Why? New joiners can see this message.
    # How? Stick the note in the list.
    chat_history.append(chat_entry)
    
    # Sends message to ALL in chat.
    # emit('message', chat_entry, broadcast=True) shouts it.
    # “message” is for browsers to show messages.
    # broadcast=True sends to everyone.
    # Why? Everyone sees “CoolMonkey: Hi!”.
    # How? SocketIO sends to all browsers.
    emit('message', chat_entry, broadcast=True)

# Checks if we’re running the code directly.
# __name__ is “__main__” if we run this file.
# Why? Only start website if running this file.
# How? Python checks __name__ to decide.
if __name__ == '__main__':
    # Starts the website for chatting.
    # socketio.run(app, host='0.0.0.0', port=10000) opens doors.
    # - app: Our website.
    # - host='0.0.0.0': Anyone can visit.
    # - port=10000: Website’s “address”.
    # Why? Makes website live for users.
    # How? SocketIO starts server for visitors and chat.
    socketio.run(app, host='0.0.0.0', port=10000)