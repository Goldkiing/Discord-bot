# commands/authorize_command.py

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

class AuthorizeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="authorize", description="Grant permission to a user.")
    @app_commands.describe(user="Select the user to authorize.")
    async def authorize(self, interaction: discord.Interaction, user: discord.User):
        settings = load_settings()
        author_id = interaction.user.id
        guild_owner_id = interaction.guild.owner_id if interaction.guild else None

        # Only the bot owner or server owner can authorize
        if author_id != OWNER_ID and author_id != guild_owner_id:
            await interaction.response.send_message("❌ Only the bot owner or server owner can authorize users.")
            return

        if user.id in settings["authorized_users"]:
            await interaction.response.send_message(f"ℹ️ {user.mention} is already authorized.")
        else:
            settings["authorized_users"].append(user.id)
            save_settings(settings)
            await interaction.response.send_message(f"✅ {user.mention} has been authorized.")

async def setup(bot):
    await bot.add_cog(AuthorizeCommand(bot))
