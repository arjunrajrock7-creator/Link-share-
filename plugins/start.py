import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from database.database import db
from plugins.fsub import force_sub
from utils.decorators import debounce
import time

@Client.on_message(filters.command("start") & filters.private)
@debounce(1.5)
@force_sub
async def start_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    await db.add_user(user_id, message.from_user.username)

    text = message.text.split()
    if len(text) > 1:
        # Handle Deep Links
        token = text[1]
        link_data = await db.get_external_link(token)
        if link_data:
            # External Link
            caption = (
                f"{T_BANNER}\n"
                f"{T_DIVIDER}\n"
                f"**ʏᴏᴜʀ ʟɪɴᴋ ɪs ʀᴇᴀᴅʏ!**\n"
                f"{T_DIVIDER}\n"
                f"{SUPPORT_LINE}"
            )
            buttons = [[InlineKeyboardButton("🔗 ᴏᴘᴇɴ ʟɪɴᴋ", url=link_data['url'])]]
            return await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(buttons))

    # Regular Start
    mention = message.from_user.mention
    caption = START_MSG.format(
        banner=T_BANNER,
        divider=T_DIVIDER,
        mention=mention,
        pray=E_PRAY,
        link=E_LINK,
        revoke=E_REVOKE,
        bulk=E_BULK,
        support=SUPPORT_LINE
    )

    buttons = [
        [
            InlineKeyboardButton(f"{E_HELP} ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton(f"{E_CHANNELS} ᴄʜᴀɴɴᴇʟs", callback_data="channels_list")
        ],
        [
            InlineKeyboardButton(f"{E_STATS} sᴛᴀᴛs", callback_data="stats")
        ]
    ]

    # Check if admin
    if user_id == OWNER_ID or await db.is_admin(user_id):
        buttons.append([InlineKeyboardButton(f"{E_ADMIN} ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", callback_data="admin_panel")])

    await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.command("help") & filters.private)
@debounce(1.5)
@force_sub
async def help_handler(bot: Client, message: Message):
    caption = HELP_MSG.format(
        banner=T_BANNER,
        divider=T_DIVIDER,
        support=SUPPORT_LINE
    )
    await message.reply_text(caption)

@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(bot: Client, query):
    await query.answer()
    caption = HELP_MSG.format(
        banner=T_BANNER,
        divider=T_DIVIDER,
        support=SUPPORT_LINE
    )
    await query.message.edit_text(caption, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start_back")]]))

@Client.on_callback_query(filters.regex("^start_back$"))
@force_sub
async def start_back(bot: Client, query):
    await query.answer()
    mention = query.from_user.mention
    caption = START_MSG.format(
        banner=T_BANNER,
        divider=T_DIVIDER,
        mention=mention,
        pray=E_PRAY,
        link=E_LINK,
        revoke=E_REVOKE,
        bulk=E_BULK,
        support=SUPPORT_LINE
    )

    buttons = [
        [
            InlineKeyboardButton(f"{E_HELP} ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton(f"{E_CHANNELS} ᴄʜᴀɴɴᴇʟs", callback_data="channels_list")
        ],
        [
            InlineKeyboardButton(f"{E_STATS} sᴛᴀᴛs", callback_data="stats")
        ]
    ]

    if query.from_user.id == OWNER_ID or await db.is_admin(query.from_user.id):
        buttons.append([InlineKeyboardButton(f"{E_ADMIN} ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", callback_data="admin_panel")])

    await query.message.edit_text(caption, reply_markup=InlineKeyboardMarkup(buttons))
