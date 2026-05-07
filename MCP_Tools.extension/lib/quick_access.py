# -*- coding: utf-8 -*-
import os
import io
import json
from pyrevit import script

# Always resolve to an absolute path to avoid IronPython __file__ ambiguity
_here = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(_here, "quick_access_config.json")

def get_config():
    """Read the configuration from JSON file."""
    if os.path.exists(CONFIG_PATH):
        try:
            with io.open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("[quick_access] Failed to read config: {}".format(e))
    return {"pipe_types": [None, None, None, None, None]}

def save_config(config):
    """Save the configuration to JSON file."""
    try:
        with io.open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print("[quick_access] Failed to save config: {}".format(e))
        return False

def get_pipe_type_name(index):
    """Get the pipe type name at the given index (0-4). Returns None if empty."""
    config = get_config()
    types = config.get("pipe_types", [None] * 5)
    if 0 <= index < len(types):
        return types[index]
    return None

def update_ribbon_titles():
    """Update ribbon button titles based on current config."""
    config = get_config()
    types = config.get("pipe_types", [None] * 5)
    for i, name in enumerate(types):
        try:
            btn_id = "Pipe{}".format(i + 1)
            button = script.get_button(btn_id)
            if button:
                button.title = name if name else "Pipe {}".format(i + 1)
        except Exception:
            pass
