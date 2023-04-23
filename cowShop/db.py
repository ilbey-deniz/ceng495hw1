from pymongo import MongoClient, ReturnDocument
from flask import jsonify
import json
from bson import ObjectId, json_util

uri = "mongodb+srv://ilbey:1@cluster0.ozk1wag.mongodb.net/?retryWrites=true&w=majority"
DB = "test"
USERS = "users"
PRODUCTS = "products"
REVIEWS = "reviews"
RATINGS = "ratings"

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

def get_user_by_id(db, id):
    # Get the user from the database
    cursor = db[USERS].find_one({"_id": ObjectId(id)})
    return parse_json(cursor)

def get_product_reviews(db, id):
    # Get the product from the database
    cursor = db[REVIEWS].find({"product_id": ObjectId(id)})
    return parse_json(cursor)

def get_review_by_user(db, id):
    # Get the product from the database
    cursor = db[REVIEWS].find({"done_by": ObjectId(id)})
    return parse_json(cursor)

def get_rating_by_user(db, id):
    # Get the product from the database
    cursor = db[RATINGS].find({"done_by": ObjectId(id)})
    return parse_json(cursor)

def get_rating_by_user(db, id):
    # Get the product from the database
    cursor = db[RATINGS].find({"done_by": ObjectId(id)})
    return parse_json(cursor)

def add_review(db, user_id, review):
    username = get_user_by_id(db, user_id)["username"]
    # Create a new review
    review = {
        "product_id": ObjectId(review["product_id"]),
        "done_by": ObjectId(user_id),
        "text": review["text"],
        "done_by_username": username
    }
    # Insert the review into the database
    db[REVIEWS].update_one(
        {"$and":[{"done_by":review["done_by"]},{"product_id": review["product_id"]}]},
        {"$set":review},
        upsert=True)
    
def delete_one_review(db, review):
    print(review)
    # Delete the review from the database
    db[REVIEWS].delete_one(
        {"$and": [{"done_by": ObjectId(review["done_by"])}, 
                  {"product_id": ObjectId(review["product_id"]["$oid"])}
                  ]}
    )

def add_rating(db, user_id, rating):
    username = get_user_by_id(db, user_id)["username"]
    # Create a new review
    rating = {
        "product_id": ObjectId(rating["product_id"]),
        "done_by": ObjectId(user_id),
        "rating": rating["rating"],
        "done_by_username": username
    }
    # Insert the review into the database
    db[RATINGS].update_one(
        {"$and":[{"done_by":rating["done_by"]},{"product_id": rating["product_id"]}]},
        {"$set":rating},
        upsert=True)
    
def get_product_ratings(db, id):
    # Get the product from the database
    cursor = db[RATINGS].find({"product_id": ObjectId(id)})
    return parse_json(cursor)