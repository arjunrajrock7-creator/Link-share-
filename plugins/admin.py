import asyncio
import time
import string
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from database.database import db
from datetime import datetime, timedelta
import platform
from pyrogram.errors import PeerIdInvalid

@Client.on_message(filters.command("addchannel") & filters.private)
async def add_channel(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID and not await db.is_admin(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/addchannel -100xxxxxxxxxx`")

    channel_id = int(message.command[1])
    try:
        chat = await bot.get_chat(channel_id)
        await db.add_channel(channel_id, chat.title)
        await message.reply_text(f"{E_SUCCESS} **ᴀᴅᴅᴇᴅ {chat.title} ({channel_id})**")
    except (PeerIdInvalid, Exception) as e:
        if isinstance(e, PeerIdInvalid) or "Peer id invalid" in str(e):
             await message.reply_text(
                f"{E_ERROR} **ᴇʀʀᴏʀ: ᴘᴇᴇʀ ɪᴅ ɪɴᴠᴀʟɪᴅ!**\n\n"
                f"📌 **ᴛɪᴘs ᴛᴏ ғɪx:**\n"
                f"1️⃣ ᴍᴀᴋᴇ sᴜʀᴇ ᴛʜᴇ ʙᴏᴛ ɪs **ᴀᴅᴍɪɴ** ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.\n"
                f"2️⃣ sᴇɴᴅ ᴀ ᴛᴇsᴛ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴀғᴛᴇʀ ᴀᴅᴅɪɴɢ ᴛʜᴇ ʙᴏᴛ.\n"
                f"3️⃣ ғᴏʀᴡᴀʀᴅ ᴀɴʏ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛʜɪs ʙᴏᴛ, ᴛʜᴇɴ ᴛʀʏ ᴀɢᴀɪɴ."
            )
        else:
            await message.reply_text(f"{E_ERROR} **ᴇʀʀᴏʀ:** {e}")

@Client.on_message(filters.command("removechannel") & filters.private)
async def remove_channel(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID and not await db.is_admin(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/removechannel -100xxxxxxxxxx`")

    channel_id = int(message.command[1])
    await db.remove_channel(channel_id)
    await message.reply_text(f"{E_SUCCESS} **ʀᴇᴍᴏᴠᴇᴅ {channel_id}**")

@Client.on_message(filters.command("genlink") & filters.private)
async def gen_link_external(bot: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/genlink <url>`")

    url = message.text.split(None, 1)[1]
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    await db.save_external_link(token, url)

    bot_url = f"https://t.me/{bot.username}?start={token}"
    await message.reply_text(
        f"✨ {T_BANNER}\n"
        f"{T_DIVIDER}\n"
        f"🔗 **ʏᴏᴜʀ ᴇɴᴄᴏᴅᴇᴅ ʟɪɴᴋ:**\n"
        f"`{bot_url}`\n"
        f"{T_DIVIDER}\n"
        f"{SUPPORT_LINE}"
    )

@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID and not await db.is_admin(message.from_user.id):
        return

    if not message.reply_to_message:
        return await message.reply_text(f"{E_ERROR} **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ.**")

    msg = await message.reply_text("⚡ **ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛɪɴɢ...**")
    users = await db.get_all_users()
    count = 0
    total = await db.get_total_users()

    async for user in users:
        try:
            await message.reply_to_message.copy(user['_id'])
            count += 1
            if count % 100 == 0:
                await msg.edit_text(f"📢 **ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ:** `{count}/{total}`")
        except:
            pass

    await msg.edit_text(f"{E_SUCCESS} **ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!**\n\n{E_SUCCESS} sᴇɴᴛ ᴛᴏ: `{count}` users.")

@Client.on_message(filters.command("stats") & filters.private)
async def stats(bot: Client, message: Message):
    users = await db.get_total_users()
    channels = len(await db.get_all_channels())
    latency = await db.health_check()

    text = (
        f"📊 **𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀:**\n"
        f"{T_DIVIDER}\n"
        f"👤 **ᴛᴏᴛᴀʟ ᴜsᴇʀs:** `{users}`\n"
        f"📡 **ᴛᴏᴛᴀʟ ᴄʜᴀɴɴᴇʟs:** `{channels}`\n"
        f"⚡ **ᴅʙ ʟᴀᴛᴇɴᴄʏ:** `{latency}ms`\n"
        f"{T_DIVIDER}"
    )
    await message.reply_text(text)

@Client.on_callback_query(filters.regex("^stats$"))
async def stats_callback(bot: Client, query: CallbackQuery):
    await query.answer()
    users = await db.get_total_users()
    channels = len(await db.get_all_channels())
    latency = await db.health_check()

    text = (
        f"📊 **𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀:**\n"
        f"{T_DIVIDER}\n"
        f"👤 **ᴛᴏᴛᴀʟ ᴜsᴇʀs:** `{users}`\n"
        f"📡 **ᴛᴏᴛᴀʟ ᴄʜᴀɴɴᴇʟs:** `{channels}`\n"
        f"⚡ **ᴅʙ ʟᴀᴛᴇɴᴄʏ:** `{latency}ms`\n"
        f"{T_DIVIDER}"
    )
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start_back")]]))

@Client.on_callback_query(filters.regex("^admin_panel$"))
async def admin_panel_callback(bot: Client, query: CallbackQuery):
    if query.from_user.id != OWNER_ID and not await db.is_admin(query.from_user.id):
        return await query.answer("ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ!", show_alert=True)

    await query.answer()
    text = HELP_MSG.format(
        banner=T_BANNER,
        divider=T_DIVIDER,
        support=SUPPORT_LINE
    )
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start_back")]]))

@Client.on_callback_query(filters.regex("^none$"))
async def none_callback(bot: Client, query: CallbackQuery):
    await query.answer()

@Client.on_message(filters.command("ping") & filters.private)
async def ping(bot: Client, message: Message):
    start = time.time()
    msg = await message.reply_text("⚡ **ᴘɪɴɢɪɴɢ...**")
    end = time.time()
    latency = round((end - start) * 1000, 2)
    await msg.edit_text(f"🚀 **ᴘᴏɴɢ:** `{latency}ms`")

@Client.on_message(filters.command("addadmin") & filters.private & filters.user(OWNER_ID))
async def add_admin_cmd(bot: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("ᴜsᴀɢᴇ: `/addadmin <id>`")
    user_id = int(message.command[1])
    await db.add_admin(user_id)
    await message.reply_text(f"{E_SUCCESS} User `{user_id}` added as admin.")

@Client.on_message(filters.command("rmadmin") & filters.private & filters.user(OWNER_ID))
async def rm_admin_cmd(bot: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("ᴜsᴀɢᴇ: `/rmadmin <id>`")
    user_id = int(message.command[1])
    await db.remove_admin(user_id)
    await message.reply_text(f"{E_ERROR} User `{user_id}` removed from admins.")

@Client.on_message(filters.command("admins") & filters.private)
async def admins_list(bot: Client, message: Message):
    admins = await db.get_all_admins()
    text = "👨‍💻 **𝗕𝗼𝘁 𝗔𝗱𝗺𝗶𝗻𝘀:**\n\n"
    text += f"1. `{OWNER_ID}` (OWNER)\n"
    for i, adm in enumerate(admins, 2):
        text += f"{i}. `{adm}`\n"
    await message.reply_text(text)

@Client.on_message(filters.command("fsub_add") & filters.private)
async def fsub_add_cmd(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID and not await db.is_admin(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/fsub_add -100xxxxxxxxxx`")

    channel_id = int(message.command[1])
    await db.add_fsub(channel_id)
    await message.reply_text(f"{E_SUCCESS} **ᴀᴅᴅᴇᴅ {channel_id} ᴛᴏ ғsᴜʙ!**")

@Client.on_message(filters.command("fsub_remove") & filters.private)
async def fsub_remove_cmd(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID and not await db.is_admin(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/fsub_remove -100xxxxxxxxxx`")

    channel_id = int(message.command[1])
    await db.remove_fsub(channel_id)
    await message.reply_text(f"{E_SUCCESS} **ʀᴇᴍᴏᴠᴇᴅ {channel_id} ғʀᴏᴍ ғsᴜʙ!**")

@Client.on_message(filters.command("status") & filters.private)
async def status_cmd(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID and not await db.is_admin(message.from_user.id):
        return

    if hasattr(bot, "uptime"):
        uptime_sec = (datetime.now() - bot.uptime).total_seconds()
        uptime = str(timedelta(seconds=int(uptime_sec)))
    else:
        uptime = "Unknown"

    py_ver = platform.python_version()
    bot_ver = "1.0.0"

    text = (
        f"🚀 **𝗕𝗼𝘁 𝗦𝘆𝘀𝘁𝗲𝗺 𝗦𝘁𝗮𝘁𝘂𝘀**\n"
        f"{T_DIVIDER}\n"
        f"⏱️ **ᴜᴘᴛɪᴍᴇ:** `{uptime}`\n"
        f"🐍 **ᴘʏᴛʜᴏɴ:** `{py_ver}`\n"
        f"🤖 **ʙᴏᴛ ᴠᴇʀsɪᴏɴ:** `{bot_ver}`\n"
        f"💻 **ᴘʟᴀᴛғᴏʀᴍ:** `{platform.system()}`\n"
        f"{T_DIVIDER}"
    )
    await message.reply_text(text)
