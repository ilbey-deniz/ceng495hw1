from flask import Flask, jsonify, request, Response, render_template
from flask_socketio import SocketIO, emit
from functools import wraps
import jwt
import bcrypt


app = Flask(__name__,
            template_folder = "./dist",
            static_folder = "./dist/assets",)

app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on('hello')
def test_connect():
    socketio.emit('hello response', {'data': 'Connected'})
    print('Client connected')

if __name__ == "__main__":
    
    socketio.run(app, host="0.0.0.0", port="4000", debug=True, allow_unsafe_werkzeug=True)

