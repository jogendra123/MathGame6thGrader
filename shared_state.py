import os
import json
from threading import Lock

# Simple file-backed shared players storage. Atomic writes via temp+rename.
_lock = Lock()
STATE_FILE = os.path.join(os.path.dirname(__file__), 'shared_players.json')

def load_players():
    """Load players dict from disk. Returns empty dict if file missing or invalid."""
    try:
        if not os.path.exists(STATE_FILE):
            return {}
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure keys and simple types
            if isinstance(data, dict):
                return data
    except Exception:
        return {}
    return {}

def save_players(players: dict):
    """Save players dict to disk atomically."""
    tmp = STATE_FILE + '.tmp'
    with _lock:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(players, f, ensure_ascii=False, indent=2)
        try:
            os.replace(tmp, STATE_FILE)
        except Exception:
            # fallback
            os.remove(tmp) if os.path.exists(tmp) else None

def reset_players():
    save_players({})

def add_or_update_player(player_name: str, info: dict):
    players = load_players()
    players[player_name] = info
    save_players(players)
    return players
