# helper.py

import os
import json

def load_json(path, default=None):
    """Safely load JSON from file or return default."""
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load {path}: {e}")
    return default if default is not None else {}

def save_json(path, data):
    """Save a Python dict to JSON file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Failed to save {path}: {e}")

def is_authorized(user_id: int, owner_id: int, settings: dict) -> bool:
    """Check if a user is authorized."""
    if user_id == owner_id:
        return True
    return user_id in settings.get("authorized_users", [])

def ensure_owner_in_auth(settings: dict, owner_id: int) -> bool:
    """Ensure the server owner is in the authorized list."""
    if owner_id not in settings["authorized_users"]:
        settings["authorized_users"].append(owner_id)
        return True
    return False
