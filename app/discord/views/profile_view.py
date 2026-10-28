from __future__ import annotations

import discord


class ProfileView(discord.ui.View):
    def __init__(self, *, timeout: int = 180):
        super().__init__(timeout=timeout)
        self.add_item(discord.ui.Button(label="Refresh Data", style=discord.ButtonStyle.primary, custom_id="refresh_profile"))
        self.add_item(discord.ui.Button(label="Link Steam", style=discord.ButtonStyle.secondary, custom_id="link_steam"))
        self.add_item(discord.ui.Button(label="Link FACEIT", style=discord.ButtonStyle.secondary, custom_id="link_faceit"))
        self.add_item(discord.ui.Button(label="Head-to-Head", style=discord.ButtonStyle.blurple, custom_id="h2h_profile"))
