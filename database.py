import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS, tlsCAFile=certifi.where(), tlsAllowInvalidCertificates=True)
database = client.news_database
article_collection = database.get_collection("articles")
user_collection = database.get_collection("users")
