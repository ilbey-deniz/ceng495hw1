from pymongo import MongoClient
from flask import jsonify
import json
from bson import ObjectId, json_util

uri = "mongodb+srv://ilbey:1@cluster0.ozk1wag.mongodb.net/?retryWrites=true&w=majority"
DB = "test"
USERS = "users"
PRODUCTS = "products"
REVIEWS = "reviews"

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
    
def parse_json(data):
    return json.loads(json_util.dumps(data))

# Create a new client and connect to the server
client = MongoClient(uri)

def init_db():
    db = client.get_database(DB)
    return db

def add_user(db, username, password):
    # Create a new user
    user = {
        "username": username,
        "password": password
    }
    # Insert the user into the database
    db[USERS].insert_one(user)

def get_user(db, username):
    # Get the user from the database
    user = db[USERS].find_one({"username": username})
    return user

def get_all_products(db):
    # Get all products from the database
    cursor = db[PRODUCTS].find({})
    return parse_json(cursor)

def get_all_users(db):
    # Get all users from the database
    cursor = db[USERS].find({})
    return parse_json(cursor)

def get_all_reviews(db):
    # Get all rewiews from the database
    cursor = db[REVIEWS].find({})
    return parse_json(cursor)

def get_product_by_id(db, id):
    # Get the product from the database
    cursor = db[PRODUCTS].find_one({"_id": ObjectId(id)})
    return parse_json(cursor)