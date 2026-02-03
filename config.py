import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---

def get_env(name: str, default: str = None, is_int: bool = False):
    value = os.environ.get(name, default)
    if is_int:
        try:
            return int(value) if value else 0
        except (ValueError, TypeError):
            return 0
    return value

# Telegram API credentials
API_ID = get_env("API_ID", "31355944", is_int=True)
API_HASH = get_env("API_HASH", "167e960d46363e3098f9c1fc78496adb")
BOT_TOKEN = get_env("BOT_TOKEN", "8592003417:AAGonw5Y61jFHS5bq0eWMuqDL7hY84jZ3uI")

# MongoDB credentials
MONGO_DB_URI = get_env("MONGO_DB_URI", "mongodb+srv://botskingdom2:t7ognZuINrNfH3tj@cluster0.ystdy4m.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = get_env("DB_NAME", "Cluster0")

# Owner and Admins
OWNER_ID = get_env("OWNER_ID", "8557029592", is_int=True)
ADMINS_STR = get_env("ADMINS", "8557029592")
ADMINS = [int(x) for x in ADMINS_STR.split()] if ADMINS_STR else []

# Optional Configurations
FSUB_ENABLED = get_env("FSUB_ENABLED", "True").lower() == "true"
LOG_CHANNEL = get_env("LOG_CHANNEL", "-1003840288506", is_int=True)
PORT = get_env("PORT", "8080", is_int=True)
TG_BOT_WORKERS = get_env("TG_BOT_WORKERS", "40", is_int=True)

# Bot info
BOT_USERNAME = get_env("BOT_USERNAME", "HT_LINKFORWARD_BOT")

# Branding & Support
OWNER_NAME = "⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡"
SUPPORT_ADMIN = "@ALONEKINGSTAR77"
SUPPORT_LINK = "https://t.me/ALONEKINGSTAR77"
START_IMG = "https://freeimage.host/i/fZZKTOl"

SUPPORT_LINE = f"<blockquote><b>ᴀɴʏ ɪssᴜᴇ ᴘʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ: {SUPPORT_ADMIN}</b></blockquote>"

# --- ANIME THEME UI ---
T_BANNER = f"✨ 𝗦𝗨𝗣𝗘𝗥 𝗟𝗜𝗡𝗞 𝗦𝗛𝗔𝗥𝗘 𝗕𝗬 {OWNER_NAME} ✨"
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

START_MSG = """
✨ **𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗟𝗶𝗻𝗸 𝗦𝗵𝗮𝗿𝗲 𝗕𝗼𝘁** ✨

🎋 **Hᴇʟʟᴏ {mention}**

📌 **Sᴇɴᴅ ᴍᴇ ᴀɴ Aɴɪᴍᴇ/Mᴏᴠɪᴇ/Sᴇʀɪᴇs ɴᴀᴍᴇ**
🔍 **I ᴡɪʟʟ sᴇᴀʀᴄʜ ғʀᴏᴍ ᴍʏ DB Cʜᴀɴɴᴇʟs**
🔗 **I ᴡɪʟʟ sᴇɴᴅ ᴊᴏɪɴ ʟɪɴᴋs / ᴘᴏsᴛ ʟɪɴᴋs ɪɴsᴛᴀɴᴛʟʏ**

⚡ **Fᴀsᴛ • Cʟᴇᴀɴ • Pʀᴇᴍɪᴜᴍ UI**
{divider}
{support}
"""

HELP_MSG = """
{banner}
{divider}
**ᴜsᴇʀ ᴄᴍᴅs:**
/start - sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
/help - sʜᴏᴡ ʜᴇʟᴘ ᴍᴇɴᴜ
/channels - sʜᴏᴡ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs
/genlink <ᴜʀʟ> - ᴇɴᴄᴏᴅᴇ ᴇxᴛᴇʀɴᴀʟ ʟɪɴᴋ

**ᴀᴅᴍɪɴ ᴄᴍᴅs:**
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
/ping - ʙᴏᴛ ʟᴀᴛᴇɴᴄʏ
{divider}
{support}
"""

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
