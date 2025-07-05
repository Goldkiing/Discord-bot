# commands/active_command.py

import discord
from discord import app_commands
from discord.ext import commands
from config import SETTINGS_FILE, OWNER_ID
import json
import os

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"authorized_users": [], "allowed_channels": []}

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

class ActiveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="active", description="Activate the bot in this channel.")
    async def activate(self, interaction: discord.Interaction):
        channel_id = interaction.channel.id
        user_id = interaction.user.id
        guild_owner_id = interaction.guild.owner_id if interaction.guild else None

        # Check authorization
        if user_id != OWNER_ID and user_id != guild_owner_id:
            await interaction.response.send_message("❌ Only the server owner or bot owner can use this.")
            return

        settings = load_settings()

        if channel_id not in settings["allowed_channels"]:
            settings["allowed_channels"].append(channel_id)
            save_settings(settings)
            await interaction.response.send_message("✅ This channel has been activated for bot use.")
        else:
            await interaction.response.send_message("ℹ️ This channel is already active.")

async def setup(bot):
    await bot.add_cog(ActiveCommand(bot))
