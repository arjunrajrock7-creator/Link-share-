from pyrogram import Client, filters
from pyrogram.types import Message, ChatJoinRequest
from config import *
from database.database import db

@Client.on_message(filters.command(["requeston", "requestoff"]) & filters.private)
async def toggle_request(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID and not await db.is_admin(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(f"ᴜsᴀɢᴇ: `/{message.command[0]} -100xxxxxxxxxx`")

    channel_id = int(message.command[1])
    status = True if message.command[0] == "requeston" else False

    await db.set_request_approval(channel_id, status)
    await message.reply_text(f"{E_SUCCESS} **ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴀʟ set to {status} for {channel_id}**")

@Client.on_chat_join_request()
async def auto_approve(bot: Client, request: ChatJoinRequest):
    channel_id = request.chat.id
    ch = await db.get_channel(channel_id)

    if ch and ch.get('request_approval'):
        try:
            await bot.approve_chat_join_request(channel_id, request.from_user.id)
            logging.info(f"Approved {request.from_user.id} in {channel_id}")
        except Exception as e:
            logging.error(f"Failed to approve {request.from_user.id}: {e}")
