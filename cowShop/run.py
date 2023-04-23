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
def get_user(msg):
    user = get_user_by_id(db, msg)
    if user:
        emit("get user answer", user["username"])
    else:
        emit("get user answer", {"status": "error", "message": "noUser"})

@socketio.on("submit review")
def submit_review(msg):
    if not msg:
        emit("submit review answer", {"status": "error", "message": "missingCredentials"})
    else:
        #TODO: user id from token
        if "done_by" in msg:
            add_review(db, msg["done_by"], msg)
        else:
            add_review(db, "6443d83576b3088c36a52d7e", msg)
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
        #TODO: user id from token
        add_rating(db, "6443d83576b3088c36a52d7e", msg)
        emit("submit rating answer", {"status": "success", "message": "reviwAdded"})

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

