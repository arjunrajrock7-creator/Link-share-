from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db
from config import *
from utils.decorators import debounce
from datetime import datetime, timedelta

@Client.on_message(filters.command("batch") & filters.private)
@debounce(2.0)
async def batch_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and not await db.is_admin(user_id):
        return

    if len(message.command) < 2:
        return await message.reply_text(f"{E_ERROR} **ᴜsᴀɢᴇ:** `/batch -100xxx -100yyy ...`")

    ids = message.command[1:]
    result_text = f"{T_BANNER}\n{T_DIVIDER}\n**ʙᴀᴛᴄʜ ʟɪɴᴋs ɢᴇɴᴇʀᴀᴛᴇᴅ:**\n\n"
    expiry_date = datetime.utcnow() + timedelta(minutes=5)

    for cid_str in ids:
        try:
            cid = int(cid_str)
            ch = await db.get_channel(cid)
            if not ch:
                # Try to fetch chat info if not in DB
                chat = await bot.get_chat(cid)
                await db.add_channel(cid, chat.title)
                title = chat.title
            else:
                title = ch['title']

            invite = await bot.create_chat_invite_link(chat_id=cid, expire_date=expiry_date)
            result_text += f"📡 **{title}**\n🔗 `{invite.invite_link}`\n\n"

            await db.save_generated_link(
                channel_id=cid,
                invite_link=invite.invite_link,
                message_id=message.id, # Using command message ID as anchor
                chat_id=message.chat.id,
                expiry_time=expiry_date
            )
        except Exception as e:
            result_text += f"📡 **ID: {cid_str}**\n{E_ERROR} Error: `{str(e)}`\n\n"

    result_text += f"{E_REVOKE} **ᴀʟʟ ʟɪɴᴋs ᴇxᴘɪʀᴇ ɪɴ 5 ᴍɪɴs**\n{T_DIVIDER}\n{SUPPORT_LINE}"
    await message.reply_text(result_text)
