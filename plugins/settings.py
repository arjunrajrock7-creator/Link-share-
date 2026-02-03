import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db
from config import *

@Client.on_message(filters.command("requeston") & filters.private)
async def requeston_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and not await db.is_admin(user_id):
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/requeston -100xxxxxxxxxx`")

    try:
        channel_id = int(message.command[1])
        await db.set_request_approval(channel_id, True)
        await message.reply_text(f"{E_SUCCESS} **ᴀᴜᴛᴏ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴀʟ ᴇɴᴀʙʟᴇᴅ!**")
    except Exception as e:
        await message.reply_text(f"{E_ERROR} **ᴇʀʀᴏʀ:** `{str(e)}`")

@Client.on_message(filters.command("requestoff") & filters.private)
async def requestoff_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and not await db.is_admin(user_id):
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/requestoff -100xxxxxxxxxx`")

    try:
        channel_id = int(message.command[1])
        await db.set_request_approval(channel_id, False)
        await message.reply_text(f"{E_SUCCESS} **ᴀᴜᴛᴏ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴀʟ ᴅɪsᴀʙʟᴇᴅ!**")
    except Exception as e:
        await message.reply_text(f"{E_ERROR} **ᴇʀʀᴏʀ:** `{str(e)}`")

# Revocation background logic (to be called from bot.py or as a task)
async def auto_revoke_task(bot: Client):
    while True:
        try:
            expired_links = await db.get_expired_links()
            for link in expired_links:
                try:
                    # Revoke link
                    await bot.revoke_chat_invite_link(link['channel_id'], link['invite_link'])

                    # Edit message to "Expired"
                    caption = (
                        f"{T_BANNER}\n"
                        f"{T_DIVIDER}\n"
                        f"{E_REVOKE} **ᴛʜɪs ʟɪɴᴋ ʜᴀs ᴇxᴘɪʀᴇᴅ!**\n"
                        f"ᴘʟᴇᴀsᴇ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ɴᴇᴡ ᴏɴᴇ.\n"
                        f"{T_DIVIDER}"
                    )
                    try:
                        await bot.edit_message_text(
                            chat_id=link['chat_id'],
                            message_id=link['message_id'],
                            text=caption
                        )
                    except:
                        pass # Message might be deleted

                    # Remove from DB
                    await db.remove_link(link['invite_link'])
                except Exception as e:
                    print(f"Error revoking link {link['invite_link']}: {e}")
        except Exception as e:
            print(f"Error in auto_revoke_task: {e}")

        await asyncio.sleep(60) # Check every minute
