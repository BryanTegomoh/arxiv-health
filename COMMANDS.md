# arXiv Health Monitor - Command Reference

Quick reference for all available commands and options.

## Basic Commands

### Run with Defaults (50 papers, 7 days back)
```bash
python run.py
```

### Quick Test (Recommended First Run)
```bash
python run.py --max-results 10 --skip-download
```

### Full Run with PDFs
```bash
python run.py --max-results 50
```

## Command-Line Options

### --max-results N
Fetch maximum N papers per run
```bash
python run.py --max-results 100
```

### --days-back N
Look back N days for papers
```bash
python run.py --days-back 14
```

### --skip-download
Don't download PDFs (much faster)
```bash
python run.py --skip-download
```

### --provider PROVIDER
Use specific AI provider (gemini, openai, claude, grok)
```bash
python run.py --provider gemini
python run.py --provider openai
python run.py --provider claude
python run.py --provider grok
```

### --rebuild-site
Rebuild website without fetching new papers
```bash
python run.py --rebuild-site
```

## Combined Options

### Fast Daily Update
```bash
python run.py --max-results 30 --days-back 2 --skip-download
```

### Weekly Full Update
```bash
python run.py --max-results 100 --days-back 7
```

### Test Different AI Provider
```bash
python run.py --max-results 5 --provider openai --skip-download
```

### Rebuild Website Only
```bash
python run.py --rebuild-site
```

## Quick Start Scripts

### Windows
```cmd
quick-start.bat
```

### macOS/Linux
```bash
./quick-start.sh
```

## Git Commands

### Initial Setup
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/arxiv-health.git
git push -u origin main
```

### Daily Updates
```bash
git add .
git commit -m "Update papers $(date +'%Y-%m-%d')"
git push
```

### Quick Update
```bash
git add . && git commit -m "Update" && git push
```

## Python Package Management

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Upgrade Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Install Specific Package
```bash
pip install google-generativeai --upgrade
```

## Viewing Results

### Open Website Locally (Windows)
```cmd
start docs\index.html
```

### Open Website Locally (macOS)
```bash
open docs/index.html
```

### Open Website Locally (Linux)
```bash
xdg-open docs/index.html
```

## Configuration

### Edit Configuration
```bash
# Windows
notepad config.py

# macOS/Linux
nano config.py
# or
vim config.py
```

### Edit Environment Variables
```bash
# Windows
notepad .env

# macOS/Linux
nano .env
```

## Database Operations

### View Database (pretty print)
```bash
python -c "import json; print(json.dumps(json.load(open('data/arxiv_health.json')), indent=2))"
```

### Count Papers
```bash
python -c "from src.database import PaperDatabase; db = PaperDatabase(); print(f'Total papers: {db.get_statistics()[\"total_papers\"]}')"
```

### List Domains
```bash
python -c "from src.database import PaperDatabase; db = PaperDatabase(); stats = db.get_statistics(); print('\\n'.join([f'{d}: {c}' for d, c in stats['top_domains']]))"
```

## Troubleshooting Commands

### Check Python Version
```bash
python --version
```

### List Installed Packages
```bash
pip list
```

### Test Gemini API
```bash
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('API working!')"
```

### Check Available Gemini Models
```bash
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); models = genai.list_models(); [print(m.name) for m in models if 'generateContent' in m.supported_generation_methods]"
```

### Clean Restart
```bash
# Remove database and website
rm -rf data/arxiv_health.json docs/*.html docs/papers

# Re-run
python run.py
```

## GitHub Pages Commands

### Check Git Status
```bash
git status
```

### View Remote URL
```bash
git remote -v
```

### Force Push (careful!)
```bash
git push --force
```

### Pull Latest
```bash
git pull
```

## Development Commands

### Run Python Interactive with Project
```bash
python -i run.py
```

### Test ArXiv Client
```bash
python -c "from src.arxiv_client import ArxivHealthClient; client = ArxivHealthClient(); papers = client.fetch_recent_papers(max_results=5); print(f'Fetched {len(papers)} papers')"
```

### Test AI Summarizer
```bash
python -c "from src.ai_summarizer import AISummarizer; summarizer = AISummarizer(); print('Summarizer initialized')"
```

### Test Website Generator
```bash
python -c "from src.website_generator import WebsiteGenerator; gen = WebsiteGenerator(); print('Generator initialized')"
```

## Useful Aliases (Optional)

Add to your `.bashrc` or `.bash_profile`:

```bash
# Quick commands
alias arxiv-update='cd ~/arxiv-health && python run.py --max-results 30 --days-back 2'
alias arxiv-full='cd ~/arxiv-health && python run.py --max-results 100'
alias arxiv-test='cd ~/arxiv-health && python run.py --max-results 5 --skip-download'
alias arxiv-rebuild='cd ~/arxiv-health && python run.py --rebuild-site'
alias arxiv-view='open ~/arxiv-health/docs/index.html'
alias arxiv-deploy='cd ~/arxiv-health && git add . && git commit -m "Update $(date +%Y-%m-%d)" && git push'
```

Then use:
```bash
arxiv-update    # Daily update
arxiv-test      # Quick test
arxiv-view      # View website
arxiv-deploy    # Deploy to GitHub
```

## Scheduled Tasks

### Linux/macOS (cron)
```bash
# Edit crontab
crontab -e

# Add daily update at 7 AM
0 7 * * * cd ~/arxiv-health && python run.py --max-results 50
```

### Windows (Task Scheduler)
```cmd
# Create task
schtasks /create /tn "arXiv Health Update" /tr "python C:\path\to\arxiv-health\run.py" /sc daily /st 07:00
```

## Environment Variables

Set these in `.env`:

```bash
# Required
GEMINI_API_KEY=your_key_here

# Optional
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GROK_API_KEY=your_key_here

# Preferred provider
AI_PROVIDER=gemini

# Search parameters
MAX_RESULTS_PER_RUN=50
DAYS_TO_LOOK_BACK=7

# Website
SITE_TITLE=arXiv Health Monitor
SITE_DESCRIPTION=AI-curated medical research
```

## Most Common Workflows

### 1. Daily Quick Update
```bash
python run.py --max-results 20 --skip-download
```

### 2. Weekly Full Update
```bash
python run.py --max-results 100
```

### 3. Test Run
```bash
python run.py --max-results 5 --skip-download
```

### 4. Rebuild Website
```bash
python run.py --rebuild-site
```

### 5. Deploy to GitHub
```bash
git add .
git commit -m "Update papers"
git push
```

## Help

### Show Help Message
```bash
python run.py --help
```

### Version Info
```bash
python run.py --version  # (if implemented)
```

## Emergency Commands

### Stop Running Process
```
Ctrl+C
```

### Force Kill (if frozen)
```bash
# Find process
ps aux | grep run.py

# Kill it
kill -9 <PID>
```

### Reset Everything
```bash
# Backup database first!
cp data/arxiv_health.json data/backup.json

# Clean everything
rm -rf data/arxiv_health.json
rm -rf docs/*.html docs/papers/*

# Start fresh
python run.py --max-results 10
```

---

**Pro Tip**: Start with `python run.py --max-results 10 --skip-download` to test everything works, then scale up!
