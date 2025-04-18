# TOTP CLI - Terminal One-Time Password

A powerful, terminal-based One-Time Password (TOTP) manager written in Python. Designed for speed, security, and flexibility, with clipboard support, previews, and backup management.

![badge](https://img.shields.io/badge/made%20with-%F0%9F%90%8D%20Python-blue?style=flat-square)

## 🚀 Features

- Interactive TOTP selector using `fzf`
- Search by issuer or account name
- Auto-copy OTP to clipboard
- Preview OTP with color-coded expiration
- JSON-based secret storage
- Backup and restore support
- Terminal tab renaming

## 📦 Requirements

- Python 3.7+
- `fzf` installed and available in `$PATH`
- Python packages listed in `requirements.txt`
- A virtual environment (recommended)

## 🔧 Setup

```bash
# Clone your repo
cd ~/totp-cli
python3 -m venv env
source env/bin/activate
pip install -r src/requirements.txt
```

Make sure `fzf` is installed:
```bash
sudo apt install fzf   # Debian/Ubuntu
# or
brew install fzf       # macOS
```
If `fzf` is installed but not found by the script, you can set its path manually:

```bash
export FZF_PATH=$(dirname $(which fzf))
```


## 📁 File Structure

```
totp-cli/
├── env/                         # Python virtual environment
├── json/
│   ├── secrets.json             # Your TOTP secret file
│   └── backups/                 # Backup files
├── src/
│   ├── app.py                   # Main CLI entrypoint
│   ├── monitor.py               # Live TOTP code viewer
│   └── utils/                   # All internal modules
│       ├── preview.py           # Preview shown in fzf
│       ├── utils.py             # General utility functions
│       ├── commands.py          # Command handlers
│       └── protobuf/            # Google Authenticator QR importer
│           ├── extract_google_otp_from_qr.py
│           ├── migration_pb2.py
│           └── migration.proto
├── README.md
└── requirements.txt
```

## 🧪 Usage

```bash
# Run the OTP menu
sudo ./env/bin/python ./src/app.py
```

Or create an alias in your shell (bash/zsh):

```bash
alias otpcli='sudo ~/totp-cli/env/bin/python ~/totp-cli/src/app.py'
```

## 🛠️ Command Line Options

```bash
otpcli                          Interactive menu with all OTP accounts
otpcli <keyword>                Filter accounts by keyword(s), auto-copy if exactly one match

--help, -h                      Show this help message
--list                          Print all account labels
--stats                         Show stats per issuer
--edit                          Open the JSON file in default editor
--edit --backup                 Backup file before editing
--list-backups                  Show available backup files
--restore <FILENAME>            Restore a specific backup
```

## 🧾 Example Output

```
$ otpcli github

OTP code for GitHub (you@example.com): 123456
Valid for another 17 seconds (copied to clipboard)
```

```
$ otpcli --stats

TOTP CLI - Account Stats

Total accounts: 6
Unique issuers: 4

  GitHub              -> 2
  Google              -> 2
  AWS                 -> 1
  Bitwarden           -> 1
```

## 🔐 OTP Storage Format

All OTP secrets are stored in `json/secrets.json` as a list of dicts:

```json
[
  {
    "issuer": "GitHub",
    "name": "you@example.com",
    "secret": "JBSWY3DPEHPK3PXP"
  }
]
```

You can import from Google Authenticator QR via script.

## 🧯 Backup and Restore

- Backups are stored in `json/backups/`
- File format: `secrets.json.bak.YYYY-MM-DD_HH-MM-SS`

To restore:
```bash
otpcli --restore secrets.json.bak.2025-04-18_23-30-00
```

## 💙 License

MIT License. Built for personal security and terminal love. Contributions welcome!
