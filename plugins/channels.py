from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db
from config import *
import math

@Client.on_message(filters.command("addchannel") & filters.private)
async def add_channel_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and not await db.is_admin(user_id):
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/addchannel -100xxxxxxxxxx`")

    channel_id_str = message.command[1]
    try:
        channel_id = int(channel_id_str)
        chat = await bot.get_chat(channel_id)

        await db.add_channel(channel_id, chat.title)
        await message.reply_text(
            f"{E_SUCCESS} **ᴄʜᴀɴɴᴇʟ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
            f"**ɴᴀᴍᴇ:** {chat.title}\n"
            f"**ɪᴅ:** `{channel_id}`"
        )
    except Exception as e:
        await message.reply_text(f"{E_ERROR} **ᴇʀʀᴏʀ:** `{str(e)}`")

@Client.on_message(filters.command("removechannel") & filters.private)
async def remove_channel_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and not await db.is_admin(user_id):
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/removechannel -100xxxxxxxxxx`")

    try:
        channel_id = int(message.command[1])
        await db.remove_channel(channel_id)
        await message.reply_text(f"{E_SUCCESS} **ᴄʜᴀɴɴᴇʟ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**")
    except Exception as e:
        await message.reply_text(f"{E_ERROR} **ᴇʀʀᴏʀ:** `{str(e)}`")

@Client.on_message(filters.command("channels") & filters.private)
async def channels_list_handler(bot: Client, message: Message):
    await show_channels(bot, message, page=1)

@Client.on_callback_query(filters.regex(r"^channels_page_(\d+)$"))
async def channels_page_callback(bot: Client, query):
    page = int(query.data.split("_")[-1])
    await show_channels(bot, query.message, page=page, is_callback=True)

@Client.on_callback_query(filters.regex("^channels_list$"))
async def channels_list_callback(bot: Client, query):
    await show_channels(bot, query.message, page=1, is_callback=True)

async def show_channels(bot, message, page=1, is_callback=False):
    channels = await db.get_all_channels()
    if not channels:
        text = f"{E_ERROR} **ɴᴏ ᴄʜᴀɴɴᴇʟs ᴀᴅᴅᴇᴅ ʏᴇᴛ!**"
        if is_callback:
            return await message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start_back")]]))
        return await message.reply_text(text)

    per_page = 10
    total_pages = math.ceil(len(channels) / per_page)
    start = (page - 1) * per_page
    end = start + per_page

    text = f"{T_BANNER}\n{T_DIVIDER}\n**ʟɪsᴛ ᴏғ ᴄʜᴀɴɴᴇʟs (ᴘᴀɢᴇ {page}/{total_pages}):**\n\n"
    for ch in channels[start:end]:
        status = "ʀᴇǫᴜᴇsᴛ" if ch.get("request_approval") else "ɴᴏʀᴍᴀʟ"
        text += f"📡 **{ch['title']}**\nID: `{ch['_id']}`\nsᴛᴀᴛᴜs: {status}\n\n"

    text += T_DIVIDER

    buttons = []
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ ᴘʀᴇᴠ", callback_data=f"channels_page_{page-1}"))
    if page < total_pages:
        nav.append(InlineKeyboardButton("ɴᴇxᴛ ➡️", callback_data=f"channels_page_{page+1}"))

    if nav:
        buttons.append(nav)

    buttons.append([InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start_back")])

    if is_callback:
        await message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
