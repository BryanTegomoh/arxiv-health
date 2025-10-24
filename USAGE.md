# arXiv Health Monitor - Usage Guide

## Quick Start (First Time Setup)

### Windows

1. Open Command Prompt or PowerShell in this directory
2. Run the quick start script:
   ```
   quick-start.bat
   ```

### macOS/Linux

1. Open Terminal in this directory
2. Run the quick start script:
   ```bash
   ./quick-start.sh
   ```

## Manual Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Make sure your `.env` file has your Gemini API key:

```
GEMINI_API_KEY=AIzaSyDEEXXFDlpdQhnK7XaRxG2wRSyXAYQyS48
AI_PROVIDER=gemini
```

### 3. Run the Script

Basic run (defaults: 50 papers, 7 days back):
```bash
python run.py
```

## Command-Line Options

### Fetch Fewer Papers (Faster Testing)
```bash
python run.py --max-results 10
```

### Look Further Back in Time
```bash
python run.py --days-back 14
```

### Skip PDF Downloads (Much Faster)
```bash
python run.py --skip-download
```

### Use Different AI Provider
```bash
# OpenAI
python run.py --provider openai

# Claude
python run.py --provider claude

# Grok
python run.py --provider grok
```

### Rebuild Website Without Fetching New Papers
```bash
python run.py --rebuild-site
```

### Combine Options
```bash
python run.py --max-results 20 --days-back 14 --skip-download
```

## Typical Workflows

### Daily Update (Recommended)
```bash
# Run every morning to get yesterday's papers
python run.py --max-results 30 --days-back 2
```

### Weekly Catchup
```bash
# Run weekly to catch all papers from the past week
python run.py --max-results 100 --days-back 7
```

### Quick Test
```bash
# Test with just a few papers, no PDF downloads
python run.py --max-results 5 --skip-download
```

### Full Archive Build
```bash
# Build comprehensive archive (will take hours!)
python run.py --max-results 500 --days-back 30
```

## Viewing Results

### Local Website
After running, open:
```
docs/index.html
```

The website includes:
- Full list of curated papers
- Search functionality
- Filter by medical domain
- Sort by date/relevance
- Individual paper detail pages

### Database
All papers are stored in JSON format:
```
data/arxiv_health.json
```

### PDFs
Downloaded PDFs are in:
```
data/papers/
```

## GitHub Pages Deployment

### One-Time Setup

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/docs`
   - Click Save

3. **Add API Key Secret** (for automated updates):
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `GEMINI_API_KEY`
   - Value: Your Gemini API key
   - Click "Add secret"

### Manual Updates

```bash
# Run the script
python run.py

# Commit and push
git add .
git commit -m "Update papers $(date +'%Y-%m-%d')"
git push
```

Wait 1-2 minutes for GitHub Pages to rebuild.

Your site will be at: `https://USERNAME.github.io/arxiv-health/`

### Automated Daily Updates

The GitHub Action in `.github/workflows/update-papers.yml` automatically:
- Runs every day at 6 AM UTC
- Fetches new papers
- Updates the website
- Commits and pushes changes

You can also trigger it manually:
- Go to Actions tab
- Click "Update arXiv Papers"
- Click "Run workflow"

## Configuration

### Customize Keywords

Edit `config.py` to add your own medical keywords:

```python
HEALTH_KEYWORDS = [
    # Add your custom keywords
    "genomics",
    "crispr",
    "immunotherapy",
    # ...
]
```

### Adjust Relevance Threshold

In `config.py`:

```python
MIN_RELEVANCE_SCORE = 0.7  # 0.0 to 1.0
# 0.6 = lenient (more papers)
# 0.8 = strict (fewer, more relevant papers)
```

### Change Search Parameters

In `.env`:

```
MAX_RESULTS_PER_RUN=50  # Number of papers to fetch
DAYS_TO_LOOK_BACK=7     # How far back to search
```

### Customize Website

Edit `config.py`:

```python
SITE_TITLE = "Your Custom Title"
SITE_DESCRIPTION = "Your custom description"
```

## Troubleshooting

### "API key not found"
- Make sure `.env` file exists
- Check that your API key is in the file
- No spaces around the `=` sign

### "No papers found"
- Try increasing `--days-back`
- Check arXiv server status
- Check your internet connection

### PDFs Not Downloading
- Use `--skip-download` to skip PDFs
- Check if arXiv is rate-limiting you
- Try running again later

### "models/gemini-xxx not found"
- Make sure you have the latest version:
  ```bash
  pip install google-generativeai --upgrade
  ```

### Website Not Updating on GitHub
- Wait 1-2 minutes after pushing
- Check Actions tab for errors
- Make sure GitHub Pages is enabled
- Verify you're deploying from `/docs` folder

## Performance & Costs

### Speed
- **5 papers**: ~2-3 minutes
- **50 papers**: ~15-20 minutes
- **100 papers**: ~30-40 minutes

(Without PDFs is about 3x faster)

### API Costs (Gemini)
- **Free tier**: 1500 requests/day (plenty!)
- **Paid tier**: ~$0.01-0.05 per run of 50 papers

### Storage
- Each paper PDF: ~1-5 MB
- Database: Negligible
- Website: ~1-2 MB

## Tips & Best Practices

### 1. Start Small
Run with `--max-results 10` first to test everything works

### 2. Skip PDFs Initially
Use `--skip-download` until you're sure the papers are relevant

### 3. Run Incrementally
The system tracks what's processed, so you can run multiple times safely

### 4. Check Relevance
Review the relevance scores and adjust `MIN_RELEVANCE_SCORE` if needed

### 5. Backup Database
The database is in `data/arxiv_health.json` - back it up periodically

### 6. Monitor Costs
Check your API usage at: https://ai.google.dev/

### 7. Customize for Your Needs
Edit keywords and categories in `config.py` to focus on your research area

## Advanced Usage

### Use Multiple AI Providers

Test which gives better results:

```bash
python run.py --provider gemini --max-results 5
python run.py --provider openai --max-results 5
python run.py --provider claude --max-results 5
```

### Export Data

The database is JSON, so you can easily export:

```python
import json
with open('data/arxiv_health.json') as f:
    data = json.load(f)
    papers = data['papers']
# Process papers...
```

### Custom Analysis

Build custom reports using the database:

```python
from src.database import PaperDatabase

db = PaperDatabase()
papers = db.get_all_papers()

# Filter by domain
oncology_papers = db.get_papers_by_domain('oncology')

# Search
covid_papers = db.search_papers('COVID')

# Statistics
stats = db.get_statistics()
print(f"Total papers: {stats['total_papers']}")
```

## Support

- **Issues**: https://github.com/yourusername/arxiv-health/issues
- **Documentation**: See README.md
- **arXiv API**: https://info.arxiv.org/help/api/
- **Gemini API**: https://ai.google.dev/

## Next Steps

1. Run your first update: `python run.py --max-results 10`
2. Check the website: `docs/index.html`
3. Deploy to GitHub Pages (follow instructions above)
4. Set up automated daily updates
5. Customize keywords for your research area
6. Share your site!

---

**Happy researching!** 🔬📚
