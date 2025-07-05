# main.py

import discord
from discord.ext import commands
import asyncio
import config

# ✅ Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# ✅ Create bot
bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ Events
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

    # Load command extensions (slash commands)
    await bot.load_extension("commands.learn_command")
    await bot.load_extension("commands.active_command")
    await bot.load_extension("commands.authorize_command")

# ✅ Run bot
if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)
