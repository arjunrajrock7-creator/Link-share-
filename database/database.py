import motor.motor_asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Union
from config import MONGO_DB_URI, DB_NAME

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, uri, name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[name]
        self.users = self.db.users
        self.channels = self.db.channels
        self.admins = self.db.admins
        self.links = self.db.links
        self.fsub = self.db.fsub
        self.external_links = self.db.external_links

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

    async def remove_admin(self, user_id: int):
        await self.admins.delete_one({"_id": user_id})

    async def is_admin(self, user_id: int):
        admin = await self.admins.find_one({"_id": user_id})
        return bool(admin)

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

    async def get_external_link(self, token: str):
        return await self.external_links.find_one({"token": token})

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
