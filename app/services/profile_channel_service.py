from __future__ import annotations

import discord


class ProfileChannelService:
    """Creates and maintains the persistent profile channel."""

    async def ensure_channel(self, guild: discord.Guild, channel_name: str = "🎮・my-profile") -> discord.TextChannel:
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if channel is None:
            channel = await guild.create_text_channel(channel_name)

        everyone = guild.default_role
        overwrites = {
            everyone: discord.PermissionOverwrite(send_messages=False, read_messages=True, add_reactions=True),
            guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True, manage_messages=True),
        }
        if channel.overwrites_for(everyone) != overwrites.get(everyone):
            await channel.set_permissions(everyone, send_messages=False, read_messages=True, add_reactions=True)
        return channel

    async def ensure_profile_message(self, channel: discord.TextChannel, content: str = "CS2 Profile") -> discord.Message | None:
        if not channel:
            return None
        async for msg in channel.history(limit=20):
            if msg.author == channel.guild.me and "CS2 Profile" in msg.content:
                return msg
        return await channel.send(content)
