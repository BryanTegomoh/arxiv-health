"""
Configuration management for arXiv Health Monitor
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
PAPERS_DIR = DATA_DIR / "papers"
WEBSITE_DIR = PROJECT_ROOT / "docs"
WEBSITE_PAPERS_DIR = WEBSITE_DIR / "papers"
DATABASE_PATH = DATA_DIR / "arxiv_health.json"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
PAPERS_DIR.mkdir(exist_ok=True)
WEBSITE_DIR.mkdir(exist_ok=True)
WEBSITE_PAPERS_DIR.mkdir(exist_ok=True)

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()

# arXiv Search Configuration
MAX_RESULTS_PER_RUN = int(os.getenv("MAX_RESULTS_PER_RUN", "50"))
DAYS_TO_LOOK_BACK = int(os.getenv("DAYS_TO_LOOK_BACK", "7"))

# Website Configuration
SITE_TITLE = os.getenv("SITE_TITLE", "Health AI Hub")
SITE_DESCRIPTION = os.getenv("SITE_DESCRIPTION", "AI-powered medical research discovery | Latest health AI papers from arXiv, curated daily")
SITE_TAGLINE = os.getenv("SITE_TAGLINE", "Your daily dose of cutting-edge health AI research")

# Social Media
TWITTER_HANDLE = os.getenv("TWITTER_HANDLE", "@ArXiv_Health")
SUBSTACK_URL = os.getenv("SUBSTACK_URL", "https://bryantegomoh.substack.com")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "bryan@arxiv-health.org")

# Feature Flags
ENABLE_DARK_MODE = os.getenv("ENABLE_DARK_MODE", "true").lower() == "true"
ENABLE_BOOKMARKS = os.getenv("ENABLE_BOOKMARKS", "true").lower() == "true"
ENABLE_TRENDING = os.getenv("ENABLE_TRENDING", "true").lower() == "true"
ENABLE_CHAT_ASSISTANT = os.getenv("ENABLE_CHAT_ASSISTANT", "true").lower() == "true"

# Medical/Health Keywords for arXiv search
HEALTH_KEYWORDS = [
    # Clinical Medicine
    "medicine", "clinical", "diagnosis", "treatment", "therapy", "drug", "pharmaceutical",
    "patient", "disease", "symptom", "medical imaging", "radiology", "pathology",

    # Public Health
    "public health", "epidemiology", "pandemic", "epidemic", "infectious disease",
    "vaccination", "immunization", "health policy", "healthcare",

    # Biosecurity
    "biosecurity", "biodefense", "bioterrorism", "pathogen", "outbreak",
    "surveillance", "early warning",

    # Medical AI/ML
    "medical AI", "healthcare AI", "clinical AI", "medical machine learning",
    "diagnostic AI", "predictive medicine", "precision medicine",
    "medical computer vision", "clinical NLP", "health informatics",

    # Biotech & Computational Biology
    "computational biology", "bioinformatics", "genomics", "proteomics",
    "drug discovery", "drug design", "molecular dynamics", "protein folding",
    "CRISPR", "gene therapy", "biomarker", "personalized medicine",

    # Specific Medical Fields
    "oncology", "cancer", "cardiology", "neurology", "psychiatry", "mental health",
    "diabetes", "Alzheimer", "Parkinson", "stroke", "sepsis", "COVID",
    "respiratory", "pulmonary", "cardiovascular", "neurological",

    # Medical Technologies
    "telemedicine", "digital health", "health monitoring", "wearable health",
    "medical robot", "surgical robot", "prosthetic", "medical device",

    # Healthcare Systems
    "hospital", "emergency", "ICU", "critical care", "primary care",
    "health record", "EHR", "clinical decision support"
]

# arXiv categories relevant to medical/health research
ARXIV_CATEGORIES = [
    "q-bio.*",  # Quantitative Biology (all subcategories)
    "cs.AI",    # Artificial Intelligence
    "cs.LG",    # Machine Learning
    "cs.CV",    # Computer Vision
    "cs.CL",    # Computation and Language
    "stat.ML",  # Machine Learning (statistics)
    "physics.med-ph",  # Medical Physics
]

# Validation settings
MIN_RELEVANCE_SCORE = 0.6  # Minimum AI relevance score (0-1) to include a paper
