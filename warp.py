import os
import json

CONFIG_FILE = os.path.expanduser("~/.config/daps/config.json")

def run(args):
    # Load config to access bookmarks
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except:
        config = {}

    if "bookmarks" not in config:
        config["bookmarks"] = {}

    if not args:
        print("Usage: warp [add|remove|list] <name> | <bookmark_name>")
        return 1

    action = args[0]

    # List all bookmarks
    if action == "list":
        if not config["bookmarks"]:
            print("No bookmarks saved.")
        for name, path in config["bookmarks"].items():
            print(f"\033[92m{name}\033[0m -> {path}")
        return 0

    # Add current directory as bookmark
    elif action == "add" and len(args) == 2:
        name = args[1]
        config["bookmarks"][name] = os.getcwd()
        print(f"Saved bookmark: {name}")

    # Remove a bookmark
    elif action == "remove" and len(args) == 2:
        name = args[1]
        if name in config["bookmarks"]:
            del config["bookmarks"][name]
            print(f"Removed bookmark: {name}")
        else:
            print(f"Bookmark '{name}' not found.")

    # Teleport to bookmark
    elif action in config["bookmarks"]:
        target = config["bookmarks"][action]
        if os.path.exists(target):
            os.chdir(target)
            return 0
        else:
            print(f"Error: Path {target} no longer exists.")
            return 1
    else:
        print(f"Unknown bookmark: {action}")
        return 1

    # Save changes
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    return 0
