from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db
from config import *
import asyncio
import logging

logger = logging.getLogger(__name__)

@Client.on_chat_join_request()
async def auto_approve(bot: Client, request: ChatJoinRequest):
    chat_id = request.chat.id
    user_id = request.from_user.id

    # Check if auto-approve is enabled for this channel
    channel_data = await db.get_channel(chat_id)
    if channel_data and channel_data.get("request_approval"):
        try:
            await bot.approve_chat_join_request(chat_id, user_id)

            # Welcome message
            caption = (
                f"{T_BANNER}\n"
                f"{T_DIVIDER}\n"
                f"{E_SUCCESS} **ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴀʟ!**\n\n"
                f"ʜᴇʟʟᴏ {request.from_user.mention},\n"
                f"ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴛᴏ ᴊᴏɪɴ **{request.chat.title}**.\n"
                f"{T_DIVIDER}\n"
                f"{SUPPORT_LINE}"
            )

            try:
                await bot.send_message(user_id, caption)
            except Exception as e:
                logger.debug(f"Failed to send approval message to {user_id}: {e}")

        except Exception as e:
            logger.error(f"Error approving join request for user {user_id} in chat {chat_id}: {e}")
