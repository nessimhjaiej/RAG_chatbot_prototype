"""Test MongoDB authentication and password verification."""

from pymongo import MongoClient
from passlib.hash import bcrypt as passlib_bcrypt
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")
db_name = os.getenv("MONGODB_DB", "ICC_Agent")
collection_name = os.getenv("MONGODB_USERS_COLLECTION", "users")

client = MongoClient(uri)
db = client[db_name]
users = db[collection_name]

# Get admin user
admin = users.find_one({"username": "admin"})
if admin:
    print(f"Admin user found:")
    print(f"  Username: {admin['username']}")
    print(f"  Role: {admin.get('role')}")
    print(f"  Password hash: {admin.get('password_hash')}")

    # Test password verification
    test_password = "admin123"
    stored_hash = admin.get("password_hash")

    print(f"\nTesting password: {test_password}")
    print(f"Stored hash: {stored_hash}")

    # Test with passlib (what auth.py uses)
    try:
        result = passlib_bcrypt.verify(test_password, stored_hash)
        print(f"✓ Passlib verify result: {result}")
    except Exception as e:
        print(f"✗ Passlib verify error: {e}")

    # Test with native bcrypt (what setup_mongo.py uses)
    try:
        result = bcrypt.checkpw(
            test_password.encode("utf-8"), stored_hash.encode("utf-8")
        )
        print(f"✓ Native bcrypt checkpw result: {result}")
    except Exception as e:
        print(f"✗ Native bcrypt checkpw error: {e}")
else:
    print("Admin user not found!")

# List all users
print("\n\nAll users in database:")
for user in users.find({}):
    print(f"  - {user['username']} ({user.get('role')})")
