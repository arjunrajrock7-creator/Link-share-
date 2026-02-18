import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
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
            try:
                return await message.reply_photo(photo=START_IMG, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
            except:
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
        support=SUPPORT_LINE,
        owner=OWNER_NAME
    )

    buttons = [
        [
            InlineKeyboardButton(f"{E_HELP} ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton(f"{E_CHANNELS} ᴄʜᴀɴɴᴇʟs", callback_data="channels_list")
        ],
        [
            InlineKeyboardButton(f"{E_STATS} sᴛᴀᴛs", callback_data="stats"),
            InlineKeyboardButton(f"👤 ᴏᴡɴᴇʀ", url=SUPPORT_LINK)
        ]
    ]

    # Check if admin
    if user_id == OWNER_ID or await db.is_admin(user_id):
        buttons.append([InlineKeyboardButton(f"{E_ADMIN} ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", callback_data="admin_panel")])

    try:
        await message.reply_photo(photo=START_IMG, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
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
    try:
        await message.reply_photo(photo=START_IMG, caption=caption)
    except:
        await message.reply_text(caption)

@Client.on_message(filters.private & ~filters.command(["start", "help", "channels", "settings", "genlink", "bulkgen", "batch", "requeston", "requestoff", "addadmin", "rmadmin", "admins", "broadcast", "stats", "status", "ping", "fsub_add", "fsub_remove", "addchannel", "removechannel"]))
@force_sub
async def search_handler(bot: Client, message: Message):
    query = message.text
    if not query:
        return

    channels = await db.get_all_channels()
    results = [ch for ch in channels if query.lower() in ch['title'].lower()]

    if not results:
        return await message.reply_text(f"{E_ERROR} **ɴᴏ ᴄʜᴀɴɴᴇʟs ғᴏᴜɴᴅ ғᴏʀ '{query}'**\n\n{SUPPORT_LINE}")

    text = f"{T_BANNER}\n{T_DIVIDER}\n**sᴇᴀʀᴄʜ ʀᴇsᴜʟᴛs ғᴏʀ '{query}':**\n\n"
    buttons = []
    for ch in results[:10]: # Limit to 10 results
        buttons.append([InlineKeyboardButton(f"📡 {ch['title']}", callback_data=f"gen_choice_{ch['_id']}")])

    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(bot: Client, query):
    await query.answer()
    caption = HELP_MSG.format(
        banner=T_BANNER,
        divider=T_DIVIDER,
        support=SUPPORT_LINE
    )
    try:
        await query.message.edit_message_media(
            media=InputMediaPhoto(media=START_IMG, caption=caption),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="start_back")]])
        )
    except:
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
        support=SUPPORT_LINE,
        owner=OWNER_NAME
    )

    buttons = [
        [
            InlineKeyboardButton(f"{E_HELP} ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton(f"{E_CHANNELS} ᴄʜᴀɴɴᴇʟs", callback_data="channels_list")
        ],
        [
            InlineKeyboardButton(f"{E_STATS} sᴛᴀᴛs", callback_data="stats"),
            InlineKeyboardButton(f"👤 ᴏᴡɴᴇʀ", url=SUPPORT_LINK)
        ]
    ]

    if query.from_user.id == OWNER_ID or await db.is_admin(query.from_user.id):
        buttons.append([InlineKeyboardButton(f"{E_ADMIN} ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", callback_data="admin_panel")])

    try:
        await query.message.edit_message_media(
            media=InputMediaPhoto(media=START_IMG, caption=caption),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        await query.message.edit_text(caption, reply_markup=InlineKeyboardMarkup(buttons))
