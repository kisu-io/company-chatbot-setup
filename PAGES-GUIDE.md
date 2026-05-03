# GitHub Pages Deployment Guide

## 🌐 Live Website URL

Once GitHub Pages is enabled, your setup guide will be available at:

**https://kisu-io.github.io/company-chatbot-setup/**

---

## 🔧 How to Enable GitHub Pages

### Option 1: Via GitHub Web UI (Recommended)

1. Go to: **https://github.com/kisu-io/company-chatbot-setup**
2. Click **Settings** tab
3. Click **Pages** in left sidebar
4. Under "Source", select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**
6. Wait 1-2 minutes for deployment
7. Your site will be live at the URL above

### Option 2: Via GitHub CLI

```bash
# Enable Pages (requires GitHub CLI v2.0+)
gh api \
  --method POST \
  --hostname github.com \
  --path /repos/kisu-io/company-chatbot-setup/pages \
  --field source='{"branch":"main","path":"/"}'
```

---

## 📊 Check Deployment Status

Visit: **https://github.com/kisu-io/company-chatbot-setup/deployments**

Or check Pages status:
```bash
gh api /repos/kisu-io/company-chatbot-setup/pages
```

---

## 🎨 What You'll See

The website includes:

- ✅ Interactive setup checklist (saves progress)
- ✅ Sticky navigation menu
- ✅ Timeline of setup phases
- ✅ File tree visualization
- ✅ Troubleshooting cards
- ✅ Comparison tables
- ✅ Responsive design (mobile-friendly)
- ✅ Dark theme with gradient accents

---

## 🔄 Auto-Updates

Every time you push to the `main` branch:
- GitHub Pages automatically rebuilds
- Changes appear within 1-2 minutes
- No manual deployment needed

---

## 📱 Access from Any Device

Once enabled, you can access the guide from:
- Desktop: https://kisu-io.github.io/company-chatbot-setup/
- Mobile: Same URL (responsive design)
- QR Code: Generate from the URL for easy sharing

---

## 🎯 Quick Test

After enabling Pages, open in browser:
```bash
open https://kisu-io.github.io/company-chatbot-setup/
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 Not Found | Wait 2-3 minutes, Pages needs time to build |
| Wrong content | Clear browser cache, hard refresh (Cmd+Shift+R) |
| Not updating | Check GitHub Actions for build errors |
| Custom domain wanted | Add CNAME file and configure in Settings → Pages |

---

## 📞 Need Help?

1. Check **Settings → Pages** for deployment status
2. View **Actions** tab for build logs
3. Verify `index.html` is in the root of the repo

---

**Repo:** https://github.com/kisu-io/company-chatbot-setup  
**Expected Pages URL:** https://kisu-io.github.io/company-chatbot-setup/
