# arXiv Health Monitor

**Automatically curate, summarize, and publish medical & health research papers from arXiv**

AI-powered system that fetches the latest medical, healthcare, biosecurity, and health-related AI research from arXiv, uses AI to verify relevance, generates comprehensive summaries, and publishes everything to a beautiful searchable website.

[🌐 View Live Site](https://arxiv-health.org) | [📖 Quick Start Guide](QUICKSTART.md) | [💬 Discussions](https://github.com/BryanTegomoh/arxiv-health/discussions) | [🐛 Report Issue](https://github.com/BryanTegomoh/arxiv-health/issues)

---

## 🚀 New Here? Start with the [Quick Start Guide →](QUICKSTART.md)

The [QUICKSTART.md](QUICKSTART.md) has simple step-by-step instructions for running the site. This README contains detailed documentation.

## Features

- **Automated Fetching**: Pulls latest papers from arXiv based on medical/health keywords and categories
- **AI-Powered Curation**: Uses AI to verify relevance to medicine, health, biosecurity, and medical AI
- **Comprehensive Summaries**: Generates detailed summaries with:
  - 2-3 sentence overview
  - 5-7 key bullet points
  - Medical relevance analysis
  - Clinical impact assessment
  - Methodology & findings
  - Future directions
- **Multi-Provider AI Support**: Choose from:
  - **Gemini** (cheapest, recommended)
  - OpenAI GPT-4
  - Anthropic Claude
  - Grok
- **PDF Downloads**: Automatically downloads PDFs for offline reading
- **Beautiful Website**: Static site with:
  - Responsive design
  - Search functionality
  - Domain filtering
  - Sortable papers
  - Detailed paper pages
- **Incremental Updates**: Only processes new papers, tracks what's been added
- **GitHub Pages Ready**: Automatic deployment to GitHub Pages

## Medical Domains Covered

- Clinical Medicine (diagnosis, treatment, drugs)
- Public Health & Epidemiology
- Biosecurity & Pandemic Preparedness
- Medical AI/ML Applications
- Biotech & Computational Biology
- Oncology, Cardiology, Neurology
- Digital Health & Telemedicine
- And many more...

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/BryanTegomoh/arxiv-health.git
cd arxiv-health
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Requirements:**
- Python 3.8+
- pip

### 3. Configure API Keys

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API key. You only need ONE of these:

```bash
# For Gemini (Cheapest - Recommended)
GEMINI_API_KEY=your_gemini_key_here

# OR for OpenAI
OPENAI_API_KEY=your_openai_key_here

# OR for Claude
ANTHROPIC_API_KEY=your_claude_key_here

# OR for Grok
GROK_API_KEY=your_grok_key_here

# Set your preferred provider
AI_PROVIDER=gemini
```

**Getting API Keys:**
- **Gemini**: https://ai.google.dev/ (Free tier available)
- **OpenAI**: https://platform.openai.com/api-keys
- **Claude**: https://console.anthropic.com/
- **Grok**: https://x.ai/api

### 4. Run the System

```bash
python run.py
```

This will:
1. Fetch latest medical/health papers from arXiv
2. Check relevance using AI
3. Generate summaries for relevant papers
4. Download PDFs
5. Build the website in `docs/`

**First run will take 10-20 minutes depending on number of papers.**

### 5. View the Website Locally

Open `docs/index.html` in your browser to see the generated website.

## Usage

### Basic Usage

```bash
# Run with defaults (50 papers, 7 days back)
python run.py

# Fetch more papers
python run.py --max-results 100

# Look further back in time
python run.py --days-back 14

# Use a different AI provider
python run.py --provider openai

# Skip PDF downloads (faster)
python run.py --skip-download

# Rebuild website without fetching new papers
python run.py --rebuild-site
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--max-results` | Max papers to fetch per run | 50 |
| `--days-back` | Days to look back for papers | 7 |
| `--provider` | AI provider (gemini/openai/claude/grok) | gemini |
| `--skip-download` | Skip PDF downloads | False |
| `--rebuild-site` | Rebuild website from existing DB | False |

### Configuration

Edit `config.py` or `.env` to customize:

- Search keywords
- arXiv categories
- Relevance threshold
- Website title/description
- And more...

## Deploying to GitHub Pages

### One-Time Setup

1. **Enable GitHub Pages**:
   - Go to your repository settings
   - Navigate to "Pages"
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/docs`
   - Save

2. **Add API Keys to GitHub Secrets** (for automated updates):
   - Go to repository Settings → Secrets and variables → Actions
   - Add your API key (e.g., `GEMINI_API_KEY`)

3. **Enable GitHub Actions**:
   - The workflow in `.github/workflows/update-papers.yml` will automatically run daily
   - Or trigger manually from the Actions tab

### Manual Deployment

```bash
# Run the script
python run.py

# Commit and push
git add .
git commit -m "Update papers"
git push
```

Your site will be live at: `https://bryantegomoh.github.io/arxiv-health/`

## Project Structure

```
arxiv-health/
├── config.py              # Main configuration
├── run.py                 # Main execution script
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not in git)
├── .env.example          # Example environment file
│
├── src/
│   ├── arxiv_client.py   # arXiv API client
│   ├── ai_summarizer.py  # AI summarization
│   ├── database.py       # Paper storage
│   └── website_generator.py  # Static site generator
│
├── data/
│   ├── arxiv_health.json # Database of papers
│   └── papers/           # Downloaded PDFs
│
├── docs/                 # Generated website (GitHub Pages)
│   ├── index.html        # Homepage
│   ├── styles.css        # Stylesheet
│   ├── script.js         # Interactive features
│   └── papers/           # Individual paper pages
│
└── .github/
    └── workflows/
        └── update-papers.yml  # Automated updates
```

## How It Works

1. **Fetch**: Queries arXiv API for papers matching medical/health keywords and categories
2. **Filter**: AI checks each paper's relevance to medicine/health (configurable threshold)
3. **Summarize**: AI generates comprehensive summaries with key points, clinical impact, etc.
4. **Download**: Saves PDFs for offline access
5. **Store**: Adds to database (JSON) with all metadata and summaries
6. **Generate**: Creates static HTML website with search and filtering
7. **Publish**: Website deployed to GitHub Pages

## Cost Estimates

Using **Gemini** (recommended):
- **Free tier**: 15 requests/minute, 1500 requests/day
- **Paid**: ~$0.15 per 1M tokens
- **Estimated cost**: $0.01-0.05 per run (50 papers)

Using **OpenAI GPT-4o-mini**:
- ~$0.15 per 1M input tokens
- **Estimated cost**: $0.05-0.15 per run

Using **Grok**:
- ~$0.10 per 1M tokens
- **Estimated cost**: $0.03-0.10 per run

## Troubleshooting

### "API key not found"
- Make sure `.env` file exists
- Check that your API key is correctly set
- Ensure no extra spaces in the `.env` file

### "No papers found"
- arXiv might be temporarily down
- Try increasing `--days-back`
- Check your internet connection

### PDFs not downloading
- Use `--skip-download` to skip PDFs
- Check arXiv server status
- Some papers might not have PDFs available

### Website not updating on GitHub Pages
- Make sure you've enabled GitHub Pages in settings
- Check that you're deploying from `/docs` folder
- Wait 1-2 minutes for GitHub to rebuild

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.8+)

## Advanced Usage

### Adding Custom Keywords

Edit `config.py` and add to `HEALTH_KEYWORDS`:

```python
HEALTH_KEYWORDS = [
    # ... existing keywords ...
    "your custom keyword",
    "another keyword",
]
```

### Changing Relevance Threshold

In `config.py`:

```python
MIN_RELEVANCE_SCORE = 0.7  # 0.0 to 1.0 (higher = stricter)
```

### Using a Different Database

The system uses TinyDB (JSON) by default. To use SQLite or another database, modify `src/database.py`.

### Customizing the Website

- Edit templates in `src/website_generator.py`
- Modify CSS in the `_generate_css()` method
- Customize JavaScript in `_generate_javascript()` method

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use for any purpose

## Acknowledgments

- **arXiv** for providing open access to research
- **AI providers** for making advanced summarization possible
- **Python community** for excellent libraries

## Support

- [Open an issue](https://github.com/BryanTegomoh/arxiv-health/issues)
- [Discussions](https://github.com/BryanTegomoh/arxiv-health/discussions)

## Roadmap

- [ ] Email notifications for new papers
- [ ] RSS feed generation
- [ ] More advanced search (full-text)
- [ ] Paper recommendations
- [ ] Citation tracking
- [ ] Integration with reference managers
- [ ] Multi-language support

---

**Built with Python, arXiv API, and AI** | Made for researchers, clinicians, and health AI enthusiasts
