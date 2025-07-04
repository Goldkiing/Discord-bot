from discord import app_commands, Interaction
from config import OWNER_ID, SETTINGS_FILE
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

def is_authorized(user_id, guild_owner_id):
    settings = load_settings()
    # أضف مالك السيرفر تلقائيًا
    if guild_owner_id not in settings["authorized_users"]:
        settings["authorized_users"].append(guild_owner_id)
        save_settings(settings)
    return user_id in settings["authorized_users"] or user_id == guild_owner_id or user_id == OWNER_ID

# يمكنك استخدام is_authorized في أي أمر آخر لاحقًا
