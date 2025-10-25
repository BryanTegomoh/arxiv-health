"""
Static website generator for displaying curated papers
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from jinja2 import Template
import config


class WebsiteGenerator:
    """Generates static HTML website for papers"""

    def __init__(self, output_dir: str = None):
        """
        Initialize website generator

        Args:
            output_dir: Directory for generated website
        """
        self.output_dir = Path(output_dir) if output_dir else config.WEBSITE_DIR
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "papers").mkdir(exist_ok=True)

    def generate_website(self, papers: List[Dict], stats: Dict):
        """
        Generate complete website with all papers

        Args:
            papers: List of paper records
            stats: Database statistics
        """
        print("\nGenerating website...")

        # Generate individual paper pages
        for paper in papers:
            self._generate_paper_page(paper)

        # Generate index page
        self._generate_index_page(papers, stats)

        # Generate domain pages
        self._generate_domain_pages(papers, stats)

        # Copy static assets
        self._generate_css()
        self._generate_javascript()

        # Generate search index
        self._generate_search_index(papers)

        print(f"Website generated at: {self.output_dir}")
        print(f"  - Index: {self.output_dir / 'index.html'}")
        print(f"  - {len(papers)} paper pages")

    def _generate_index_page(self, papers: List[Dict], stats: Dict):
        """Generate main index page"""
        # Calculate weekly statistics
        from src.utils import get_weekly_stats, format_domain_summary
        weekly_stats = get_weekly_stats(papers)
        total_citations = sum(paper.get('citation_count', 0) for paper in papers)

        template = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ site_title }}</title>
    <meta name="description" content="{{ site_description }}">
    <meta name="keywords" content="medical AI, health AI, arXiv, research papers, machine learning, healthcare">
    <meta name="author" content="Health AI Hub">

    <!-- Open Graph / Social Media -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{{ site_title }}">
    <meta property="og:description" content="{{ site_description }}">
    <meta property="og:url" content="https://arxiv-health.org">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="{{ twitter_handle }}">

    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>{{ site_title }}</h1>
            <p class="tagline">{{ tagline }}</p>

            <!-- Weekly Activity Hero Section -->
            <div class="weekly-hero">
                <h2>This Week's Activity</h2>
                <div class="hero-stats">
                    <div class="hero-stat-item">
                        <div class="hero-stat-number">{{ weekly_stats.papers_this_week }}</div>
                        <div class="hero-stat-label">New Papers</div>
                    </div>
                    <div class="hero-stat-item">
                        <div class="hero-stat-number">{{ stats.total_papers }}</div>
                        <div class="hero-stat-label">Total Curated</div>
                    </div>
                    <div class="hero-stat-item">
                        <div class="hero-stat-number">{{ stats.domains|length }}</div>
                        <div class="hero-stat-label">Medical Domains</div>
                    </div>
                </div>
                {% if weekly_stats.top_domains %}
                <div class="hottest-domains">
                    <strong>Hottest domains this week:</strong> {{ weekly_domain_summary }}
                </div>
                {% endif %}
            </div>
        </div>
    </header>

    <nav class="container">
        <div class="nav-tools">
            <div class="search-box">
                <input type="text" id="search" placeholder="🔍 Search papers by title, author, keywords, or domain...">
            </div>
            <div class="filters">
                <div class="filter-group">
                    <label>Sort by:</label>
                    <select id="sort-select">
                        <option value="date">Newest First</option>
                        <option value="relevance">Relevance Score</option>
                        <option value="citations">Most Cited</option>
                        <option value="title">Title A-Z</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Domain:</label>
                    <select id="domain-filter">
                        <option value="">All Domains</option>
                        {% for domain, count in stats.top_domains %}
                        <option value="{{ domain }}">{{ domain|title }} ({{ count }})</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="filter-group">
                    <label>Author:</label>
                    <input type="text" id="author-filter" placeholder="Filter by author">
                </div>
            </div>
        </div>
    </nav>

    <main class="container">
        <div class="papers-grid" id="papers-container">
            {% for paper in papers %}
            <article class="paper-card"
                     data-arxiv-id="{{ paper.arxiv_id }}"
                     data-domains="{{ paper.medical_domains|join(',') }}"
                     data-keywords="{{ paper.keywords|join(',') }}"
                     data-authors="{{ paper.authors|join(',') }}">

                <div class="paper-header">
                    <h2 class="paper-title">
                        <a href="papers/{{ paper.arxiv_id|replace('/', '_') }}.html">{{ paper.title }}</a>
                    </h2>
                    <div class="paper-meta">
                        <span class="date">📅 {{ paper.published[:10] }}</span>
                        <span class="relevance">⭐ {{ "%.2f"|format(paper.relevance_score) }}</span>
                        {% if paper.citation_count %}
                        <span class="citations">📖 {{ paper.citation_count }} citations</span>
                        {% endif %}
                        <span class="category">📂 {{ paper.primary_category }}</span>
                    </div>
                </div>

                <div class="paper-authors">
                    <strong>Authors:</strong> {{ paper.authors[:3]|join(', ') }}{% if paper.authors|length > 3 %} et al.{% endif %}
                </div>

                <div class="paper-summary">
                    {{ paper.summary }}
                </div>

                <div class="paper-domains">
                    {% for domain in paper.medical_domains[:5] %}
                    <span class="domain-tag">{{ domain }}</span>
                    {% endfor %}
                </div>

                <div class="paper-links">
                    <a href="papers/{{ paper.arxiv_id|replace('/', '_') }}.html" class="btn btn-primary">Read Full Summary</a>
                    <a href="{{ paper.arxiv_url }}" target="_blank" class="btn btn-secondary">arXiv</a>
                    <a href="{{ paper.pdf_url }}" target="_blank" class="btn btn-secondary">PDF</a>
                    <button class="export-btn" data-paper-id="{{ paper.arxiv_id }}" title="Export Citation">
                        📚 Cite
                    </button>
                </div>
            </article>
            {% endfor %}
        </div>
    </main>

    <footer class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h3>{{ site_title }}</h3>
                <p>{{ tagline }}</p>
                <p>Curated by <a href="mailto:{{ contact_email }}">Bryan Tegomoh</a></p>
                <p>Powered by Gemini AI | Updated Daily</p>
            </div>
            <div class="footer-section">
                <h3>About</h3>
                <p><a href="about.html">Methodology</a></p>
                <p><a href="https://github.com/BryanTegomoh/arxiv-health" target="_blank">Open Source</a></p>
                <p><a href="https://github.com/BryanTegomoh/arxiv-health/discussions" target="_blank">Discussions</a></p>
            </div>
            <div class="footer-section">
                <h3>Connect</h3>
                <p><a href="https://twitter.com/{{ twitter_handle[1:] }}" target="_blank">Twitter/X</a></p>
                <p><a href="{{ substack_url }}" target="_blank">Newsletter</a></p>
                <p><a href="https://arxiv.org" target="_blank">arXiv.org</a></p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2025 Health AI Hub | Last updated: {{ last_updated }}</p>
        </div>
    </footer>

    <!-- Export Modal -->
    <div id="export-modal" class="modal">
        <div class="modal-content">
            <span class="modal-close">&times;</span>
            <h2>Export Citation</h2>
            <div class="export-options">
                <button class="export-format" data-format="bibtex">BibTeX</button>
                <button class="export-format" data-format="ris">RIS (EndNote/Mendeley)</button>
                <button class="export-format" data-format="plain">Plain Text</button>
            </div>
            <textarea id="citation-output" readonly></textarea>
            <button id="copy-citation" class="btn btn-primary">Copy to Clipboard</button>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
""")

        # Format weekly domain summary
        from src.utils import format_domain_summary
        weekly_domain_summary = format_domain_summary(weekly_stats['top_domains'])

        html = template.render(
            site_title=config.SITE_TITLE,
            site_description=config.SITE_DESCRIPTION,
            tagline=config.SITE_DESCRIPTION,
            twitter_handle=config.TWITTER_HANDLE,
            substack_url=config.SUBSTACK_URL,
            contact_email=config.CONTACT_EMAIL,
            papers=papers,
            stats=stats,
            weekly_stats=weekly_stats,
            weekly_domain_summary=weekly_domain_summary,
            total_citations=total_citations,
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        (self.output_dir / "index.html").write_text(html, encoding='utf-8')

    def _generate_paper_page(self, paper: Dict):
        """Generate individual paper detail page"""
        template = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ paper.title }} - {{ site_title }}</title>
    <meta name="description" content="{{ paper.summary[:160] }}">
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png">
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <header>
        <div class="container">
            <nav class="breadcrumb">
                <a href="../index.html">← Back to all papers</a>
            </nav>
        </div>
    </header>

    <main class="container paper-detail">
        <article>
            <h1>{{ paper.title }}</h1>

            <div class="paper-metadata">
                <div class="meta-row">
                    <strong>arXiv ID:</strong> <a href="{{ paper.arxiv_url }}" target="_blank">{{ paper.arxiv_id }}</a>
                </div>
                <div class="meta-row">
                    <strong>Published:</strong> {{ paper.published[:10] }}
                </div>
                <div class="meta-row">
                    <strong>Authors:</strong> {{ paper.authors|join(', ') }}
                </div>
                <div class="meta-row">
                    <strong>Categories:</strong> {{ paper.categories|join(', ') }}
                </div>
                <div class="meta-row">
                    <strong>Relevance Score:</strong> {{ "%.2f"|format(paper.relevance_score) }} / 1.00
                </div>
            </div>

            <div class="action-buttons">
                <a href="{{ paper.arxiv_url }}" target="_blank" class="btn btn-primary">View on arXiv</a>
                <a href="{{ paper.pdf_url }}" target="_blank" class="btn btn-primary">Download PDF</a>
            </div>

            <section class="paper-section">
                <h2>Summary</h2>
                <p class="summary-text">{{ paper.summary }}</p>
            </section>

            <section class="paper-section">
                <h2>Medical Relevance</h2>
                <p>{{ paper.medical_relevance }}</p>
            </section>

            {% if paper.ai_health_application %}
            <section class="paper-section">
                <h2>AI Health Application</h2>
                <p>{{ paper.ai_health_application }}</p>
            </section>
            {% endif %}

            <section class="paper-section">
                <h2>Key Points</h2>
                <ul class="key-points">
                    {% for point in paper.key_points %}
                    <li>{{ point }}</li>
                    {% endfor %}
                </ul>
            </section>

            <div class="two-column">
                <section class="paper-section">
                    <h2>Methodology</h2>
                    <p>{{ paper.methodology }}</p>
                </section>

                <section class="paper-section">
                    <h2>Key Findings</h2>
                    <p>{{ paper.key_findings }}</p>
                </section>
            </div>

            <section class="paper-section">
                <h2>Clinical Impact</h2>
                <p>{{ paper.clinical_impact }}</p>
            </section>

            {% if paper.limitations %}
            <section class="paper-section">
                <h2>Limitations</h2>
                <p>{{ paper.limitations }}</p>
            </section>
            {% endif %}

            {% if paper.future_directions %}
            <section class="paper-section">
                <h2>Future Directions</h2>
                <p>{{ paper.future_directions }}</p>
            </section>
            {% endif %}

            <section class="paper-section">
                <h2>Medical Domains</h2>
                <div class="tags">
                    {% for domain in paper.medical_domains %}
                    <span class="tag">{{ domain }}</span>
                    {% endfor %}
                </div>
            </section>

            <section class="paper-section">
                <h2>Keywords</h2>
                <div class="tags">
                    {% for keyword in paper.keywords %}
                    <span class="tag tag-keyword">{{ keyword }}</span>
                    {% endfor %}
                </div>
            </section>

            <section class="paper-section">
                <h2>Abstract</h2>
                <p class="abstract">{{ paper.abstract }}</p>
            </section>

            {% if paper.comment %}
            <section class="paper-section">
                <h2>Comments</h2>
                <p>{{ paper.comment }}</p>
            </section>
            {% endif %}

            {% if paper.journal_ref %}
            <section class="paper-section">
                <h2>Journal Reference</h2>
                <p>{{ paper.journal_ref }}</p>
            </section>
            {% endif %}
        </article>
    </main>

    <footer class="container">
        <p><a href="../index.html">← Back to all papers</a></p>
    </footer>
</body>
</html>
""")

        html = template.render(
            paper=paper,
            site_title=config.SITE_TITLE
        )

        filename = f"{paper['arxiv_id'].replace('/', '_')}.html"
        (self.output_dir / "papers" / filename).write_text(html, encoding='utf-8')

    def _generate_domain_pages(self, papers: List[Dict], stats: Dict):
        """Generate pages for each medical domain"""
        # This could be expanded to create separate pages per domain
        pass

    def _generate_css(self):
        """Generate CSS stylesheet"""
        css = """
/* arXiv Health Monitor - Styles */

:root {
    --primary-color: #14b8a6;
    --secondary-color: #06b6d4;
    --accent-color: #10b981;
    --success-color: #059669;
    --bg-color: #f8fafc;
    --card-bg: #ffffff;
    --text-color: #1e293b;
    --text-muted: #64748b;
    --border-color: #e2e8f0;
    --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}


* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 2rem 0;
    margin-bottom: 2rem;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.tagline {
    font-size: 1.1rem;
    opacity: 0.9;
    margin-bottom: 1rem;
}

.stats {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.stat-item {
    background: rgba(255, 255, 255, 0.2);
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.95rem;
}

/* Navigation */
nav {
    margin-bottom: 2rem;
}

.search-box {
    margin-bottom: 1rem;
}

#search {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    border: 2px solid var(--border-color);
    border-radius: 0.5rem;
    transition: border-color 0.3s;
}

#search:focus {
    outline: none;
    border-color: var(--primary-color);
}

.filters {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    align-items: center;
}

.filters label {
    font-weight: 600;
    color: var(--text-muted);
}

.filters select {
    padding: 0.5rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: 0.95rem;
}

/* Papers Grid */
.papers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
}

.paper-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}

.paper-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.paper-title {
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
    line-height: 1.4;
}

.paper-title a {
    color: var(--text-color);
    text-decoration: none;
}

.paper-title a:hover {
    color: var(--primary-color);
}

.paper-meta {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
}

.paper-authors {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
}

.paper-summary {
    margin: 1rem 0;
    line-height: 1.6;
    color: var(--text-color);
}

.paper-domains {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 1rem 0;
}

.domain-tag {
    background: var(--bg-color);
    color: var(--primary-color);
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.85rem;
    font-weight: 500;
}

.paper-links {
    display: flex;
    gap: 0.75rem;
    margin-top: 1rem;
}

.btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
    transition: all 0.2s;
    border: none;
    cursor: pointer;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: #1d4ed8;
}

.btn-secondary {
    background: var(--bg-color);
    color: var(--text-color);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--border-color);
}

/* Paper Detail Page */
.paper-detail {
    max-width: 900px;
}

.breadcrumb {
    padding: 1rem 0;
}

.breadcrumb a {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
}

.paper-detail h1 {
    font-size: 2rem;
    margin-bottom: 1.5rem;
    line-height: 1.3;
}

.paper-metadata {
    background: var(--bg-color);
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
}

.meta-row {
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border-color);
}

.meta-row:last-child {
    border-bottom: none;
}

.action-buttons {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.paper-section {
    margin-bottom: 2rem;
}

.paper-section h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--primary-color);
}

.summary-text {
    font-size: 1.1rem;
    line-height: 1.8;
}

.key-points {
    list-style: none;
    padding-left: 0;
}

.key-points li {
    padding: 0.75rem 0 0.75rem 2rem;
    position: relative;
    border-bottom: 1px solid var(--border-color);
}

.key-points li:before {
    content: "→";
    position: absolute;
    left: 0;
    color: var(--primary-color);
    font-weight: bold;
}

.two-column {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
}

.tags {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.tag {
    background: var(--primary-color);
    color: white;
    padding: 0.375rem 0.75rem;
    border-radius: 0.375rem;
    font-size: 0.875rem;
}

.tag-keyword {
    background: var(--secondary-color);
}

.abstract {
    background: var(--bg-color);
    padding: 1.5rem;
    border-left: 4px solid var(--primary-color);
    border-radius: 0.375rem;
    line-height: 1.8;
}

/* Footer */
footer {
    text-align: center;
    padding: 2rem 0;
    color: var(--text-muted);
    border-top: 1px solid var(--border-color);
}

footer a {
    color: var(--primary-color);
    text-decoration: none;
}

/* Weekly Hero Section */
.weekly-hero {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 1rem;
    padding: 2rem;
    margin-top: 2rem;
}

.weekly-hero h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    text-align: center;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 3rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}

.hero-stat-item {
    text-align: center;
}

.hero-stat-number {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.hero-stat-label {
    font-size: 0.95rem;
    opacity: 0.9;
    font-weight: 500;
}

.hottest-domains {
    text-align: center;
    font-size: 1.05rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
}

.btn-cta:hover {
    background: #f8fafc;
    transform: translateY(-2px);
}

/* Enhanced Stats */
.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.5rem;
}

.stat-item {
    background: rgba(255, 255, 255, 0.15);
    padding: 1.5rem;
    border-radius: 1rem;
    text-align: center;
    backdrop-filter: blur(10px);
}

.stat-number {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 0.9rem;
    opacity: 0.9;
}

/* Bookmark Button */
.bookmark-btn {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: var(--card-bg);
    border: 2px solid var(--border-color);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    transition: all 0.3s;
    z-index: 10;
}

.bookmark-btn:hover {
    transform: scale(1.1);
    border-color: var(--primary-color);
}

.bookmark-btn.bookmarked {
    background: var(--primary-color);
    border-color: var(--primary-color);
    color: white;
}

/* Paper Card Enhancements */
.paper-card {
    position: relative;
}

.paper-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.share-buttons {
    display: flex;
    gap: 0.5rem;
}

.share-btn,
.export-btn {
    background: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    width: 36px;
    height: 36px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    transition: all 0.2s;
}

.share-btn:hover,
.export-btn:hover {
    background: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
    transform: translateY(-2px);
}

/* Trending Section */
.trending-section {
    margin-bottom: 3rem;
}

.trending-section h2 {
    font-size: 2rem;
    margin-bottom: 1.5rem;
    color: var(--text-color);
}

.trending-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}

.trending-card {
    background: var(--card-bg);
    border: 2px solid var(--primary-color);
    border-radius: 1rem;
    padding: 1.5rem;
    position: relative;
    transition: transform 0.3s, box-shadow 0.3s;
}

.trending-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.trending-badge {
    position: absolute;
    top: -12px;
    right: 20px;
    background: var(--primary-color);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.85rem;
    font-weight: 600;
}

.trending-card h3 {
    margin: 0.5rem 0 1rem 0;
    font-size: 1.1rem;
}

.trending-card h3 a {
    color: var(--text-color);
    text-decoration: none;
}

.trending-card h3 a:hover {
    color: var(--primary-color);
}

.trending-meta {
    font-size: 0.85rem;
    color: var(--text-muted);
}

/* Advanced Filters */
.nav-tools {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.filter-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.filter-group label {
    font-weight: 600;
    color: var(--text-muted);
    min-width: 60px;
}

.filter-group input[type="text"] {
    padding: 0.5rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: 0.95rem;
    background: var(--card-bg);
    color: var(--text-color);
}

.btn-outline {
    background: transparent;
    border: 2px solid var(--primary-color);
    color: var(--primary-color);
}

.btn-outline:hover {
    background: var(--primary-color);
    color: white;
}

/* Export Modal */
.modal {
    display: none;
    position: fixed;
    z-index: 2000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
}

.modal-content {
    background: var(--card-bg);
    margin: 5% auto;
    padding: 2rem;
    border-radius: 1rem;
    width: 90%;
    max-width: 600px;
    box-shadow: var(--shadow-lg);
}

.modal-close {
    float: right;
    font-size: 2rem;
    font-weight: bold;
    cursor: pointer;
    color: var(--text-muted);
}

.modal-close:hover {
    color: var(--text-color);
}

.export-options {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}

.export-format {
    flex: 1;
    padding: 0.75rem 1rem;
    background: var(--bg-color);
    border: 2px solid var(--border-color);
    border-radius: 0.5rem;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s;
}

.export-format:hover {
    border-color: var(--primary-color);
    background: var(--primary-color);
    color: white;
}

#citation-output {
    width: 100%;
    min-height: 200px;
    padding: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
    margin-bottom: 1rem;
    background: var(--bg-color);
    color: var(--text-color);
}

/* Enhanced Footer */
.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-section h3 {
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.footer-section a {
    color: var(--text-color);
    text-decoration: none;
}

.footer-section a:hover {
    color: var(--primary-color);
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
}

/* No Results */
.no-results {
    text-align: center;
    padding: 4rem 2rem;
    grid-column: 1 / -1;
}

.no-results h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--text-color);
}

.no-results p {
    color: var(--text-muted);
}

/* Citations Display */
.citations {
    color: var(--accent-color);
    font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
    header h1 {
        font-size: 2rem;
    }

    .header-content {
        flex-direction: column;
        align-items: flex-start;
    }

    .stat-number {
        font-size: 2rem;
    }

    .papers-grid {
        grid-template-columns: 1fr;
    }

    .two-column {
        grid-template-columns: 1fr;
    }

    .filters {
        flex-direction: column;
        align-items: stretch;
    }

    .filters select {
        width: 100%;
    }
}
"""
        (self.output_dir / "styles.css").write_text(css, encoding='utf-8')

    def _generate_javascript(self):
        """Generate streamlined JavaScript for expert users"""
        js = """// Health AI Hub - Professional Research Tool
// Advanced Search, Filtering, Citation Export

(function() {
    'use strict';

    // ============================================
    // ADVANCED SEARCH & FILTERS
    // ============================================
    const searchInput = document.getElementById('search');
    const sortSelect = document.getElementById('sort-select');
    const domainFilter = document.getElementById('domain-filter');
    const authorFilter = document.getElementById('author-filter');
    const papersContainer = document.getElementById('papers-container');

    if (papersContainer) {
        constructor() {
            this.bookmarks = this.load();
            this.init();
        }

        load() {
            const saved = localStorage.getItem('bookmarks');
            return saved ? JSON.parse(saved) : [];
        }

        save() {
            localStorage.setItem('bookmarks', JSON.stringify(this.bookmarks));
            this.updateCount();
        }

        add(paperId) {
            if (!this.bookmarks.includes(paperId)) {
                this.bookmarks.push(paperId);
                this.save();
                return true;
            }
            return false;
        }

        remove(paperId) {
            const index = this.bookmarks.indexOf(paperId);
            if (index > -1) {
                this.bookmarks.splice(index, 1);
                this.save();
                return true;
            }
            return false;
        }

        has(paperId) {
            return this.bookmarks.includes(paperId);
        }

        toggle(paperId) {
            if (this.has(paperId)) {
                this.remove(paperId);
                return false;
            } else {
                this.add(paperId);
                return true;
            }
        }

        updateCount() {
            const countEl = document.getElementById('bookmark-count');
            if (countEl) {
                countEl.textContent = this.bookmarks.length;
            }
        }

        init() {
            this.updateCount();

            // Update all bookmark buttons
            document.querySelectorAll('.bookmark-btn').forEach(btn => {
                const paperId = btn.getAttribute('data-paper-id');
                if (this.has(paperId)) {
                    btn.classList.add('bookmarked');
                }

                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const isBookmarked = this.toggle(paperId);
                    btn.classList.toggle('bookmarked', isBookmarked);
                });
            });

            // Show bookmarks button
            const showBookmarksBtn = document.getElementById('show-bookmarks');
            if (showBookmarksBtn) {
                showBookmarksBtn.addEventListener('click', () => {
                    this.filterBookmarked();
                });
            }
        }

        filterBookmarked() {
            const papers = document.querySelectorAll('.paper-card');
            let visibleCount = 0;

            papers.forEach(paper => {
                const paperId = paper.getAttribute('data-arxiv-id');
                if (this.has(paperId)) {
                    paper.style.display = 'block';
                    visibleCount++;
                } else {
                    paper.style.display = 'none';
                }
            });

            if (visibleCount === 0) {
                alert('No bookmarks yet! Click the 🔖 button on papers to save them.');
            }
        }
    }

    const bookmarkManager = new BookmarkManager();

    // ============================================
    // ADVANCED SEARCH & FILTERS
    // ============================================
    const searchInput = document.getElementById('search');
    const sortSelect = document.getElementById('sort-select');
    const domainFilter = document.getElementById('domain-filter');
    const authorFilter = document.getElementById('author-filter');
    const papersContainer = document.getElementById('papers-container');

    if (papersContainer) {
        const papers = Array.from(papersContainer.querySelectorAll('.paper-card'));

        function filterAndSort() {
            const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
            const selectedDomain = domainFilter ? domainFilter.value.toLowerCase() : '';
            const authorTerm = authorFilter ? authorFilter.value.toLowerCase() : '';
            const sortBy = sortSelect ? sortSelect.value : 'date';

            // Filter papers
            const filteredPapers = papers.filter(paper => {
                // Search filter (title, summary, keywords, domains)
                const title = paper.querySelector('.paper-title')?.textContent.toLowerCase() || '';
                const summary = paper.querySelector('.paper-summary')?.textContent.toLowerCase() || '';
                const keywords = (paper.dataset.keywords || '').toLowerCase();
                const domains = (paper.dataset.domains || '').toLowerCase();
                const authors = (paper.dataset.authors || '').toLowerCase();

                const matchesSearch = !searchTerm ||
                    title.includes(searchTerm) ||
                    summary.includes(searchTerm) ||
                    keywords.includes(searchTerm) ||
                    domains.includes(searchTerm) ||
                    authors.includes(searchTerm);

                // Domain filter
                const matchesDomain = !selectedDomain || domains.includes(selectedDomain);

                // Author filter
                const matchesAuthor = !authorTerm || authors.includes(authorTerm);

                return matchesSearch && matchesDomain && matchesAuthor;
            });

            // Sort papers
            filteredPapers.sort((a, b) => {
                if (sortBy === 'date') {
                    const dateA = a.querySelector('.date')?.textContent || '';
                    const dateB = b.querySelector('.date')?.textContent || '';
                    return dateB.localeCompare(dateA);
                } else if (sortBy === 'relevance') {
                    const relA = parseFloat(a.querySelector('.relevance')?.textContent.split(' ')[1] || 0);
                    const relB = parseFloat(b.querySelector('.relevance')?.textContent.split(' ')[1] || 0);
                    return relB - relA;
                } else if (sortBy === 'citations') {
                    const citA = parseInt(a.querySelector('.citations')?.textContent.match(/\\d+/)?.[0] || 0);
                    const citB = parseInt(b.querySelector('.citations')?.textContent.match(/\\d+/)?.[0] || 0);
                    return citB - citA;
                } else if (sortBy === 'title') {
                    const titleA = a.querySelector('.paper-title')?.textContent || '';
                    const titleB = b.querySelector('.paper-title')?.textContent || '';
                    return titleA.localeCompare(titleB);
                }
                return 0;
            });

            // Hide all papers
            papers.forEach(paper => paper.style.display = 'none');

            // Show filtered and sorted papers
            filteredPapers.forEach(paper => {
                paper.style.display = 'block';
                papersContainer.appendChild(paper);
            });

            // Show/hide no results message
            updateNoResults(filteredPapers.length === 0);
        }

        function updateNoResults(show) {
            let noResults = document.getElementById('no-results');
            if (show && !noResults) {
                noResults = document.createElement('div');
                noResults.id = 'no-results';
                noResults.className = 'no-results';
                noResults.innerHTML = `
                    <h3>No papers found</h3>
                    <p>Try adjusting your search criteria or filters.</p>
                `;
                papersContainer.appendChild(noResults);
            } else if (!show && noResults) {
                noResults.remove();
            }
        }

        // Attach event listeners
        if (searchInput) searchInput.addEventListener('input', filterAndSort);
        if (sortSelect) sortSelect.addEventListener('change', filterAndSort);
        if (domainFilter) domainFilter.addEventListener('change', filterAndSort);
        if (authorFilter) authorFilter.addEventListener('input', filterAndSort);
    }

    // ============================================
    // SOCIAL SHARING
    // ============================================
    document.querySelectorAll('.share-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const paperId = this.getAttribute('data-paper-id');
            const paperCard = this.closest('.paper-card');
            const title = paperCard.querySelector('.paper-title a')?.textContent || '';
            const url = `https://arxiv-health.org/papers/${paperId.replace('/', '_')}.html`;

            const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}&via=ArXiv_Health&hashtags=HealthAI,MedicalAI,Research`;

            window.open(shareUrl, '_blank', 'width=600,height=400');
        });
    });

    // ============================================
    // CITATION EXPORT
    // ============================================
    const exportModal = document.getElementById('export-modal');
    const citationOutput = document.getElementById('citation-output');
    let currentPaperId = null;

    // Export button click
    document.querySelectorAll('.export-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            currentPaperId = this.getAttribute('data-paper-id');
            if (exportModal) {
                exportModal.style.display = 'block';
            }
        });
    });

    // Format selection
    document.querySelectorAll('.export-format').forEach(btn => {
        btn.addEventListener('click', async function() {
            const format = this.getAttribute('data-format');
            if (!currentPaperId || !citationOutput) return;

            // Fallback: generate simple citation
            citationOutput.value = generateFallbackCitation(currentPaperId, format);
        });
    });

    // Copy to clipboard
    const copyCitationBtn = document.getElementById('copy-citation');
    if (copyCitationBtn) {
        copyCitationBtn.addEventListener('click', () => {
            if (citationOutput) {
                citationOutput.select();
                document.execCommand('copy');
                copyCitationBtn.textContent = 'Copied!';
                setTimeout(() => {
                    copyCitationBtn.textContent = 'Copy to Clipboard';
                }, 2000);
            }
        });
    }

    // Close modal
    const modalClose = document.querySelector('.modal-close');
    if (modalClose) {
        modalClose.addEventListener('click', () => {
            if (exportModal) {
                exportModal.style.display = 'none';
            }
        });
    }

    // Close on outside click
    window.addEventListener('click', (e) => {
        if (e.target === exportModal) {
            exportModal.style.display = 'none';
        }
    });

    function generateFallbackCitation(paperId, format) {
        // Simple fallback citation generation
        const paperCard = document.querySelector(`[data-arxiv-id="${paperId}"]`);
        if (!paperCard) return '';

        const title = paperCard.querySelector('.paper-title')?.textContent || '';
        const authors = paperCard.dataset.authors || '';
        const date = paperCard.querySelector('.date')?.textContent.replace('📅 ', '') || '';

        if (format === 'bibtex') {
            return `@article{${paperId.replace('/', '_')},
  title={${title}},
  author={${authors.split(',')[0]}},
  year={${date.substring(0, 4)}},
  url={https://arxiv.org/abs/${paperId}}
}`;
        } else if (format === 'ris') {
            return `TY  - JOUR
TI  - ${title}
AU  - ${authors.split(',')[0]}
PY  - ${date.substring(0, 4)}
UR  - https://arxiv.org/abs/${paperId}
ER  -`;
        }
        return `${title}\\n${authors}\\n${date}\\nhttps://arxiv.org/abs/${paperId}`;
    }

    // ============================================
    // SMOOTH SCROLLING
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // ============================================
    // ANALYTICS (Page views tracking)
    // ============================================
    function trackView() {
        // Simple view tracking - can integrate with Google Analytics later
        const viewed = sessionStorage.getItem('papers_viewed') || '[]';
        const viewedList = JSON.parse(viewed);

        document.querySelectorAll('.paper-card').forEach(card => {
            const paperId = card.getAttribute('data-arxiv-id');
            if (!viewedList.includes(paperId)) {
                // Track as viewed when in viewport
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            viewedList.push(paperId);
                            sessionStorage.setItem('papers_viewed', JSON.stringify(viewedList));
                            observer.disconnect();
                        }
                    });
                }, { threshold: 0.5 });

                observer.observe(card);
            }
        });
    }

    trackView();

    console.log('🔬 Health AI Hub - Enhanced Features Loaded');
})();
"""
        (self.output_dir / "script.js").write_text(js, encoding='utf-8')

    def _get_trending_papers(self, papers: List[Dict]) -> List[Dict]:
        """Calculate and return trending papers"""
        from src.enhancements import PaperEnhancements

        trending = []
        for paper in papers:
            paper_copy = paper.copy()
            paper_copy['trending_score'] = PaperEnhancements.calculate_trending_score(paper)
            trending.append(paper_copy)

        # Sort by trending score
        trending.sort(key=lambda x: x['trending_score'], reverse=True)
        return trending[:10]  # Return top 10

    def _generate_search_index(self, papers: List[Dict]):
        """Generate JSON search index for advanced search"""
        search_index = []
        for paper in papers:
            search_index.append({
                'id': paper['arxiv_id'],
                'title': paper['title'],
                'authors': paper['authors'],
                'summary': paper['summary'],
                'keywords': paper.get('keywords', []),
                'domains': paper.get('medical_domains', []),
                'url': f"papers/{paper['arxiv_id'].replace('/', '_')}.html"
            })

        (self.output_dir / "search-index.json").write_text(
            json.dumps(search_index, indent=2),
            encoding='utf-8'
        )
