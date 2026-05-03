# 🚀 Tomorrow's Session — Quick Start Guide

**For:** Keezhu  
**Project:** Company AI Learning Chatbot  
**Machine:** New Mac Mini  
**Date:** 2026-05-04

---

## ⚡ 5-Minute Pre-Check

Before starting, make sure you have:

- [ ] Lark Open API credentials (App ID, App Secret)
- [ ] Telegram bot token (already configured)
- [ ] Internet connection
- [ ] ~2 hours of focused time

---

## 📋 Step-by-Step Session Plan

### Phase 1: Install Hermes (15 min)

```bash
# 1. Install Hermes Agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 2. Verify
hermes --version

# 3. Check Python version (need 3.10+)
python3 --version
```

**Expected output:** Hermes version number, Python 3.10+

---

### Phase 2: Copy Setup Files (10 min)

All files are already created in `~/projects/company-chatbot/`:

```bash
# Navigate to project
cd ~/projects/company-chatbot

# List what's ready
ls -la

# Copy config to Hermes
cp config.yaml.example ~/.hermes/config.yaml

# Copy env file and edit
cp .env.example ~/.hermes/.env
nano ~/.hermes/.env  # Fill in your Lark credentials
```

**Edit `~/.hermes/.env`:**
```bash
LARK_APP_ID=cli_your_actual_id
LARK_APP_SECRET=your_actual_secret
WIKI_PATH=~/projects/company-chatbot/company-wiki
```

---

### Phase 3: Install Dependencies (10 min)

```bash
# Python deps
pip3 install requests python-dotenv markdown

# Optional: Node.js for MCP (if needed later)
brew install node

# Verify Python deps
python3 -c "import requests, dotenv; print('OK')"
```

---

### Phase 4: Test Sync Script (20 min)

```bash
# Make script executable
chmod +x ~/projects/company-chatbot/scripts/sync-lark-wiki.py

# Run first sync
python3 ~/projects/company-chatbot/scripts/sync-lark-wiki.py
```

**Expected output:**
```
🚀 Starting Lark Wiki sync...
🔑 Got Lark access token
📚 Fetching document list...
📄 Found 47 documents
[1/47] Processing: Company Handbook
✅ Saved: Company Handbook
...
✅ Sync complete!
   New/updated: 47
   Skipped: 0
```

**Verify:**
```bash
# Check synced files
ls ~/projects/company-chatbot/company-wiki/raw/lark/

# Check index
cat ~/projects/company-chatbot/company-wiki/index.md
```

---

### Phase 5: Test Hermes Queries (15 min)

```bash
# Start Hermes session
hermes

# Test queries:
"What documents do we have about onboarding?"
"Show me the index of our company wiki"
"Find all engineering-related docs"
```

**Expected:** Hermes reads from `index.md` and `raw/lark/` files

---

### Phase 6: Deploy to Telegram (15 min)

```bash
# Start gateway (if not running)
hermes gateway start

# Test from Telegram
# Send: "What's in our company wiki?"
```

---

### Phase 7: Set Up Auto-Sync (Optional, 15 min)

```bash
# Add to crontab
crontab -e

# Add this line (sync every 6 hours)
0 */6 * * * python3 ~/projects/company-chatbot/scripts/sync-lark-wiki.py >> ~/.hermes/logs/lark-sync.log 2>&1

# Create log directory
mkdir -p ~/.hermes/logs
```

---

## 🎯 Success Checklist

By end of session, verify:

- [ ] Hermes installed and running
- [ ] `~/.hermes/.env` has Lark credentials
- [ ] Sync script runs without errors
- [ ] At least 10 docs synced to `company-wiki/raw/lark/`
- [ ] `index.md` exists and lists documents
- [ ] Hermes can answer questions about wiki content
- [ ] Telegram bot responds (if gateway running)
- [ ] Cron job scheduled (optional)

---

## 🐛 Common Issues & Fixes

### "Auth failed" error
```bash
# Check credentials
cat ~/.hermes/.env | grep LARK

# Verify in Lark developer console:
# https://open.feishu.cn → Your App → Credentials
```

### "Permission denied" from Lark API
```
# In Lark developer console:
# App → Permissions → Enable:
# - Docs: Read
# - Wiki: Read (if separate)
```

### Sync script not found
```bash
# Full path:
python3 ~/projects/company-chatbot/scripts/sync-lark-wiki.py

# Or copy to Hermes scripts:
cp ~/projects/company-chatbot/scripts/sync-lark-wiki.py ~/.hermes/scripts/
```

### Hermes doesn't find wiki
```bash
# Check WIKI_PATH in .env
cat ~/.hermes/.env | grep WIKI

# Should be:
WIKI_PATH=~/projects/company-chatbot/company-wiki

# Restart Hermes after changing .env
```

### Rate limiting from Lark
```python
# Already handled in script with time.sleep()
# If still hitting limits, increase delays:
# Line ~60: time.sleep(0.5) → time.sleep(2)
# Line ~130: time.sleep(1) → time.sleep(3)
```

---

## 📞 When You're Ready Tomorrow

Just message: **"Starting Mac Mini setup"** and I'll:

1. Walk through each phase with you
2. Debug any errors in real-time
3. Customize the setup based on your company's needs
4. Save the complete setup as a reusable skill

---

## 📁 Files Ready for You

All these files are already created:

```
~/projects/company-chatbot/
├── setup-checklist.md          # Detailed checklist
├── quick-start.md              # This file
├── .env.example                # Credential template
├── config.yaml.example         # Hermes config
├── scripts/
│   ├── sync-lark-wiki.py       # Sync script (executable)
│   └── sync-lark-wiki.md       # Documentation
└── company-wiki/
    ├── SCHEMA.md               # Wiki conventions
    ├── raw/lark/               # Synced docs (empty until first sync)
    ├── concepts/               # Curated concepts
    ├── learning-paths/         # Learning sequences
    └── queries/                # Q&A archive
```

---

## 🔐 Security Reminders

- [ ] Never commit `.env` to git
- [ ] Store Lark credentials in 1Password/Keychain
- [ ] Use separate app for production if needed
- [ ] Review synced docs for sensitive content

---

**Estimated total time:** 90-120 minutes  
**Difficulty:** Intermediate (requires API setup + Python)  
**Support:** Message me anytime during setup 👁️

_Good luck tomorrow! See you then._
