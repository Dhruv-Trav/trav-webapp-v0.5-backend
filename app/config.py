from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://dhruvvpatel1010_db_user:0it1bmPzVjjrBDVp@travtesting.sg6nbfu.mongodb.net/?retryWrites=true&w=majority&appName=travtesting")
DB_NAME = os.getenv("DB_NAME", "travtesting")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
