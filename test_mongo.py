import os
import certifi
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_URL")

async def test_conn():
    print("Testing connection to MongoDB...")
    try:
        # Thử kết nối với các tham số SSL mạnh nhất
        client = AsyncIOMotorClient(
            MONGO_DETAILS, 
            tls=True, 
            tlsCAFile=certifi.where(), 
            tlsAllowInvalidCertificates=True, 
            serverSelectionTimeoutMS=5000
        )
        await client.admin.command('ping')
        print("Connected successfully!")
    except Exception as e:
        print("Error:", type(e).__name__, e)

asyncio.run(test_conn())
