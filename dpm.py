import os
import urllib.request
import json
import sys

# --- COLORS ---
COLOR_RE = "\033[0m"
COLOR_USER = "\033[92m"
COLOR_HOST = "\033[94m"
COLOR_ERR = "\033[91m"
COLOR_INFO = "\033[96m"

PLUGIN_DIR = os.path.expanduser("~/.config/daps/plugins/")
# Your repo URL
REPO_URL = "https://raw.githubusercontent.com/Stormzady/DAPS-Plugins/main/registry.json"

def run(args):
    if not args:
        print(f"{COLOR_INFO}DAPS Plugin Manager (dpm){COLOR_RE}")
        print("Usage: dpm [list | install | remove] <plugin_name>")
        return 1

    action = args[0]

    try:
        if action == "list":
            print(f"{COLOR_INFO}Fetching available plugins...{COLOR_RE}")
            with urllib.request.urlopen(REPO_URL) as response:
                registry = json.loads(response.read())
                print(f"{'Plugin':<15} | {'Description'}")
                print("-" * 40)
                for name, info in registry.items():
                    print(f"{COLOR_USER}{name:<15}{COLOR_RE} | {info['desc']}")
            return 0

        elif action == "install" and len(args) == 2:
            plugin_name = args[1]
            print(f"Installing {COLOR_USER}{plugin_name}{COLOR_RE}...")
            
            with urllib.request.urlopen(REPO_URL) as response:
                registry = json.loads(response.read())
            
            if plugin_name in registry:
                url = registry[plugin_name]['url']
                target_path = os.path.join(PLUGIN_DIR, f"{plugin_name}.py")
                urllib.request.urlretrieve(url, target_path)
                print(f"{COLOR_USER}Successfully installed {plugin_name}!{COLOR_RE}")
                print("Restart DAPS or call the command to use it.")
                return 0
            else:
                print(f"{COLOR_ERR}Error: Plugin '{plugin_name}' not found in registry.{COLOR_RE}")
                return 1

        elif action == "remove" and len(args) == 2:
            plugin_name = args[1]
            target_path = os.path.join(PLUGIN_DIR, f"{plugin_name}.py")
            if os.path.exists(target_path):
                os.remove(target_path)
                print(f"{COLOR_ERR}Removed {plugin_name}.{COLOR_RE}")
                return 0
            else:
                print(f"{COLOR_ERR}Plugin {plugin_name} is not installed.{COLOR_RE}")
                return 1
        
        else:
            print(f"{COLOR_ERR}Unknown action or invalid arguments.{COLOR_RE}")
            return 1

    except Exception as e:
        print(f"{COLOR_ERR}DPM Error: {e}{COLOR_RE}")
        return 1
