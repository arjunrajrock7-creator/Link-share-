import asyncio
import time
from datetime import datetime
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import BotCommand
from config import *
from plugins import web_server
from aiohttp import web
from plugins.settings import auto_revoke_task
from database.database import db
import logging

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="SuperLinkShareBot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={"root": "plugins"},
            bot_token=BOT_TOKEN,
            workers=TG_BOT_WORKERS,
            sleep_threshold=10 # Handle FloodWait automatically
        )
        self.LOGGER = LOGGER

    async def start(self):
        try:
            await super().start()

            # Initialize database indexes
            await db.initialize()

            me = await self.get_me()
            self.username = me.username
            self.uptime = datetime.now()

            self.LOGGER(__name__).info(f"Bot started as @{self.username}")

            # Automatic command registration
            await self.set_bot_commands([
                BotCommand("start", "Sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
                BotCommand("help", "Sʜᴏᴡ ʜᴇʟᴘ ᴍᴇɴᴜ"),
                BotCommand("channels", "Sʜᴏᴡ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs"),
                BotCommand("genlink", "Eɴᴄᴏᴅᴇ ᴇxᴛᴇʀɴᴀʟ ʟɪɴᴋ"),
                BotCommand("status", "Bᴏᴛ sʏsᴛᴇᴍ sᴛᴀᴛᴜs"),
                BotCommand("ping", "Bᴏᴛ ʟᴀᴛᴇɴᴄʏ")
            ])

            # Start background tasks
            asyncio.create_task(auto_revoke_task(self))

            # Web server for health checks (Render.com)
            try:
                app = web.AppRunner(await web_server())
                await app.setup()
                await web.TCPSite(app, "0.0.0.0", PORT).start()
                self.LOGGER(__name__).info(f"Health check server started on port {PORT}")
            except Exception as e:
                self.LOGGER(__name__).error(f"Failed to start web server: {e}")

        except Exception as e:
            self.LOGGER(__name__).critical(f"Bot failed to start: {e}")
            raise

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

if __name__ == "__main__":
    # Robust execution loop
    while True:
        try:
            Bot().run()
        except Exception as e:
            logging.error(f"Critical error in main loop: {e}")
            time.sleep(5) # Delay before restart
