import sys
import os
import shutil
from utils.utils import (
    create_backup,
    restore_backup,
    list_backups,
    get_stats
)

def handle_commands(argv, accounts, json_path, backup_dir):
    if "--help" in argv or "-h" in argv:
        print("""
TOTP CLI - Terminal One-Time Password

Usage:
  otpcli                          Interactive menu with all OTP accounts
  otpcli <keyword>                Filter accounts by keyword(s), auto-copy if exactly one match

--help, -h                        Show this help message
--list                            Print all account labels
--stats                           Show stats per issuer
--edit                            Open the JSON file in default editor
--edit --backup                   Backup file before editing
--list-backups                    Show available backup files
--restore <FILENAME>              Restore a specific backup
""")
        sys.exit(0)

    if "--list" in argv:
        for acc in accounts:
            print(f"{acc['issuer']} ({acc['name']})")
        sys.exit(0)

    if "--stats" in argv:
        total, issuer_counts = get_stats(accounts)
        print("\nTOTP CLI - Account Stats\n")
        print(f"Total accounts: {total}")
        print(f"Unique issuers: {len(issuer_counts)}\n")
        max_len = max(len(issuer) for issuer in issuer_counts)
        for issuer, count in issuer_counts.most_common():
            print(f"  {issuer:<{max_len}} -> {count}")
        sys.exit(0)

    if "--edit" in argv:
        if "--backup" in argv:
            path = create_backup(json_path, backup_dir)
            print(f"Backup saved to: {path}")

        editor = os.environ.get("EDITOR")
        if not editor or not shutil.which(editor):
            for fallback in ["vi", "nano", "vim"]:
                if shutil.which(fallback):
                    editor = fallback
                    break
            else:
                print("No suitable editor found.")
                sys.exit(1)

        os.execvp(editor, [editor, json_path])

    if "--restore" in argv:
        try:
            index = argv.index("--restore")
            restore_name = argv[index + 1]
        except IndexError:
            print("Please provide the name of the backup file to restore.")
            sys.exit(1)

        restored = restore_backup(restore_name, backup_dir, json_path)
        print(f"Backup restored from: {restored}")
        sys.exit(0)

    if "--list-backups" in argv:
        print("\nAvailable backups:")
        backups = list_backups(backup_dir)
        if not backups:
            print("  (No backups found)")
        else:
            for b in backups:
                print(f"  {b}")
        sys.exit(0)
