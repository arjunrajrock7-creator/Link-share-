import motor.motor_asyncio
import logging
import asyncio
import time
from datetime import datetime, timedelta
from typing import List, Optional, Union, Dict
from config import MONGO_DB_URI, DB_NAME

logger = logging.getLogger(__name__)

class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self.cache: Dict[str, tuple] = {}

    def get(self, key: str):
        if key in self.cache:
            val, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return val
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value):
        self.cache[key] = (value, time.time())

class Database:
    def __init__(self, uri, name):
        # Optimized connection pooling for high concurrency
        self._client = motor.motor_asyncio.AsyncIOMotorClient(
            uri,
            maxPoolSize=100,
            minPoolSize=10,
            waitQueueTimeoutMS=5000
        )
        self.db = self._client[name]
        self.users = self.db.users
        self.channels = self.db.channels
        self.admins = self.db.admins
        self.links = self.db.links
        self.fsub = self.db.fsub
        self.external_links = self.db.external_links

        # In-memory TTL caches
        self.admin_cache = TTLCache(ttl_seconds=300) # 5 minutes
        self.link_cache = TTLCache(ttl_seconds=60)    # 1 minute

    async def initialize(self):
        """Initializes database indexes."""
        try:
            await self.users.create_index("_id")
            await self.channels.create_index("_id")
            await self.external_links.create_index("token", unique=True)
            await self.links.create_index("expiry_time")
            logger.info("Database indexes created successfully.")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")

    async def health_check(self) -> float:
        """Returns the DB latency in milliseconds."""
        start = time.time()
        await self.db.command("ping")
        return round((time.time() - start) * 1000, 2)

    # --- USER METHODS ---
    async def add_user(self, user_id: int, username: str = None):
        user = {
            "_id": user_id,
            "username": username,
            "join_date": datetime.utcnow()
        }
        try:
            await self.users.update_one({"_id": user_id}, {"$set": user}, upsert=True)
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")

    async def get_total_users(self):
        return await self.users.count_documents({})

    async def get_all_users(self):
        return self.users.find({})

    # --- ADMIN METHODS ---
    async def add_admin(self, user_id: int):
        await self.admins.update_one({"_id": user_id}, {"$set": {"_id": user_id}}, upsert=True)
        self.admin_cache.set(str(user_id), True)

    async def remove_admin(self, user_id: int):
        await self.admins.delete_one({"_id": user_id})
        self.admin_cache.set(str(user_id), False)

    async def is_admin(self, user_id: int):
        cache_val = self.admin_cache.get(str(user_id))
        if cache_val is not None:
            return cache_val

        admin = await self.admins.find_one({"_id": user_id})
        is_adm = bool(admin)
        self.admin_cache.set(str(user_id), is_adm)
        return is_adm

    async def get_all_admins(self) -> List[int]:
        admins = await self.admins.find({}).to_list(length=None)
        return [admin["_id"] for admin in admins]

    # --- CHANNEL METHODS ---
    async def add_channel(self, channel_id: int, title: str):
        await self.channels.update_one(
            {"_id": channel_id},
            {"$set": {"_id": channel_id, "title": title, "request_approval": False}},
            upsert=True
        )

    async def remove_channel(self, channel_id: int):
        await self.channels.delete_one({"_id": channel_id})

    async def get_channel(self, channel_id: int):
        return await self.channels.find_one({"_id": channel_id})

    async def get_all_channels(self):
        return await self.channels.find({}).to_list(length=None)

    async def set_request_approval(self, channel_id: int, status: bool):
        await self.channels.update_one({"_id": channel_id}, {"$set": {"request_approval": status}})

    # --- LINK TRACKING (AUTO-REVOKE) ---
    async def save_generated_link(self, channel_id: int, invite_link: str, message_id: int, chat_id: int, expiry_time: datetime):
        link_data = {
            "channel_id": channel_id,
            "invite_link": invite_link,
            "message_id": message_id,
            "chat_id": chat_id,
            "created_at": datetime.utcnow(),
            "expiry_time": expiry_time
        }
        await self.links.insert_one(link_data)

    async def get_expired_links(self):
        return await self.links.find({"expiry_time": {"$lt": datetime.utcnow()}}).to_list(length=None)

    async def remove_link(self, invite_link: str):
        await self.links.delete_one({"invite_link": invite_link})

    # --- EXTERNAL LINK ENCODING ---
    async def save_external_link(self, token: str, url: str):
        await self.external_links.update_one(
            {"token": token},
            {"$set": {"token": token, "url": url, "created_at": datetime.utcnow()}},
            upsert=True
        )
        self.link_cache.set(token, {"url": url})

    async def get_external_link(self, token: str):
        cache_val = self.link_cache.get(token)
        if cache_val:
            return cache_val

        link = await self.external_links.find_one({"token": token})
        if link:
            self.link_cache.set(token, link)
        return link

    # --- FSUB METHODS ---
    async def add_fsub(self, channel_id: int):
        await self.fsub.update_one({"_id": channel_id}, {"$set": {"_id": channel_id}}, upsert=True)

    async def remove_fsub(self, channel_id: int):
        await self.fsub.delete_one({"_id": channel_id})

    async def get_all_fsub(self):
        fsubs = await self.fsub.find({}).to_list(length=None)
        return [f["_id"] for f in fsubs]

# Global database instance
db = Database(MONGO_DB_URI, DB_NAME)
