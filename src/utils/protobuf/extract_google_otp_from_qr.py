import sys
import os
import base64
import migration_pb2
import json
import subprocess
from urllib.parse import unquote

if os.geteuid() != 0:
    print("This script must be run as root (use sudo).")
    sys.exit(1)

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "../../../json/secrets.json")

uri = input("Paste otpauth-migration string: ").strip()

data_b64 = uri.split("data=")[1]
data_b64 = unquote(data_b64)
missing_padding = len(data_b64) % 4
if missing_padding:
    data_b64 += '=' * (4 - missing_padding)

data_bytes = base64.urlsafe_b64decode(data_b64)

payload = migration_pb2.MigrationPayload()
payload.ParseFromString(data_bytes)

print("\n=== Accounts found ===")
accounts = []

for param in payload.otp_parameters:
    secret_b32 = base64.b32encode(param.secret).decode("utf-8").replace("=", "")
    issuer = param.issuer or "unknown"
    name = param.name
    print(f"{issuer} ({name}): {secret_b32}")
    accounts.append({
        "issuer": issuer,
        "name": name,
        "secret": secret_b32
    })

# create parent folder if needed
os.makedirs(os.path.dirname(json_path), exist_ok=True)

with open(json_path, "w") as f:
    json.dump(accounts, f, indent=2)

subprocess.run(["chown", "root:", json_path], check=True)
subprocess.run(["chmod", "600", json_path], check=True)

print("\nFile saved in json/secrets.json with secure permissions.")