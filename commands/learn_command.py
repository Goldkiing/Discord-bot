# commands/learn_command.py

import discord
from discord import app_commands
from discord.ext import commands
from learner import learn_paragraph
from config import SETTINGS_FILE
import json
import os

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"authorized_users": [], "allowed_channels": []}

class LearnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="learn", description="Teach the bot from a full paragraph.")
    @app_commands.describe(paragraph="Write a paragraph to learn from.")
    async def learn(self, interaction: discord.Interaction, paragraph: str):
        settings = load_settings()
        user_id = interaction.user.id
        channel_id = interaction.channel.id
        guild_owner_id = interaction.guild.owner_id if interaction.guild else None

        # Authorization Check
        if user_id not in settings["authorized_users"] and user_id != guild_owner_id:
            await interaction.response.send_message("❌ You are not authorized to use this command.")
            return

        # Channel Check
        if channel_id not in settings["allowed_channels"]:
            await interaction.response.send_message("❌ This channel is not activated. Use `/active` to activate.")
            return

        # Learn and respond
        learned = learn_paragraph(paragraph)
        result = "\n".join([f"✅ `{entry['sentence']}` → *(intent: {entry['intent']}, type: {entry['type']})*" for entry in learned])

        await interaction.response.send_message(f"🧠 Learned the following:\n{result}")

async def setup(bot):
    await bot.add_cog(LearnCommand(bot))
