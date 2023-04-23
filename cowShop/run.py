from flask import Flask, render_template
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
        return

    user = get_user(db, msg["username"])

    if not user:
        emit("login answer", {"status": "error", "message": "noSuchUser"})
        return

    if check_password_hash(user["password"], msg["password"]):
        token = jwt.encode({'sub': str(user["_id"]), 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return emit("login answer", {'status':"success", 'token': token.decode('UTF-8')})

    emit("login answer", {"status": "error", "message": "wrongPassword"})

@socketio.on("register")
def register(msg):
    if not msg or not msg["username"] or not msg["password"]:
        emit("register answer", {"status": "error", "message": "missingCredentials"})
        return

    user = get_user(db, msg["username"])

    if user:
        emit("register answer", {"status": "error", "message": "userExists"})
        return
    
    if not user:
        pw_bytes = msg["password"].encode('utf-8')
        salt = bcrypt.gensalt()
        pw_hash = bcrypt.hashpw(pw_bytes, salt).decode('utf-8')

        add_user(db, msg["username"], pw_hash, msg["is_admin"])
        user = get_user(db, msg["username"])

        token = jwt.encode({'sub': str(user["_id"]), 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        emit("register answer", {"status": "success", "token": token.decode('UTF-8')})

@socketio.on("add product")
def add_product(msg):
    if msg:
        add_one_product(db, msg)
        emit("add product answer", {"status": "success", "message": "productCreated"})

@socketio.on("get products")
def get_products():
    products = get_all_products(db)
    if products:
        emit("get products answer", products)
    else:
        emit("get products answer", {"status": "error", "message": "noProducts"})
    
@socketio.on("get product")
def get_product(msg):
    product = get_product_by_id(db, msg)
    if product:
        emit("get product answer", product)
    else:
        emit("get product answer", {"status": "error", "message": "noProduct"})

@socketio.on("get product review")
def product_review(msg):
    reviews = get_product_reviews(db, msg)
    if reviews:
        emit("get product review answer", reviews)
    
@socketio.on("get user")
def get_user_id(msg):
    user = get_user_by_id(db, msg)
    if user:
        emit("get user answer", user["username"])
    else:
        emit("get user answer", {"status": "error", "message": "noUser"})

@socketio.on("get users")
def get_users():
    users = get_all_users(db)
    if users:
        emit("get users answer", users)
    else:
        emit("get users answer", {})

@socketio.on("submit review")
def submit_review(msg):
    if not msg:
        emit("submit review answer", {"status": "error", "message": "missingCredentials"})
    else:
        add_review(db, msg["done_by"], msg)
        emit("submit review answer", {"status": "success", "message": "reviewAdded"})

@socketio.on("delete review")
def delete_review(msg):
    if not msg:
        emit("delete review answer", {"status": "error", "message": "missingCredentials"})
    else:
        delete_one_review(db, msg)
        emit("delete review answer", {"status": "success", "message": "reviewDeleted"})
    
@socketio.on("get product ratings")
def get_ratings(msg):
    ratings = get_product_ratings(db, msg)
    if ratings:
        emit("get product ratings answer", ratings)
    else:
        emit("get product ratings answer", {})

@socketio.on("submit rating")
def submit_rating(msg):
    if not msg:
        emit("submit rating answer", {"status": "error", "message": "missingCredentials"})
    else:
        add_rating(db, msg["done_by"], msg)
        emit("submit rating answer", {"status": "success", "message": "reviwAdded"})

@socketio.on("is admin")
def is_admin(msg):
    user = get_user_by_id(db, msg)
    if user:
        emit("is admin answer", user["is_admin"])
    else:
        emit("is admin answer", False)

@socketio.on("get user reviews")
def user_reviews(msg):
    reviews = get_review_by_user(db, msg)
    if reviews:
        emit("get user reviews answer", reviews)
    else:
        emit("get user reviews answer", {})

@socketio.on("get user ratings")
def user_ratings(msg):
    ratings = get_rating_by_user(db, msg)
    if ratings:
        emit("get user ratings answer", ratings)
    else:
        emit("get user ratings answer", {})
def run():
    socketio.run(app, host="0.0.0.0", port="4000", debug=True, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    run()

