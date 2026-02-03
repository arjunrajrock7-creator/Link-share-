from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import UserNotParticipant
from config import *
from database.database import db
from functools import wraps
from typing import Union

async def get_fsub_buttons(bot: Client, user_id: int):
    fsub_channels = await db.get_all_fsub()
    if not fsub_channels:
        return None

    buttons = []
    not_joined = []

    for channel_id in fsub_channels:
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            if member.status in ["kicked", "left"]:
                not_joined.append(channel_id)
        except UserNotParticipant:
            not_joined.append(channel_id)
        except Exception:
            continue

    if not not_joined:
        return None

    for i, channel_id in enumerate(not_joined, 1):
        try:
            chat = await bot.get_chat(channel_id)
            link = chat.invite_link or (await bot.create_chat_invite_link(channel_id)).invite_link
            buttons.append([InlineKeyboardButton(f"📡 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ {i}", url=link)])
        except:
            continue

    if buttons:
        buttons.append([InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ", callback_data="check_fsub")])
        return InlineKeyboardMarkup(buttons)
    return None

def force_sub(fn):
    @wraps(fn)
    async def wrapper(bot: Client, message: Union[Message, CallbackQuery], *args, **kwargs):
        if not FSUB_ENABLED:
            return await fn(bot, message, *args, **kwargs)

        user_id = message.from_user.id
        # Owner and admins bypass FSub
        if user_id == OWNER_ID or await db.is_admin(user_id):
            return await fn(bot, message, *args, **kwargs)

        reply_markup = await get_fsub_buttons(bot, user_id)
        if reply_markup:
            text = (
                f"{T_BANNER}\n"
                f"{T_DIVIDER}\n"
                f"🎋 **ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ!**\n\n"
                f"ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ.\n"
                f"{T_DIVIDER}\n"
                f"{SUPPORT_LINE}"
            )
            if isinstance(message, Message):
                return await message.reply_text(text, reply_markup=reply_markup)
            else:
                return await message.message.edit_text(text, reply_markup=reply_markup)

        return await fn(bot, message, *args, **kwargs)
    return wrapper

@Client.on_callback_query(filters.regex("^check_fsub$"))
async def check_fsub_callback(bot: Client, query: CallbackQuery):
    user_id = query.from_user.id
    reply_markup = await get_fsub_buttons(bot, user_id)
    if reply_markup:
        await query.answer("❌ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟs!", show_alert=True)
    else:
        await query.answer("✅ ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴊᴏɪɴɪɴɢ!", show_alert=True)
        await query.message.delete()
        # After joining, user can send /start again or just continue.
        # We don't want to cause circular import.
