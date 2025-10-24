# Setup Instructions - arXiv Health Monitor

## What You Have

A complete, working system that:
- ✅ Automatically fetches medical/health papers from arXiv
- ✅ Uses AI (Gemini) to verify relevance to medicine/health
- ✅ Generates comprehensive summaries with key points
- ✅ Downloads PDFs for offline reading
- ✅ Creates a beautiful searchable website
- ✅ Ready for GitHub Pages deployment
- ✅ Supports automated daily updates

## Your System is Ready!

Everything is configured and tested. Your Gemini API key is already set up.

## Next Steps

### Option 1: Run Immediately (Quick Test)

```bash
python run.py --max-results 10 --skip-download
```

This will:
- Fetch 10 recent medical papers
- Use AI to verify relevance
- Generate summaries
- Create the website
- Takes about 3-5 minutes

Then open `docs/index.html` in your browser to see the results!

### Option 2: Full Run (Recommended for First Real Use)

```bash
python run.py --max-results 50
```

This will:
- Fetch 50 recent medical papers
- Verify relevance with AI
- Generate comprehensive summaries
- Download PDFs
- Build the complete website
- Takes about 15-20 minutes

### Option 3: Use Quick Start Script

**Windows:**
```
quick-start.bat
```

**macOS/Linux:**
```bash
./quick-start.sh
```

## What Happens When You Run It?

1. **Fetches papers from arXiv** based on medical keywords
2. **AI checks each paper** to verify it's health-related
3. **Generates detailed summaries** including:
   - 2-3 sentence overview
   - 5-7 key bullet points
   - Medical relevance
   - Clinical impact
   - Keywords and domains
4. **Downloads PDFs** (optional, skip with `--skip-download`)
5. **Builds website** with search, filters, and paper pages
6. **Saves everything** to database for future runs

## File Structure

```
arxiv-health/
├── run.py                 # Main script - run this!
├── config.py             # Configuration (customize keywords here)
├── .env                  # Your API keys (already configured!)
│
├── data/                 # Generated data (git ignored)
│   ├── arxiv_health.json # Database of all papers
│   └── papers/           # Downloaded PDFs
│
├── docs/                 # Generated website (deploy this!)
│   ├── index.html        # Main page
│   └── papers/           # Individual paper pages
│
└── src/                  # Source code (don't need to touch)
    ├── arxiv_client.py   # Fetches from arXiv
    ├── ai_summarizer.py  # AI summarization
    ├── database.py       # Stores papers
    └── website_generator.py  # Builds website
```

## Deploying to GitHub Pages

### Step 1: Create GitHub Repository

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit: arXiv Health Monitor"

# Create repository on GitHub.com, then:
git remote add origin https://github.com/YOUR-USERNAME/arxiv-health.git
git branch -M main
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings**
3. Scroll to **Pages**
4. Under **Source**:
   - Branch: `main`
   - Folder: `/docs`
   - Click **Save**

5. Wait 1-2 minutes, then visit:
   `https://YOUR-USERNAME.github.io/arxiv-health/`

### Step 3: Set Up Automated Updates (Optional)

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `GEMINI_API_KEY`
4. Value: `AIzaSyDEEXXFDlpdQhnK7XaRxG2wRSyXAYQyS48`
5. Click **Add secret**

Now the system will automatically run daily at 6 AM UTC!

## Customization

### Change Keywords

Edit `config.py` to focus on specific medical areas:

```python
HEALTH_KEYWORDS = [
    # Add your research area keywords
    "cardiovascular",
    "neuroimaging",
    "precision oncology",
    # etc.
]
```

### Adjust Relevance Filter

In `config.py`:

```python
MIN_RELEVANCE_SCORE = 0.7  # Higher = stricter filtering
```

### Change How Many Papers to Fetch

In `.env`:

```
MAX_RESULTS_PER_RUN=50
DAYS_TO_LOOK_BACK=7
```

## Command Reference

```bash
# Basic run
python run.py

# Fetch more papers
python run.py --max-results 100

# Look further back
python run.py --days-back 14

# Skip PDFs (faster)
python run.py --skip-download

# Rebuild website only
python run.py --rebuild-site

# Use different AI
python run.py --provider openai
python run.py --provider claude
python run.py --provider grok

# Combine options
python run.py --max-results 30 --days-back 7 --skip-download
```

## Your API Key Status

✅ **Gemini API Key**: Configured and working!
- Key: `AIzaSyDEEXXFDlpdQhnK7XaRxG2wRSyXAYQyS48`
- Model: `gemini-2.5-flash`
- Cost: ~$0.01-0.05 per 50 papers (very cheap!)

If you want to add other providers later, edit `.env`:

```
OPENAI_API_KEY=sk-...        # Get from platform.openai.com
ANTHROPIC_API_KEY=sk-ant-... # Get from console.anthropic.com
GROK_API_KEY=gsk-...         # Get from x.ai
```

## Recommended First Run

I suggest starting with:

```bash
python run.py --max-results 20 --skip-download
```

This will:
- Process 20 papers (good sample size)
- Skip PDFs (much faster, ~5 minutes)
- Show you how it works
- Generate the website so you can see the results

Then if you like it, run the full version:

```bash
python run.py --max-results 50
```

## Monitoring Progress

The script shows real-time progress:
- Papers being fetched
- Relevance checks (with scores)
- Summary generation
- PDF downloads
- Website building

Example output:
```
[1/50] Predicting Protein-Nucleic Acid Flexibility...
  Checking medical/health relevance...
  [OK] Relevant! Score: 0.80
    Domains: Drug Discovery, Structural Biology
  Generating AI summary...
  Downloading PDF...
  [DONE] Paper processed and added to database
```

## Viewing Your Website

After running, simply open:
```
docs/index.html
```

The website includes:
- 📚 Full list of papers with summaries
- 🔍 Search functionality
- 🏷️ Filter by medical domain
- 📊 Sort by date/relevance
- 📄 Individual detail pages for each paper

## Incremental Updates

The system is smart about updates:
- Only processes NEW papers (checks database first)
- Safe to run multiple times
- Won't re-download existing PDFs
- Picks up where it left off

So you can run it daily or weekly without duplicates!

## Cost Estimate

With Gemini (your current setup):
- **Free tier**: 1500 requests/day
- **Typical usage**: 50 papers = ~100 requests
- **Cost**: Effectively free for daily use!

If you exceed free tier:
- **Paid cost**: ~$0.01-0.05 per 50 papers
- **Monthly budget**: $1-2 for daily updates

## Getting Help

- **Errors?** Check `USAGE.md` for troubleshooting
- **Questions?** See the detailed `README.md`
- **Issues?** Open an issue on GitHub

## Summary

You're all set! Here's what to do right now:

1. **Test run**: `python run.py --max-results 10 --skip-download`
2. **Open website**: `docs/index.html`
3. **If you like it**: Deploy to GitHub Pages
4. **Customize**: Edit keywords in `config.py` for your research area
5. **Automate**: Set up GitHub Actions for daily updates

The system is fully functional and ready to use. Everything has been tested and is working with your API key.

**Enjoy your automated medical research digest! 🔬📚🚀**

---

*Built with Python, arXiv API, Gemini AI, and GitHub Pages*
