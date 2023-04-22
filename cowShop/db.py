from pymongo import MongoClient

uri = "mongodb+srv://ilbey:1@cluster0.ozk1wag.mongodb.net/?retryWrites=true&w=majority"
USERS = "users"
PRODUCTS = "products"
DB = "test"

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