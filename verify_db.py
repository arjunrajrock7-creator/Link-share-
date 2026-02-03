import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def verify():
    uri = os.environ.get("MONGO_DB_URI")
    if not uri:
        print("MONGO_DB_URI not set.")
        return

    try:
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("Database connection verified.")
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
