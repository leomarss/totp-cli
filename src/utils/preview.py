import sys
import json
import pyotp
import time
import os

# ANSI colors
RESET = "\033[0m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BOLD = "\033[1m"

def get_color(seconds):
    if seconds > 20:
        return GREEN
    elif seconds > 10:
        return YELLOW
    else:
        return RED

selected = sys.argv[1]
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.abspath(os.path.join(script_dir, "../../json/otp_secrets.json"))

with open(json_path, "r") as f:
    accounts = json.load(f)

for acc in accounts:
    label = f"{acc['issuer']} ({acc['name']})"
    if label == selected:
        totp = pyotp.TOTP(acc["secret"])
        code = totp.now()
        seconds_left = 30 - int(time.time()) % 30
        color = get_color(seconds_left)

        print(f"{BOLD}Code:{RESET} {color}{code}{RESET} - {BOLD}Expires in:{RESET} {color}{seconds_left} seconds{RESET}")
        break
