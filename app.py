from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
from html import escape
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    try:
        username = escape(data.get('username', 'Anonymous'))
        emit('chat history', chat_history)
        join_msg = {'user': 'Server', 'msg': f'{username} has joined the chat', 'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
        chat_history.append(join_msg)
        emit('message', join_msg, broadcast=True)
    except Exception as e:
        emit('error', {'msg': f'Join error: {str(e)}'})

@socketio.on('message')
def handle_message(data):
    try:
        user = escape(data.get('user', 'Anonymous'))
        msg = escape(data.get('msg', ''))
        if msg.strip():
            chat_entry = {'user': user, 'msg': msg, 'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
            chat_history.append(chat_entry)
            emit('message', chat_entry, broadcast=True)
    except Exception as e:
        emit('error', {'msg': f'Message error: {str(e)}'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))