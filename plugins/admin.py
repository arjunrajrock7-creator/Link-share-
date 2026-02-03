import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db
from config import *

@Client.on_message(filters.command("addadmin") & filters.private)
async def add_admin_handler(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/addadmin <ᴜsᴇʀ_ɪᴅ>`")

    try:
        user_id = int(message.command[1])
        await db.add_admin(user_id)
        await message.reply_text(f"{E_SUCCESS} **ᴀᴅᴍɪɴ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**")
    except Exception as e:
        await message.reply_text(f"{E_ERROR} **ᴇʀʀᴏʀ:** `{str(e)}`")

@Client.on_message(filters.command("rmadmin") & filters.private)
async def rm_admin_handler(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/rmadmin <ᴜsᴇʀ_ɪᴅ>`")

    try:
        user_id = int(message.command[1])
        await db.remove_admin(user_id)
        await message.reply_text(f"{E_SUCCESS} **ᴀᴅᴍɪɴ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**")
    except Exception as e:
        await message.reply_text(f"{E_ERROR} **ᴇʀʀᴏʀ:** `{str(e)}`")

@Client.on_message(filters.command("admins") & filters.private)
async def admins_list_handler(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID and not await db.is_admin(message.from_user.id):
        return

    admins = await db.get_all_admins()
    if not admins:
        return await message.reply_text("ɴᴏ ᴀᴅᴍɪɴs ᴀᴅᴅᴇᴅ ʏᴇᴛ.")

    text = f"{T_BANNER}\n{T_DIVIDER}\n**ʟɪsᴛ ᴏғ ᴀᴅᴍɪɴs:**\n\n"
    for admin_id in admins:
        text += f"👤 `{admin_id}`\n"
    text += T_DIVIDER
    await message.reply_text(text)

@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID and not await db.is_admin(message.from_user.id):
        return

    if not message.reply_to_message:
        return await message.reply_text(f"{E_ERROR} **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ!**")

    users = await db.get_all_users()
    total = await db.get_total_users()

    sts = await message.reply_text(f"{E_BROADCAST} **ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛᴇᴅ...**")
    done = 0
    failed = 0
    success = 0

    async for user in users:
        try:
            await message.reply_to_message.copy(chat_id=user['_id'])
            success += 1
        except:
            failed += 1
        done += 1
        if done % 20 == 0:
            await sts.edit_text(f"{E_BROADCAST} **ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ:**\n\nᴛᴏᴛᴀʟ: {total}\nᴅᴏɴᴇ: {done}\nsᴜᴄᴄᴇss: {success}\nғᴀɪʟᴇᴅ: {failed}")

    await sts.edit_text(f"{E_SUCCESS} **ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!**\n\nᴛᴏᴛᴀʟ: {total}\nsᴜᴄᴄᴇss: {success}\nғᴀɪʟᴇᴅ: {failed}")

@Client.on_message(filters.command("stats") & filters.private)
async def stats_handler(bot: Client, message: Message):
    total_users = await db.get_total_users()
    total_channels = len(await db.get_all_channels())

    text = (
        f"{T_BANNER}\n"
        f"{T_DIVIDER}\n"
        f"📊 **ʙᴏᴛ sᴛᴀᴛs:**\n\n"
        f"👤 **ᴛᴏᴛᴀʟ ᴜsᴇʀs:** `{total_users}`\n"
        f"📡 **ᴛᴏᴛᴀʟ ᴄʜᴀɴɴᴇʟs:** `{total_channels}`\n"
        f"{T_DIVIDER}"
    )
    await message.reply_text(text)

@Client.on_callback_query(filters.regex("^stats$"))
async def stats_callback(bot: Client, query):
    total_users = await db.get_total_users()
    total_channels = len(await db.get_all_channels())

    text = (
        f"{T_BANNER}\n"
        f"{T_DIVIDER}\n"
        f"📊 **ʙᴏᴛ sᴛᴀᴛs:**\n\n"
        f"👤 **ᴛᴏᴛᴀʟ ᴜsᴇʀs:** `{total_users}`\n"
        f"📡 **ᴛᴏᴛᴀʟ ᴄʜᴀɴɴᴇʟs:** `{total_channels}`\n"
        f"{T_DIVIDER}"
    )
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start_back")]]))

@Client.on_message(filters.command("status") & filters.private)
async def status_handler(bot: Client, message: Message):
    start_time = time.time()
    msg = await message.reply_text("⚡ **ᴘɪɴɢɪɴɢ...**")
    end_time = time.time()
    ping = round((end_time - start_time) * 1000, 2)

    uptime_seconds = (datetime.now() - bot.uptime).total_seconds()
    uptime = timedelta(seconds=int(uptime_seconds))

    text = (
        f"{T_BANNER}\n"
        f"{T_DIVIDER}\n"
        f"📡 **sʏsᴛᴇᴍ sᴛᴀᴛᴜs:**\n\n"
        f"🏓 **ᴘɪɴɢ:** `{ping}ᴍs`\n"
        f"🆙 **ᴜᴘᴛɪᴍᴇ:** `{str(uptime)}`\n"
        f"💾 **ᴅᴀᴛᴀʙᴀsᴇ:** `ᴄᴏɴɴᴇᴄᴛᴇᴅ`\n"
        f"{T_DIVIDER}"
    )
    await msg.edit_text(text)

@Client.on_callback_query(filters.regex("^admin_panel$"))
async def admin_panel_callback(bot: Client, query):
    user_id = query.from_user.id
    if user_id != OWNER_ID and not await db.is_admin(user_id):
        return await query.answer("ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ!", show_alert=True)

    buttons = [
        [
            InlineKeyboardButton(f"{E_CHANNELS} ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ", callback_data="add_ch_admin"),
            InlineKeyboardButton(f"{E_CHANNELS} ʀᴇᴍᴏᴠᴇ ᴄʜᴀɴɴᴇʟ", callback_data="rm_ch_admin")
        ],
        [
            InlineKeyboardButton(f"{E_BULK} ʙᴜʟᴋ ɢᴇɴ", callback_data="bulk_page_1"),
            InlineKeyboardButton(f"{E_FSUB} ғsᴜʙ sᴇᴛᴛɪɴɢs", callback_data="fsub_admin")
        ],
        [
            InlineKeyboardButton(f"{E_ADMIN} ᴀᴅᴍɪɴ ʟɪsᴛ", callback_data="admin_list_cb")
        ],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start_back")]
    ]

    await query.message.edit_text(f"{T_BANNER}\n{T_DIVIDER}\n**ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ!**\n{T_DIVIDER}", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^admin_list_cb$"))
async def admin_list_cb(bot: Client, query):
    admins = await db.get_all_admins()
    text = f"**ᴀᴅᴍɪɴ ʟɪsᴛ:**\n\n"
    for a in admins:
        text += f"👤 `{a}`\n"
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="admin_panel")]]))

@Client.on_callback_query(filters.regex("^add_ch_admin$"))
async def add_ch_admin_cb(bot: Client, query):
    await query.message.edit_text("ᴘʟᴇᴀsᴇ ᴜsᴇ /addchannel ᴄᴏᴍᴍᴀɴᴅ!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="admin_panel")]]))

@Client.on_callback_query(filters.regex("^rm_ch_admin$"))
async def rm_ch_admin_cb(bot: Client, query):
    await query.message.edit_text("ᴘʟᴇᴀsᴇ ᴜsᴇ /removechannel ᴄᴏᴍᴍᴀɴᴅ!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="admin_panel")]]))

@Client.on_callback_query(filters.regex("^fsub_admin$"))
async def fsub_admin_cb(bot: Client, query):
    fsubs = await db.get_all_fsub()
    text = f"**ғsᴜʙ ᴄʜᴀɴɴᴇʟs:**\n\n"
    for f in fsubs:
        text += f"🔐 `{f}`\n"
    text += "\nᴜsᴇ /fsub_add ᴀɴᴅ /fsub_remove ᴛᴏ ᴍᴀɴᴀɢᴇ."
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="admin_panel")]]))
