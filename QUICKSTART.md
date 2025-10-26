# Quick Start Guide - Health AI Hub

**How to run your arxiv-health.org site from scratch**

## 📋 Prerequisites

Before you start, make sure you have:
- Python 3.8 or higher installed
- Git installed
- A Gemini API key (free at https://ai.google.dev/)

## 🚀 Step-by-Step Instructions

### **Step 1: Open Terminal/Command Prompt**

Navigate to your project folder:
```bash
cd "c:\Users\bryan\OneDrive\Documents\xAI - Medicine\arxiv-health"
```

### **Step 2: Check Your Environment**

Make sure your `.env` file has your API key:
```bash
# The file should contain:
GEMINI_API_KEY=AIzaSyA8t_dvU5Yc3cfE2xb2_N1ytCxlpI2Fcf0
AI_PROVIDER=gemini
```

### **Step 3: Run the Site Generator**

**Option A: Full Update (Fetch New Papers)**
```bash
python run.py
```

This will:
- ✅ Fetch latest papers from arXiv (last 7 days)
- ✅ Check relevance with AI
- ✅ Generate summaries
- ✅ Download PDFs
- ✅ Build website in `docs/` folder
- ⏱️ Takes: 5-15 minutes depending on new papers

**Option B: Just Rebuild Website (No New Papers)**
```bash
python run.py --rebuild-site
```

This will:
- ✅ Rebuild website from existing database
- ⏱️ Takes: 10-30 seconds

**Option C: Fetch More Papers**
```bash
python run.py --max-results 100 --days-back 14
```

This will:
- ✅ Fetch up to 100 papers from last 14 days
- ⏱️ Takes: 15-30 minutes

### **Step 4: View Locally (Optional)**

Open the website in your browser:
```bash
# Windows
start docs/index.html

# Mac/Linux
open docs/index.html
```

### **Step 5: Deploy to GitHub Pages**

```bash
# Add all changes
git add .

# Commit with a message
git commit -m "Update papers 2025-10-26"

# Push to GitHub
git push origin main
```

⏱️ **Wait 2-3 minutes** for GitHub Pages to rebuild.

Your site will be live at: **https://arxiv-health.org**

---

## 🔄 Daily Routine

### What I Typically Do Each Day:

**1. Morning: Check for New Papers**
```bash
cd "c:\Users\bryan\OneDrive\Documents\xAI - Medicine\arxiv-health"
python run.py
```

**2. Review: Open Locally**
```bash
start docs/index.html
```
- Check what papers were added
- Make sure everything looks good

**3. Deploy: Push to GitHub**
```bash
git add .
git commit -m "Update papers $(date +%Y-%m-%d)"
git push
```

**4. Verify: Check Live Site**
- Visit https://arxiv-health.org
- Verify changes are live (wait 2-3 min)

---

## 📊 Common Commands

### Fetch and Deploy
```bash
# Full workflow in one go
python run.py && git add . && git commit -m "Update papers" && git push
```

### Check What's New
```bash
# See git status
git status

# See what changed
git diff docs/index.html
```

### Rebuild Only
```bash
# If you modified templates or styles
python run.py --rebuild-site
git add . && git commit -m "Update website design" && git push
```

### Fetch More Papers
```bash
# Get papers from last 2 weeks
python run.py --days-back 14 --max-results 100
```

---

## 🚨 Troubleshooting

### "Database initialized" but nothing happens
- **Check**: Do you have internet connection?
- **Fix**: Try again, arXiv might be slow

### "API key not found"
- **Check**: Is your `.env` file in the project root?
- **Fix**: Make sure it contains `GEMINI_API_KEY=your_key_here`

### Website not updating on GitHub Pages
- **Wait**: GitHub Pages takes 2-3 minutes to rebuild
- **Check**: Go to https://github.com/BryanTegomoh/arxiv-health/actions
- **Verify**: Make sure the latest workflow run succeeded

### "Import errors" or "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📅 Automation (Optional)

### Automated Daily Updates with GitHub Actions

Your site is **already set to update automatically** every day at midnight!

Check automation status:
1. Go to: https://github.com/BryanTegomoh/arxiv-health/actions
2. You should see daily "Update arXiv papers" runs
3. If needed, trigger manually by clicking "Run workflow"

**To disable automation:**
- Go to `.github/workflows/update-papers.yml`
- Comment out the `schedule:` section

**To change schedule:**
- Edit the cron expression in `update-papers.yml`
- Current: `0 0 * * *` (midnight daily)
- Example: `0 */6 * * *` (every 6 hours)

---

## 💡 Pro Tips

### Faster Runs
```bash
# Skip PDF downloads to run faster
python run.py --skip-download
```

### Test Changes Locally First
```bash
# Make changes to templates/styles
python run.py --rebuild-site
start docs/index.html
# Verify it looks good, then push
```

### Check Database
```bash
# See how many papers you have
python -c "from src.database import PaperDatabase; db = PaperDatabase(); print(f'Total papers: {len(db.get_all_papers())}')"
```

### View Logs
- Check `run.py` output for errors
- GitHub Actions logs: https://github.com/BryanTegomoh/arxiv-health/actions

---

## 🎯 Quick Reference Card

| Task | Command |
|------|---------|
| **Update papers** | `python run.py` |
| **Rebuild site** | `python run.py --rebuild-site` |
| **View locally** | `start docs/index.html` |
| **Deploy** | `git add . && git commit -m "Update" && git push` |
| **Check status** | `git status` |
| **Full workflow** | `python run.py && git add . && git commit -m "Update" && git push` |

---

## 📞 Need Help?

- **Documentation**: See full [README.md](README.md)
- **Issues**: https://github.com/BryanTegomoh/arxiv-health/issues
- **Discussions**: https://github.com/BryanTegomoh/arxiv-health/discussions
- **Contact**: bryan@arxiv-health.org

---

**Happy curating! 🔬📚✨**
