from __future__ import annotations

import asyncio
import logging

import discord
from discord.ext import commands

from app.config import settings
from app.database import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("cs2bot")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True


class CS2Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self) -> None:
        await self.load_extension("app.discord.commands")
        try:
            await self.tree.sync()
        except Exception:
            logger.exception("Could not sync application commands")

    async def on_ready(self) -> None:
        logger.info("Logged in as %s (%s)", self.user, self.user.id)


async def main() -> None:
    await init_db()
    bot = CS2Bot()
    await bot.start(settings.discord_token)


if __name__ == "__main__":
    asyncio.run(main())
