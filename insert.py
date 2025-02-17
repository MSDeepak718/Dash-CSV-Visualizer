import bcrypt
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["dash_auth"]
users_collection = db["users"]

password_hash = bcrypt.hashpw("123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

users_collection.insert_one({"username": "admin", "password": password_hash})

print("Admin user added!")
