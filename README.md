from __future__ import annotations

import discord
from discord.ext import commands

from app.config import settings
from app.database import init_db

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True


class CS2Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self) -> None:
        await self.load_extension("app.discord.commands")
        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")


async def main() -> None:
    await init_db()
    bot = CS2Bot()
    await bot.start(settings.discord_token)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
