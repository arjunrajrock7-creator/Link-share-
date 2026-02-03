import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from database.database import db
from datetime import datetime, timedelta
from utils.pagination import get_pagination

CHANNELS_PER_PAGE = 10
selected_channels = {} # user_id: [channel_ids]

@Client.on_message(filters.command("bulkgen") & filters.private)
async def bulk_gen_cmd(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID and not await db.is_admin(message.from_user.id):
        return
    await show_bulk_selection(bot, message, page=1)

@Client.on_callback_query(filters.regex(r"^bulk_page_(\d+)$"))
async def bulk_page_callback(bot: Client, query: CallbackQuery):
    if query.from_user.id != OWNER_ID and not await db.is_admin(query.from_user.id):
        return await query.answer("ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ!", show_alert=True)
    await query.answer()
    page = int(query.data.split("_")[2])
    await show_bulk_selection(bot, query, page=page)

async def show_bulk_selection(bot, message_or_query, page):
    user_id = message_or_query.from_user.id
    channels = await db.get_all_channels()
    if not channels:
        if isinstance(message_or_query, Message):
            return await message_or_query.reply_text("ɴᴏ ᴄʜᴀɴɴᴇʟs ᴀᴅᴅᴇᴅ!")
        else:
            return await message_or_query.answer("ɴᴏ ᴄʜᴀɴɴᴇʟs!", show_alert=True)

    total_pages = (len(channels) + CHANNELS_PER_PAGE - 1) // CHANNELS_PER_PAGE
    start = (page - 1) * CHANNELS_PER_PAGE
    end = start + CHANNELS_PER_PAGE

    if user_id not in selected_channels:
        selected_channels[user_id] = []

    text = f"📦 **𝗕𝘂𝗹𝗸 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗼𝗿 (𝗣𝗮𝗴𝗲 {page}/{total_pages})**\n\n sᴇʟᴇᴄᴛ ᴄʜᴀɴɴᴇʟs:"
    buttons = []
    for ch in channels[start:end]:
        mark = "✅ " if ch['_id'] in selected_channels[user_id] else ""
        buttons.append([InlineKeyboardButton(f"{mark}{ch['title']}", callback_data=f"bulk_select_{ch['_id']}_{page}")])

    pagination_buttons = get_pagination(page, total_pages, "bulk_page")
    if pagination_buttons:
        buttons.extend(pagination_buttons)

    buttons.append([InlineKeyboardButton("🚀 ɢᴇɴᴇʀᴀᴛᴇ sᴇʟᴇᴄᴛᴇᴅ", callback_data="bulk_gen_run")])
    buttons.append([InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start_back")])

    markup = InlineKeyboardMarkup(buttons)
    if isinstance(message_or_query, Message):
        await message_or_query.reply_text(text, reply_markup=markup)
    else:
        await message_or_query.message.edit_text(text, reply_markup=markup)

@Client.on_callback_query(filters.regex("^bulk_select_"))
async def bulk_select_callback(bot: Client, query: CallbackQuery):
    if query.from_user.id != OWNER_ID and not await db.is_admin(query.from_user.id):
        return await query.answer("ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ!", show_alert=True)
    await query.answer()
    user_id = query.from_user.id
    parts = query.data.split("_")
    channel_id = int(parts[2])
    page = int(parts[3])

    if user_id not in selected_channels:
        selected_channels[user_id] = []

    if channel_id in selected_channels[user_id]:
        selected_channels[user_id].remove(channel_id)
    else:
        selected_channels[user_id].append(channel_id)

    await show_bulk_selection(bot, query, page=page)

@Client.on_callback_query(filters.regex("^bulk_gen_run$"))
async def bulk_gen_run(bot: Client, query: CallbackQuery):
    if query.from_user.id != OWNER_ID and not await db.is_admin(query.from_user.id):
        return await query.answer("ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ!", show_alert=True)
    await query.answer()
    user_id = query.from_user.id
    if user_id not in selected_channels or not selected_channels[user_id]:
        return await query.answer("sᴇʟᴇᴄᴛ ᴀᴛʟᴇᴀsᴛ ᴏɴᴇ!", show_alert=True)

    await query.message.edit_text("⏳ **ɢᴇɴᴇʀᴀᴛɪɴɢ ʟɪɴᴋs...**")

    for ch_id in selected_channels[user_id]:
        try:
            ch = await db.get_channel(ch_id)
            if ch.get('request_approval'):
                link_obj = await bot.create_chat_invite_link(ch_id, creates_join_request=True)
            else:
                link_obj = await bot.create_chat_invite_link(ch_id)

            expiry = datetime.utcnow() + timedelta(minutes=5)
            msg = await bot.send_message(
                chat_id=user_id,
                text=f"🎋 {T_BANNER}\n{T_DIVIDER}\n📡 **ᴄʜᴀɴɴᴇʟ:** {ch['title']}\n🔗 **ʟɪɴᴋ:** {link_obj.invite_link}\n⏱️ **ᴇxᴘɪʀᴇs ɪɴ 𝟓 ᴍɪɴs**\n{T_DIVIDER}"
            )
            await db.save_generated_link(ch_id, link_obj.invite_link, msg.id, user_id, expiry)
        except Exception as e:
            logging.error(f"Error in bulk gen for {ch_id}: {e}")

    await query.message.delete()
    selected_channels[user_id] = []

@Client.on_callback_query(filters.regex("^gen_choice_"))
async def gen_choice_callback(bot: Client, query: CallbackQuery):
    await query.answer()
    channel_id = int(query.data.split("_")[2])
    buttons = [
        [
            InlineKeyboardButton("🔗 ɴᴏʀᴍᴀʟ ʟɪɴᴋ", callback_data=f"gen_norm_{channel_id}"),
            InlineKeyboardButton("📝 ʀᴇǫᴜᴇsᴛ ʟɪɴᴋ", callback_data=f"gen_req_{channel_id}")
        ]
    ]
    await query.message.edit_text("⚡ **ᴄʜᴏᴏsᴇ ʟɪɴᴋ ᴛʏᴘᴇ:**", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^gen_(norm|req)_"))
async def gen_link_callback(bot: Client, query: CallbackQuery):
    await query.answer()
    type = query.data.split("_")[1]
    channel_id = int(query.data.split("_")[2])
    await query.message.edit_text("⏳ **ɢᴇɴᴇʀᴀᴛɪɴɢ...**")
    try:
        ch = await db.get_channel(channel_id)
        if type == "req":
            link_obj = await bot.create_chat_invite_link(channel_id, creates_join_request=True)
        else:
            link_obj = await bot.create_chat_invite_link(channel_id)
        expiry = datetime.utcnow() + timedelta(minutes=5)
        text = f"✨ {T_BANNER}\n{T_DIVIDER}\n📡 **ᴄʜᴀɴɴᴇʟ:** {ch['title']}\n🔗 **ʟɪɴᴋ:** {link_obj.invite_link}\n⏱️ **ᴇxᴘɪʀᴇs ɪɴ 𝟓 ᴍɪɴs**\n{T_DIVIDER}\n{SUPPORT_LINE}"
        await query.message.edit_text(text)
        await db.save_generated_link(channel_id, link_obj.invite_link, query.message.id, query.from_user.id, expiry)
    except Exception as e:
        await query.message.edit_text(f"{E_ERROR} **ᴇʀʀᴏʀ:** {e}")
