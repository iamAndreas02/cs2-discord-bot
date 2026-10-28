from __future__ import annotations

import discord


class MainMenuView(discord.ui.View):
    def __init__(self, *, timeout: int = 180):
        super().__init__(timeout=timeout)
        self.add_item(discord.ui.Button(label="My Profile", style=discord.ButtonStyle.primary, custom_id="profile_main"))
        self.add_item(discord.ui.Button(label="Premier Leaderboard", style=discord.ButtonStyle.secondary, custom_id="premier_lb"))
        self.add_item(discord.ui.Button(label="FACEIT Leaderboard", style=discord.ButtonStyle.secondary, custom_id="faceit_lb"))
        self.add_item(discord.ui.Button(label="1v1 Matchmaking", style=discord.ButtonStyle.green, custom_id="matchmaking_main"))
        self.add_item(discord.ui.Button(label="Player Statistics", style=discord.ButtonStyle.blurple, custom_id="stats_main"))
        self.add_item(discord.ui.Button(label="Rank History", style=discord.ButtonStyle.gray, custom_id="rank_history_main"))


class ProfileView(discord.ui.View):
    def __init__(self, *, timeout: int = 180):
        super().__init__(timeout=timeout)
        self.add_item(discord.ui.Button(label="Refresh Data", style=discord.ButtonStyle.primary, custom_id="refresh_profile"))
        self.add_item(discord.ui.Button(label="Link Steam", style=discord.ButtonStyle.secondary, custom_id="link_steam"))
        self.add_item(discord.ui.Button(label="Link FACEIT", style=discord.ButtonStyle.secondary, custom_id="link_faceit"))
        self.add_item(discord.ui.Button(label="Head-to-Head", style=discord.ButtonStyle.blurple, custom_id="h2h_profile"))
