from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[settings.DATABASE_NAME]

# In-Memory Fail-Safe Storage for 100% High Availability
IN_MEMORY_USERS = {}
IN_MEMORY_JOURNALS = []
IN_MEMORY_EXPENSES = []
IN_MEMORY_ARCHIVES = []

def get_database():
    return db
