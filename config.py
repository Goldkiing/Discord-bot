import os  # لازم تستورد os لاستخدام os.getenv

# 🔐 Discord bot token (DO NOT share this)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") 

# 🌐 Optional external API URL (for future use)
API_URL = "https://your-glitch-api.glitch.me"  # optional, you can remove or update it

# 🎯 Similarity threshold for intent/sentence matching
SIMILARITY_THRESHOLD = 0.6

# 👑 Owner ID of the bot (from environment variable or default fallback)
OWNER_ID = int(os.getenv("OWNER_ID", "1052726688494141540"))

# ⚙️ Path to the settings file
SETTINGS_FILE = "settings.json"
