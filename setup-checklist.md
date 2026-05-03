# 🚀 Hermes + Lark Wiki Chatbot — Fresh Mac Setup

**Owner:** Keezhu  
**Project:** Company AI Learning Chatbot  
**Target Machine:** New Mac Mini (macOS)  
**Date Created:** 2026-05-03

---

## 📋 Pre-Session Checklist (Do Tonight)

### 1. Lark/Feishu Developer Access
- [ ] Go to https://open.feishu.cn
- [ ] Create a new enterprise app (or use existing)
- [ ] Enable these permissions:
  - `Docs: Read` (wiki access)
  - `Wiki: Read` (if separate)
  - `Contact: Read` (optional, for user lookup)
- [ ] Copy these credentials to a secure note:
  - `App ID` (cli_xxxxxxxxxxxxx)
  - `App Secret` (xxxxxxxxxxxxxxxx)
  - `Tenant Key` (if applicable)

### 2. Decide Your Approach
Based on your company size:

| Docs Count | Update Frequency | Recommended Approach |
|------------|-----------------|---------------------|
| < 100 | Weekly/Monthly | **Local Sync** (simplest) |
| 100-500 | Weekly | **Hybrid** (local + live fallback) |
| 500+ | Daily | **MCP Bridge** (always fresh) |

**Recommendation for most companies:** Start with **Local Sync**, add live queries later if needed.

### 3. Gather Existing Content Info
- [ ] How many wiki spaces/docs exist?
- [ ] List main categories (e.g., Onboarding, Product, Engineering, HR)
- [ ] Note any sensitive docs that should be excluded
- [ ] Identify 5-10 sample docs for testing

---

## 🛠️ Setup Steps (Tomorrow on New Mac)

### Phase 1: Hermes Agent Installation (30 min)

```bash
# 1. Install Hermes Agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 2. Verify installation
hermes --version

# 3. Configure Telegram (you already have this)
# Bot token will be needed

# 4. Set up model providers
hermes config set models.primary qwen3.5:397b
```

### Phase 2: Project Structure (15 min)

```bash
# Create project directory
mkdir -p ~/projects/company-chatbot
cd ~/projects/company-chatbot

# Create wiki structure
mkdir -p company-wiki/{raw/lark,concepts,learning-paths,queries,assets}

# Create scripts directory
mkdir -p ~/.hermes/scripts/
```

### Phase 3: Configuration Files (20 min)

Files you'll need to create:
- `~/.hermes/config.yaml` — Hermes config with wiki path
- `~/projects/company-chatbot/.env` — API credentials
- `~/.hermes/scripts/sync-lark-wiki.py` — Sync script
- `company-wiki/SCHEMA.md` — Wiki conventions

### Phase 4: Install Dependencies (10 min)

```bash
# Python dependencies
pip install requests python-dotenv markdown

# Optional: MCP SDK (if using MCP bridge)
pip install mcp

# Node.js (if using MCP servers via npx)
brew install node
```

### Phase 5: Test & Deploy (30 min)

```bash
# 1. Run initial sync
python ~/.hermes/scripts/sync-lark-wiki.py

# 2. Test a query
hermes "What's in our company wiki about onboarding?"

# 3. Deploy to Telegram
# Already configured — just start the gateway
hermes gateway start
```

---

## 📁 Files to Create Tomorrow

I'll prepare these for you in the next message:

1. **`config.yaml`** — Hermes configuration
2. **`sync-lark-wiki.py`** — Lark → local wiki sync script
3. **`SCHEMA.md`** — Wiki structure template
4. **`setup-checklist.md`** — This file (already done)
5. **`.env.example`** — Credential template

---

## ⚠️ Common Pitfalls & Solutions

| Problem | Solution |
|---------|----------|
| Lark API returns 403 | Check app permissions in developer console |
| Sync script fails on auth | Verify app_id/app_secret are correct |
| Wiki queries are slow | Add index.md, use search_files instead of full scans |
| Docs have complex formatting | Use web_extract for markdown conversion |
| Rate limiting from Lark | Add 2-second delays between API calls |
| Hermes doesn't find wiki | Set WIKI_PATH in ~/.hermes/.env |

---

## 🎯 Success Criteria

By end of session tomorrow, you should have:

- [ ] Hermes running on new Mac Mini
- [ ] Company wiki structure created
- [ ] At least 10 docs synced from Lark
- [ ] Working Q&A test (ask a question, get answer from wiki)
- [ ] Telegram bot responding with wiki knowledge
- [ ] Cron job scheduled for auto-sync (optional)

---

## 📞 When You're Ready Tomorrow

Just message: **"Ready to set up company chatbot"** and I'll:

1. Guide you through each phase step-by-step
2. Create all config files automatically
3. Debug any issues in real-time
4. Save the setup as a reusable skill for future projects

**Estimated total time:** 90-120 minutes for full setup

---

## 🔐 Security Notes

- Never commit `.env` files to git
- Store Lark credentials in 1Password/Keychain
- Use separate app credentials for dev vs production
- Consider read-only bot access for initial setup

---

_This checklist was prepared for Keezhu's company chatbot project. Save for tomorrow's session._
