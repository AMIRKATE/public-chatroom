from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    emit('chat history', chat_history)
    join_msg = {'user': 'Server', 'msg': f'{username} has joined the chat'}
    chat_history.append(join_msg)
    emit('message', join_msg, broadcast=True)

@socketio.on('message')
def handle_message(data):
    chat_entry = {'user': data['user'], 'msg': data['msg']}
    chat_history.append(chat_entry)
    emit('message', chat_entry, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)