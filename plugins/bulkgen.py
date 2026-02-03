from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db
from config import *
import math
from datetime import datetime, timedelta

# In-memory storage for selections: {user_id: {channel_id: selected_bool}}
user_selections = {}

@Client.on_message(filters.command("bulkgen") & filters.private)
async def bulkgen_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and not await db.is_admin(user_id):
        return

    user_selections[user_id] = {}
    await show_bulk_page(bot, message, user_id, page=1)

@Client.on_callback_query(filters.regex(r"^bulk_page_(\d+)$"))
async def bulk_page_callback(bot: Client, query):
    user_id = query.from_user.id
    page = int(query.data.split("_")[-1])
    await show_bulk_page(bot, query.message, user_id, page=page, is_callback=True)

@Client.on_callback_query(filters.regex(r"^bulk_toggle_(-?\d+)_(\d+)$"))
async def bulk_toggle_callback(bot: Client, query):
    user_id = query.from_user.id
    data = query.data.split("_")
    channel_id = int(data[2])
    page = int(data[3])

    if user_id not in user_selections:
        user_selections[user_id] = {}

    current = user_selections[user_id].get(channel_id, False)
    user_selections[user_id][channel_id] = not current

    await show_bulk_page(bot, query.message, user_id, page=page, is_callback=True)

@Client.on_callback_query(filters.regex(r"^bulk_generate_(\d+)$"))
async def bulk_generate_callback(bot: Client, query):
    user_id = query.from_user.id
    if user_id not in user_selections or not any(user_selections[user_id].values()):
        return await query.answer("ᴘʟᴇᴀsᴇ sᴇʟᴇᴄᴛ ᴀᴛ ʟᴇᴀsᴛ ᴏɴᴇ ᴄʜᴀɴɴᴇʟ!", show_alert=True)

    selected_ids = [cid for cid, val in user_selections[user_id].items() if val]
    await query.message.edit_text(f"⏳ **ɢᴇɴᴇʀᴀᴛɪɴɢ ʟɪɴᴋs ғᴏʀ {len(selected_ids)} ᴄʜᴀɴɴᴇʟs...**")

    result_text = f"{T_BANNER}\n{T_DIVIDER}\n**ʙᴜʟᴋ ʟɪɴᴋs ɢᴇɴᴇʀᴀᴛᴇᴅ:**\n\n"
    expiry_date = datetime.utcnow() + timedelta(minutes=5)

    for cid in selected_ids:
        try:
            ch = await db.get_channel(cid)
            invite = await bot.create_chat_invite_link(chat_id=cid, expire_date=expiry_date)
            result_text += f"📡 **{ch['title']}**\n🔗 `{invite.invite_link}`\n\n"

            # Save for auto-revoke
            await db.save_generated_link(
                channel_id=cid,
                invite_link=invite.invite_link,
                message_id=query.message.id,
                chat_id=query.message.chat.id,
                expiry_time=expiry_date
            )
        except Exception as e:
            result_text += f"📡 **ID: {cid}**\n{E_ERROR} Error: `{str(e)}`\n\n"

    result_text += f"{E_REVOKE} **ᴀʟʟ ʟɪɴᴋs ᴇxᴘɪʀᴇ ɪɴ 5 ᴍɪɴs**\n{T_DIVIDER}"
    await query.message.edit_text(result_text)
    user_selections.pop(user_id, None)

async def show_bulk_page(bot, message, user_id, page=1, is_callback=False):
    channels = await db.get_all_channels()
    if not channels:
        return await message.reply_text(f"{E_ERROR} **ɴᴏ ᴄʜᴀɴɴᴇʟs ᴀᴠᴀɪʟᴀʙʟᴇ!**")

    per_page = 8
    total_pages = math.ceil(len(channels) / per_page)
    start = (page - 1) * per_page
    end = start + per_page

    text = f"{T_BANNER}\n{T_DIVIDER}\n**sᴇʟᴇᴄᴛ ᴄʜᴀɴɴᴇʟs ғᴏʀ ʙᴜʟᴋ ɢᴇɴ:**\n(ᴘᴀɢᴇ {page}/{total_pages})\n{T_DIVIDER}"

    buttons = []
    selection = user_selections.get(user_id, {})

    for ch in channels[start:end]:
        is_selected = selection.get(ch['_id'], False)
        prefix = "✅ " if is_selected else "❌ "
        buttons.append([InlineKeyboardButton(f"{prefix}{ch['title']}", callback_data=f"bulk_toggle_{ch['_id']}_{page}")])

    # Navigation
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ ᴘʀᴇᴠ", callback_data=f"bulk_page_{page-1}"))
    if page < total_pages:
        nav.append(InlineKeyboardButton("ɴᴇxᴛ ➡️", callback_data=f"bulk_page_{page+1}"))
    if nav:
        buttons.append(nav)

    buttons.append([InlineKeyboardButton("🚀 ɢᴇɴᴇʀᴀᴛᴇ", callback_data=f"bulk_generate_{page}")])
    buttons.append([InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="admin_panel")])

    if is_callback:
        await message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
