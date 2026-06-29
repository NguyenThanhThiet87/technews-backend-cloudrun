import os
import certifi
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import bcrypt

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_URL")

mock_users = [
    {
        "username": "admin",
        "password": get_password_hash("123456"),
        "role": "admin"
    },
    {
        "username": "editor",
        "password": get_password_hash("123456"),
        "role": "editor"
    }
]

async def seed_users():
    print("Connecting to MongoDB to seed users...")
    client = AsyncIOMotorClient(MONGO_DETAILS, tlsCAFile=certifi.where(), tlsAllowInvalidCertificates=True)
    db = client.news_database
    collection = db.get_collection("users")
    
    await collection.delete_many({})
    result = await collection.insert_many(mock_users)
    print(f"Successfully inserted {len(result.inserted_ids)} users!")

if __name__ == "__main__":
    asyncio.run(seed_users())
