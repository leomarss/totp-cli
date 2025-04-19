import sys
import pyotp
import time
import json
import os
import shutil
import runpy
from datetime import datetime
from collections import Counter


def load_accounts(json_path):
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            return json.load(f)


def save_accounts(accounts, json_path):
    with open(json_path, "w") as f:
        json.dump(accounts, f, indent=2)


def generate_otp(secret):
    totp = pyotp.TOTP(secret)
    return totp.now(), 30 - int(time.time()) % 30


def create_backup(json_path, backup_dir):
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"secrets.json.bak.{timestamp}"
    backup_path = os.path.join(backup_dir, backup_name)
    shutil.copy2(json_path, backup_path)
    return backup_path


def list_backups(backup_dir):
    return sorted(
        f for f in os.listdir(backup_dir)
        if f.startswith("secrets.json.bak.")
    )


def restore_backup(backup_name, backup_dir, json_path):
    full_path = os.path.join(backup_dir, backup_name)
    shutil.copy2(full_path, json_path)
    return full_path


def get_stats(accounts):
    total = len(accounts)
    issuers = [acc.get("issuer", "Unknown") for acc in accounts]
    issuer_counts = Counter(issuers)
    return total, issuer_counts


def initialize_otp_setup():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    protobuf_dir = os.path.join(script_dir, "protobuf")
    sys.path.insert(0, protobuf_dir)

    extract_path = os.path.join(protobuf_dir, "extract_google_otp_from_qr.py")
    runpy.run_path(extract_path, run_name="__main__")