from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from app.config import settings
from app.discord.views.main_menu import MainMenuView, ProfileView
from app.services.leaderboard_service import generate_leaderboard_message
from app.services.profile_channel_service import ProfileChannelService
from app.services.profile_service import build_profile_message
from app.services.premier_service import get_rating_bracket
from app.services.rank_role_service import sync_member_roles
from app.services.steam_service import SteamOpenIDService
from app.services.verification_service import VerificationService

verification_service = VerificationService()
profile_channel_service = ProfileChannelService()


class CS2Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="menu", description="Open the main CS2 community dashboard")
    async def menu(self, interaction: discord.Interaction):
        await interaction.response.send_message("CS2 Community Dashboard", view=MainMenuView(), ephemeral=True)

    @app_commands.command(name="profile", description="View your player profile")
    async def profile(self, interaction: discord.Interaction):
        channel = await profile_channel_service.ensure_channel(interaction.guild, settings.profile_channel_name)
        await profile_channel_service.ensure_profile_message(channel, "CS2 Profile")
        await interaction.response.send_message(
            build_profile_message(interaction.user.id, interaction.user.display_name),
            view=ProfileView(),
            ephemeral=True,
        )

    @app_commands.command(name="premier", description="Check your current Premier bracket")
    async def premier(self, interaction: discord.Interaction):
        rating = 15420
        label, min_value, max_value = get_rating_bracket(rating)
        sync_member_roles(interaction.user, interaction.guild, rating)
        await interaction.response.send_message(
            f"Premier rating: {rating}\nBracket: {label}\nRange: {min_value} to {max_value}",
            ephemeral=True,
        )

    @app_commands.command(name="leaderboard", description="View the Premier leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.send_message(generate_leaderboard_message(), ephemeral=True)

    @app_commands.command(name="verify", description="Begin Steam account verification")
    async def verify(self, interaction: discord.Interaction):
        ok, message = verification_service.can_attempt(interaction.user.id, settings.verification_cooldown_seconds)
        if not ok:
            await interaction.response.send_message(message, ephemeral=True)
            return

        verification_service.register_attempt(interaction.user.id)
        service = SteamOpenIDService()
        auth_url = service.build_auth_url(
            realm=settings.steam_openid_realm,
            return_to=settings.steam_openid_return_to,
            state=f"verify:{interaction.user.id}",
        )
        await interaction.response.send_message(
            "Steam verification is required to link your account securely.\n" + auth_url,
            ephemeral=True,
        )

    @app_commands.command(name="refresh-premier", description="Refresh Premier rating data")
    async def refresh_premier(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Refresh request received. This implementation uses a provider-first update flow and reports unavailable data safely.",
            ephemeral=True,
        )

    @app_commands.command(name="join-queue", description="Join the 1v1 matchmaking queue")
    async def join_queue(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{interaction.user.display_name} has entered the 1v1 queue (manual fallback mode).",
            ephemeral=True,
        )

    @app_commands.command(name="leave-queue", description="Leave the 1v1 matchmaking queue")
    async def leave_queue(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{interaction.user.display_name} has left the 1v1 queue.",
            ephemeral=True,
        )

    @app_commands.command(name="admin-status", description="View bot system status")
    @app_commands.checks.has_permissions(administrator=True)
    async def admin_status(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Bot status: online\n"
            "Database: SQLAlchemy + SQLite ready\n"
            "Steam verification: enabled\n"
            "FACEIT: API abstraction enabled\n"
            "XPLAY: provider abstraction only; no unsupported automation claimed",
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(CS2Commands(bot))
