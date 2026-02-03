import asyncio
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from database.database import db
from utils.pagination import get_pagination

CHANNELS_PER_PAGE = 10

async def auto_revoke_task(bot: Client):
    """Background task to revoke expired links every minute."""
    while True:
        try:
            expired_links = await db.get_expired_links()
            for link in expired_links:
                try:
                    await bot.revoke_chat_invite_link(link['channel_id'], link['invite_link'])
                    try:
                        await bot.edit_message_text(
                            chat_id=link['chat_id'],
                            message_id=link['message_id'],
                            text=f"🎋 {T_BANNER}\n{T_DIVIDER}\n{E_REVOKE} **ᴛʜɪs ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ᴇxᴘɪʀᴇᴅ!**\n{T_DIVIDER}\n{SUPPORT_LINE}"
                        )
                    except:
                        pass
                    await db.remove_link(link['invite_link'])
                except Exception as e:
                    logging.error(f"Error revoking link {link['invite_link']}: {e}")
                    await db.remove_link(link['invite_link'])
        except Exception as e:
            logging.error(f"Error in auto_revoke_task: {e}")
        await asyncio.sleep(60)

@Client.on_message(filters.command("channels") & filters.private)
async def channels_cmd(bot: Client, message: Message):
    await show_channels(bot, message, page=1)

@Client.on_callback_query(filters.regex(r"^channels_list_(\d+)$"))
async def channels_list_callback(bot: Client, query: CallbackQuery):
    await query.answer()
    page = int(query.data.split("_")[2])
    await show_channels(bot, query, page=page)

@Client.on_callback_query(filters.regex("^channels_list$"))
async def channels_list_base_callback(bot: Client, query: CallbackQuery):
    await query.answer()
    await show_channels(bot, query, page=1)

async def show_channels(bot, message_or_query, page):
    channels = await db.get_all_channels()
    if not channels:
        text = f"{E_ERROR} **ɴᴏ ᴄʜᴀɴɴᴇʟs ᴀᴅᴅᴇᴅ ʏᴇᴛ!**"
        if isinstance(message_or_query, Message):
            return await message_or_query.reply_text(text)
        else:
            return await message_or_query.answer("ɴᴏ ᴄʜᴀɴɴᴇʟs!", show_alert=True)

    total_pages = (len(channels) + CHANNELS_PER_PAGE - 1) // CHANNELS_PER_PAGE
    start = (page - 1) * CHANNELS_PER_PAGE
    end = start + CHANNELS_PER_PAGE

    text = f"📡 **𝗬𝗼𝘂𝗿 𝗖𝗼𝗻𝗻𝗲𝗰𝘁𝗲𝗱 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀 (𝗣𝗮𝗴𝗲 {page}/{total_pages}):**\n\n"
    for i, ch in enumerate(channels[start:end], start + 1):
        status = "REQ" if ch.get('request_approval') else "NORM"
        text += f"{i}. `{ch['_id']}` - **{ch['title']}** [{status}]\n"

    buttons = get_pagination(page, total_pages, "channels_list")
    buttons.append([InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start_back")])

    if isinstance(message_or_query, Message):
        await message_or_query.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message_or_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
