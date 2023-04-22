from flask import Flask, jsonify, request, Response, render_template
from flask_socketio import SocketIO, emit
from functools import wraps
from db import *
import jwt
import bcrypt
from datetime import datetime, timedelta

db = init_db()
app = Flask(__name__,
            template_folder = "./dist",
            static_folder = "./dist/assets",)

app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app)

@app.route("/", defaults={"path": ""})
@app.route("/<string:path>")
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")


def check_password_hash(pw_hash, password):
    try:
        res =bcrypt.checkpw(password.encode('utf-8'), pw_hash.encode('utf-8'))
        return res
    except:
        return False


@socketio.on("login")
def login(msg):

    if not msg or not msg["username"] or not msg["password"]:
        emit("login answer", {"status": "error", "message": "missingCredentials"})

    user = get_user(db, msg["username"])

    if not user:
        emit("login answer", {"status": "error", "message": "noSuchUser"})
        return

    if check_password_hash(user["password"], msg["password"]):
        token = jwt.encode({'sub': user["username"], 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return emit("login answer", {'status':"success", 'token': token.decode('UTF-8')})

    return emit("login answer", {"status": "error", "message": "wrongPassword"})

@socketio.on("register")
def register(msg):
    if not msg or not msg["username"] or not msg["password"]:
        emit("register answer", {"status": "error", "message": "missingCredentials"})

    user = get_user(db, msg["username"])

    if user:
        emit("register answer", {"status": "error", "message": "userExists"})

    if not user:
        add_user(db, msg["username"], msg["password"])
        emit("register answer", {"status": "success", "message": "userCreated"})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port="4000", debug=True, allow_unsafe_werkzeug=True)

