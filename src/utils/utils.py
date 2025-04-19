import subprocess
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
    choice = input("Do you already have the OTP migration string? [y/N] ").strip().lower()
    if choice != "y":
        print("Opening scanner using zbarimg...")
        path = input("Path to QR code image (e.g. /home/user/Downloads/otp.png): ").strip()
        if not os.path.exists(path):
            print("File not found. Please check the path and try again.")
            return
        if not os.path.isfile(path):
            print("Path is not a file. Please provide a valid file path.")
            return
        if not os.access(path, os.R_OK):
            print("File is not readable. Please check permissions.")
            return
        if not shutil.which("zbarimg"):
            print("zbarimg is not installed. Please install it first.")
            return
        print("Scanning QR code...")
        try:
            result = subprocess.run(
                ["zbarimg", "--raw", "--quiet", path],
                check=True, capture_output=True, text=True
            )
            scanned_uri = result.stdout.strip()
            print("\nScanned successfully. Importing...")

            os.environ["MIGRATION_STRING"] = scanned_uri
        except FileNotFoundError:
            print("'zbarimg' not found. Please install it first.")
            return
        except subprocess.CalledProcessError:
            print("Failed to read QR code using zbarimg.")
            return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    extract_path = os.path.join(script_dir, "protobuf", "extract_google_otp_from_qr.py")
    runpy.run_path(extract_path, run_name="__main__")
    del os.environ["MIGRATION_STRING"] # remove the environment variable after use just to be sure
    print("OTP secrets imported successfully.")