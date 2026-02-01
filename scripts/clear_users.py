"""Delete all users from MongoDB collection."""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv("MONGODB_URI")
db_name = os.getenv("MONGODB_DB", "ICC_Agent")
collection_name = os.getenv("MONGODB_USERS_COLLECTION", "users")

client = MongoClient(uri)
db = client[db_name]
users = db[collection_name]

# Delete all existing users
result = users.delete_many({})
print(f"Deleted {result.deleted_count} existing users from {db_name}.{collection_name}")
