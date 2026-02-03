import asyncio
from datetime import datetime
from pyrogram import Client
from pyrogram.enums import ParseMode
from config import *
from plugins import web_server
from aiohttp import web
from plugins.settings import auto_revoke_task

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="SuperLinkShareBot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={"root": "plugins"},
            bot_token=BOT_TOKEN,
            workers=40
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = me.username
        self.uptime = datetime.now()

        self.LOGGER(__name__).info(f"Bot started as @{self.username}")

        # Start background tasks
        asyncio.create_task(auto_revoke_task(self))

        # Web server
        try:
            app = web.AppRunner(await web_server())
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", PORT).start()
        except Exception as e:
            self.LOGGER(__name__).error(f"Failed to start web server: {e}")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

if __name__ == "__main__":
    Bot().run()
