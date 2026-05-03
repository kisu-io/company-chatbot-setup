# 🚀 Company AI Learning Chatbot Setup

Build an intelligent knowledge base chatbot using Lark Wiki (Feishu) and Hermes Agent.

**For:** Keezhu  
**Created:** 2026-05-03  
**Target:** New Mac Mini Setup

---

## 📋 What This Repo Contains

Complete setup package for building a company learning chatbot that:

- ✅ Syncs Lark Wiki docs to local markdown files
- ✅ Enables natural language Q&A via Hermes Agent
- ✅ Deploys to Telegram (or other platforms)
- ✅ Auto-syncs on schedule (optional cron)
- ✅ Uses Karpathy's LLM Wiki pattern for knowledge compounding

---

## ⚡ Quick Start

### 1. Get Lark API Credentials

Go to https://open.feishu.cn and create an app:
- Enable **Docs: Read** permission
- Copy **App ID** and **App Secret**

### 2. Configure Environment

```bash
cp .env.example .env
nano .env  # Fill in your LARK_APP_ID and LARK_APP_SECRET
```

### 3. Install Dependencies

```bash
pip3 install requests python-dotenv markdown
```

### 4. Run Sync

```bash
python3 scripts/sync-lark-wiki.py
```

### 5. Test with Hermes

```bash
hermes
# Ask: "What documents do we have about onboarding?"
```

---

## 📁 Project Structure

```
company-chatbot-setup/
├── index.html                 # Beautiful setup guide (this content as website)
├── README.md                  # This file
├── .env.example               # Environment template
├── config.yaml.example        # Hermes config template
├── scripts/
│   ├── sync-lark-wiki.py      # Main sync script
│   └── sync-lark-wiki.md      # Script documentation
└── company-wiki/
    ├── SCHEMA.md              # Wiki conventions
    ├── index.md               # Auto-generated document index
    ├── log.md                 # Auto-generated sync log
    └── raw/lark/              # Synced Lark docs (markdown)
```

---

## 🎯 Implementation Approaches

| Approach | Best For | Complexity |
|----------|----------|------------|
| **Local Sync** (this repo) | <100 docs, weekly updates | ⭐ Simple |
| **MCP Bridge** | 500+ docs, daily updates | ⭐⭐⭐ Advanced |
| **Hybrid** | 100-500 docs, weekly | ⭐⭐ Medium |

**Recommendation:** Start with Local Sync. You can add live MCP queries later.

---

## 🛠️ Setup Phases

### Phase 1: Install Hermes (15 min)
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes --version
```

### Phase 2: Copy Configs (10 min)
```bash
cp config.yaml.example ~/.hermes/config.yaml
cp .env.example ~/.hermes/.env
# Edit ~/.hermes/.env with credentials
```

### Phase 3: Install Deps (10 min)
```bash
pip3 install requests python-dotenv markdown
```

### Phase 4: Test Sync (20 min)
```bash
python3 scripts/sync-lark-wiki.py
```

### Phase 5: Test Queries (15 min)
```bash
hermes
# "What's in our company wiki about onboarding?"
```

### Phase 6: Deploy to Telegram (15 min)
```bash
hermes gateway start
```

### Phase 7: Auto-Sync (15 min, optional)
```bash
crontab -e
# Add: 0 */6 * * * python3 ~/projects/company-chatbot/scripts/sync-lark-wiki.py
```

---

## 🔐 Security Notes

- ⚠️ **Never commit `.env`** to git (it's in `.gitignore`)
- ⚠️ Store Lark credentials in 1Password/Keychain
- ⚠️ Use separate app credentials for production
- ⚠️ Review synced docs for sensitive content before deploying

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Auth failed | Check LARK_APP_ID/LARK_APP_SECRET in .env |
| Permission denied | Enable Docs:Read in Lark app permissions |
| Rate limited | Increase `time.sleep()` delays in sync script |
| Wiki not found | Set WIKI_PATH in ~/.hermes/.env |
| Hermes doesn't respond | Check `hermes gateway status` |

---

## 📖 Documentation

- **Setup Guide:** Open `index.html` in browser for beautiful interactive guide
- **Script Docs:** See `scripts/sync-lark-wiki.md` for detailed sync documentation
- **Wiki Schema:** See `company-wiki/SCHEMA.md` for knowledge base conventions

---

## 🎯 Success Criteria

By end of setup session, you should have:

- [ ] Hermes installed and running
- [ ] Lark credentials configured
- [ ] At least 10 docs synced to `company-wiki/raw/lark/`
- [ ] Working Q&A test (ask question, get answer)
- [ ] Telegram bot responding
- [ ] Cron job scheduled (optional)

---

## 📞 Support

This setup was prepared for Keezhu's company chatbot project. For issues:

1. Check `index.html` troubleshooting section
2. Review sync logs in `company-wiki/log.md`
3. Verify credentials in `~/.hermes/.env`

---

## 📄 License

MIT License — Use freely for your company projects.

---

**Estimated Setup Time:** 90-120 minutes  
**Difficulty:** Intermediate (requires API setup + Python)
