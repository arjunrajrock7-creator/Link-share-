import secrets
import string
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db
from config import *
from datetime import datetime, timedelta
from utils.decorators import debounce

def generate_token(length=8):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))

@Client.on_message(filters.command("genlink") & filters.private)
@debounce(1.5)
async def genlink_handler(bot: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/genlink <ᴜʀʟ>`")

    url = message.command[1]
    if not url.startswith(("http://", "https://")):
        return await message.reply_text(f"{E_ERROR} **ɪɴᴠᴀʟɪᴅ ᴜʀʟ!**")

    token = generate_token()
    await db.save_external_link(token, url)

    bot_link = f"https://t.me/{bot.username}?start={token}"

    caption = (
        f"{T_BANNER}\n"
        f"{T_DIVIDER}\n"
        f"{E_SUCCESS} **ʟɪɴᴋ ᴇɴᴄᴏᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
        f"**ʙᴏᴛ ʟɪɴᴋ:** `{bot_link}`\n"
        f"{T_DIVIDER}\n"
        f"{SUPPORT_LINE}"
    )
    await message.reply_text(caption)

@Client.on_message(filters.command("link") & filters.private)
@debounce(1.5)
async def single_link_gen(bot: Client, message: Message):
    # This is for generating channel invite links
    user_id = message.from_user.id
    if user_id != OWNER_ID and not await db.is_admin(user_id):
        return

    channels = await db.get_all_channels()
    if not channels:
        return await message.reply_text(f"{E_ERROR} **ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ!**")

    buttons = []
    for ch in channels:
        buttons.append([InlineKeyboardButton(ch['title'], callback_data=f"gen_choice_{ch['_id']}")])

    await message.reply_text(f"**sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ʟɪɴᴋ:**", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex(r"^gen_choice_(-?\d+)$"))
async def gen_choice_callback(bot: Client, query):
    channel_id = int(query.data.split("_")[-1])
    buttons = [
        [
            InlineKeyboardButton("🔗 ɴᴏʀᴍᴀʟ ʟɪɴᴋ", callback_data=f"gen_link_normal_{channel_id}"),
            InlineKeyboardButton("📝 ʀᴇǫᴜᴇsᴛ ʟɪɴᴋ", callback_data=f"gen_link_request_{channel_id}")
        ],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="channels_list")]
    ]
    await query.message.edit_text(f"**ᴄʜᴏᴏsᴇ ʟɪɴᴋ ᴛʏᴘᴇ:**", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex(r"^gen_link_(normal|request)_(-?\d+)$"))
async def gen_link_final(bot: Client, query):
    data = query.data.split("_")
    link_type = data[2]
    channel_id = int(data[3])
    is_request = (link_type == "request")

    try:
        # Generate link with 5 min expiry
        expiry_date = datetime.utcnow() + timedelta(minutes=5)
        invite = await bot.create_chat_invite_link(
            chat_id=channel_id,
            creates_join_request=is_request,
            expire_date=expiry_date
        )

        invite_link = invite.invite_link

        caption = (
            f"{T_BANNER}\n"
            f"{T_DIVIDER}\n"
            f"{E_LINK} **ʏᴏᴜʀ ɪɴᴠɪᴛᴇ ʟɪɴᴋ:**\n"
            f"`{invite_link}`\n\n"
            f"{E_REVOKE} **ᴇxᴘɪʀᴇs ɪɴ 5 ᴍɪɴᴜᴛᴇs**\n"
            f"{T_DIVIDER}\n"
            f"{SUPPORT_LINE}"
        )

        msg = await query.message.edit_text(caption)

        # Save for auto-revoke
        await db.save_generated_link(
            channel_id=channel_id,
            invite_link=invite_link,
            message_id=msg.id,
            chat_id=query.message.chat.id,
            expiry_time=expiry_date
        )

    except Exception as e:
        await query.answer(f"Error: {str(e)}", show_alert=True)
