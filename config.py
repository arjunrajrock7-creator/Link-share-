import os
import logging
from logging.handlers import RotatingFileHandler

# --- CONFIGURATION ---

def get_env(name: str, default: str = None, is_int: bool = False):
    value = os.environ.get(name, default)
    if is_int:
        try:
            return int(value) if value else 0
        except ValueError:
            return 0
    return value

# Telegram API credentials
API_ID = get_env("API_ID", is_int=True)
API_HASH = get_env("API_HASH", "")
BOT_TOKEN = get_env("BOT_TOKEN", "")

# MongoDB credentials
MONGO_DB_URI = get_env("MONGO_DB_URI", "")
DB_NAME = get_env("DB_NAME", "SuperLinkShareBot")

# Owner and Admins
OWNER_ID = get_env("OWNER_ID", is_int=True)
# ADMINS can be a space-separated list of user IDs
ADMINS_STR = get_env("ADMINS", "")
ADMINS = [int(x) for x in ADMINS_STR.split()] if ADMINS_STR else []

# Optional Configurations
FSUB_ENABLED = get_env("FSUB_ENABLED", "True").lower() == "true"
LOG_CHANNEL = get_env("LOG_CHANNEL", "0", is_int=True)
PORT = get_env("PORT", "8080", is_int=True)

# Bot info
BOT_USERNAME = get_env("BOT_USERNAME", "") # Will be auto-fetched if not set

# --- ANIME THEME UI ---

# Unicode premium styles & emojis
T_BANNER = "✨ 𝗔𝗻𝗶𝗺𝗲 𝗟𝗶𝗻𝗸 𝗦𝗵𝗮𝗿𝗲𝗿 ✨"
T_DIVIDER = "━━━━━━━━━━━━━━━"
E_START = "🎋"
E_HELP = "📜"
E_LINK = "🔗"
E_REVOKE = "⏱️"
E_BULK = "📦"
E_CHANNELS = "📡"
E_ADMIN = "👨‍💻"
E_SUCCESS = "✅"
E_ERROR = "❌"
E_PRAY = "🙏"
E_STATS = "📊"
E_BROADCAST = "📢"
E_FSUB = "🔐"

# Anime themed messages
START_MSG = """
{banner}
{divider}
ʜᴇʟʟᴏ {mention} {pray}

ɪ ᴀᴍ ᴀ **sᴜᴘᴇʀ ʟɪɴᴋ sʜᴀʀᴇ ʙᴏᴛ**
ᴡɪᴛʜ ᴀɴɪᴍᴇ ᴛʜᴇᴍᴇᴅ ᴜɪ!

{link} **ɢᴇɴᴇʀᴀᴛᴇ sᴇᴄᴜʀᴇ ʟɪɴᴋs**
{revoke} **ᴀᴜᴛᴏ ʀᴇᴠᴏᴋᴇ ɪɴ 5 ᴍɪɴ**
{bulk} **ʙᴜʟᴋ sᴜᴘᴘᴏʀᴛᴇᴅ**
{divider}
"""

HELP_MSG = """
{banner}
{divider}
**ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs:**
/start - sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
/help - sʜᴏᴡ ʜᴇʟᴘ ᴍᴇɴᴜ
/channels - sʜᴏᴡ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs
/genlink <ᴜʀʟ> - ᴇɴᴄᴏᴅᴇ ᴇxᴛᴇʀɴᴀʟ ʟɪɴᴋ

**ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:**
/addchannel <ɪᴅ> - ᴀᴅᴅ ɴᴇᴡ ᴄʜᴀɴɴᴇʟ
/removechannel <ɪᴅ> - ʀᴇᴍᴏᴠᴇ ᴄʜᴀɴɴᴇʟ
/bulkgen - ɢᴇɴᴇʀᴀᴛᴇ ʟɪɴᴋs ɪɴ ʙᴜʟᴋ
/requeston <ɪᴅ> - ᴇɴᴀʙʟᴇ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ
/requestoff <ɪᴅ> - ᴅɪsᴀʙʟᴇ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ
/fsub_add <ɪᴅ> - ᴀᴅᴅ ғsᴜʙ ᴄʜᴀɴɴᴇʟ
/fsub_remove <ɪᴅ> - ʀᴇᴍᴏᴠᴇ ғsᴜʙ ᴄʜᴀɴɴᴇʟ
/addadmin <ɪᴅ> - ᴀᴅᴅ ɴᴇᴡ ᴀᴅᴍɪɴ
/rmadmin <ɪᴅ> - ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ
/admins - ʟɪsᴛ ᴀʟʟ ᴀᴅᴍɪɴs
/broadcast - sᴇɴᴅ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ
/stats - sʜᴏᴡ ʙᴏᴛ sᴛᴀᴛs
/status - ʙᴏᴛ sʏsᴛᴇᴍ sᴛᴀᴛᴜs
{divider}
"""

# --- LOGGING ---
LOG_FILE_NAME = "SuperLinkShareBot.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
