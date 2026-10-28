from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from app.discord.views.menu import MainMenuView


class DiscordCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="menu", description="Open the main CS2 community dashboard")
    async def menu(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "CS2 Community Dashboard",
            view=MainMenuView(),
            ephemeral=True,
        )

    @app_commands.command(name="verify", description="Begin Steam verification")
    async def verify(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Steam verification flow is available through the official OpenID flow. Connect the provider in production.",
            ephemeral=True,
        )

    @app_commands.command(name="refresh-premier", description="Refresh the member Premier rating")
    async def refresh_premier(self, interaction: discord.Interaction):
        await interaction.response.send_message("Premier refresh hook placeholder.", ephemeral=True)

    @app_commands.command(name="admin-status", description="View bot system status")
    @app_commands.checks.has_permissions(administrator=True)
    async def admin_status(self, interaction: discord.Interaction):
        await interaction.response.send_message("Bot status: running. Integrations: Steam/OIDC, FACEIT API, XPLAY provider abstraction ready.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(DiscordCommands(bot))
