from __future__ import annotations

import discord


class MainMenuView(discord.ui.View):
    def __init__(self, *, timeout: int = 180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="My Profile", style=discord.ButtonStyle.primary)
    async def profile_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "My profile is available from the personal profile panel. This is a placeholder view for the bot scaffold.",
            ephemeral=True,
        )

    @discord.ui.button(label="Premier Leaderboard", style=discord.ButtonStyle.secondary)
    async def premier_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Premier leaderboard placeholder.", ephemeral=True)

    @discord.ui.button(label="FACEIT Leaderboard", style=discord.ButtonStyle.secondary)
    async def faceit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("FACEIT leaderboard placeholder.", ephemeral=True)

    @discord.ui.button(label="1v1 Matchmaking", style=discord.ButtonStyle.green)
    async def queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Matchmaking placeholder.", ephemeral=True)

    @discord.ui.button(label="Player Statistics", style=discord.ButtonStyle.blurple)
    async def stats_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Player statistics placeholder.", ephemeral=True)

    @discord.ui.button(label="Rank History", style=discord.ButtonStyle.gray)
    async def history_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Rank history placeholder.", ephemeral=True)
