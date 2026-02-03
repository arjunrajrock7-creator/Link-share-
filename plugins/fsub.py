from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from database.database import db
from config import *
from functools import wraps

async def is_subscribed(bot: Client, user_id: int):
    if not FSUB_ENABLED:
        return True

    if user_id == OWNER_ID:
        return True

    fsub_channels = await db.get_all_fsub()
    if not fsub_channels:
        return True

    for ch_id in fsub_channels:
        try:
            member = await bot.get_chat_member(ch_id, user_id)
            if member.status in ["kicked", "left"]:
                return False
        except UserNotParticipant:
            return False
        except Exception as e:
            print(f"Error checking FSub for {ch_id}: {e}")
            continue
    return True

def force_sub(func):
    @wraps(func)
    async def wrapper(bot: Client, message: Message, *args, **kwargs):
        if not FSUB_ENABLED:
            return await func(bot, message, *args, **kwargs)

        user_id = message.from_user.id
        if not await is_subscribed(bot, user_id):
            fsub_channels = await db.get_all_fsub()
            buttons = []
            for cid in fsub_channels:
                try:
                    chat = await bot.get_chat(cid)
                    invite = await bot.export_chat_invite_link(cid)
                    buttons.append([InlineKeyboardButton(f"ᴊᴏɪɴ {chat.title}", url=invite)])
                except:
                    buttons.append([InlineKeyboardButton(f"ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/c/{str(cid)[4:]}")])

            # Add a Refresh button
            buttons.append([InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="start_back")])

            caption = (
                f"{T_BANNER}\n"
                f"{T_DIVIDER}\n"
                f"{E_FSUB} **ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ!**\n\n"
                f"ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʙᴇғᴏʀᴇ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.\n"
                f"{T_DIVIDER}"
            )
            return await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(buttons))
        return await func(bot, message, *args, **kwargs)
    return wrapper

@Client.on_message(filters.command("fsub_add") & filters.private)
async def fsub_add_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/fsub_add -100xxxxxxxxxx`")

    try:
        channel_id = int(message.command[1])
        await db.add_fsub(channel_id)
        await message.reply_text(f"{E_SUCCESS} **ғsᴜʙ ᴄʜᴀɴɴᴇʟ ᴀᴅᴅᴇᴅ!**")
    except Exception as e:
        await message.reply_text(f"{E_ERROR} **ᴇʀʀᴏʀ:** `{str(e)}`")

@Client.on_message(filters.command("fsub_remove") & filters.private)
async def fsub_remove_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/fsub_remove -100xxxxxxxxxx`")

    try:
        channel_id = int(message.command[1])
        await db.remove_fsub(channel_id)
        await message.reply_text(f"{E_SUCCESS} **ғsᴜʙ ᴄʜᴀɴɴᴇʟ ʀᴇᴍᴏᴠᴇᴅ!**")
    except Exception as e:
        await message.reply_text(f"{E_ERROR} **ᴇʀʀᴏʀ:** `{str(e)}`")
