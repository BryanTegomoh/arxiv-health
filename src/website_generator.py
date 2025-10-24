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
        template = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ site_title }}</title>
    <meta name="description" content="{{ site_description }}">
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>{{ site_title }}</h1>
            <p class="tagline">{{ site_description }}</p>
            <div class="stats">
                <span class="stat-item">📚 {{ stats.total_papers }} papers</span>
                <span class="stat-item">🏥 {{ stats.domains|length }} medical domains</span>
                <span class="stat-item">📅 Updated: {{ last_updated }}</span>
            </div>
        </div>
    </header>

    <nav class="container">
        <div class="search-box">
            <input type="text" id="search" placeholder="Search papers by title, keywords, or domain...">
        </div>
        <div class="filters">
            <label>Sort by:</label>
            <select id="sort-select">
                <option value="date">Newest First</option>
                <option value="relevance">Relevance Score</option>
                <option value="title">Title A-Z</option>
            </select>
            <label>Filter by domain:</label>
            <select id="domain-filter">
                <option value="">All Domains</option>
                {% for domain, count in stats.top_domains %}
                <option value="{{ domain }}">{{ domain|title }} ({{ count }})</option>
                {% endfor %}
            </select>
        </div>
    </nav>

    <main class="container">
        <div class="papers-grid" id="papers-container">
            {% for paper in papers %}
            <article class="paper-card" data-domains="{{ paper.medical_domains|join(',') }}" data-keywords="{{ paper.keywords|join(',') }}">
                <div class="paper-header">
                    <h2 class="paper-title">
                        <a href="papers/{{ paper.arxiv_id|replace('/', '_') }}.html">{{ paper.title }}</a>
                    </h2>
                    <div class="paper-meta">
                        <span class="date">📅 {{ paper.published[:10] }}</span>
                        <span class="relevance">⭐ {{ "%.2f"|format(paper.relevance_score) }}</span>
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
                    <a href="papers/{{ paper.arxiv_id|replace('/', '_') }}.html" class="btn btn-primary">Read Summary</a>
                    <a href="{{ paper.arxiv_url }}" target="_blank" class="btn btn-secondary">arXiv</a>
                    <a href="{{ paper.pdf_url }}" target="_blank" class="btn btn-secondary">PDF</a>
                </div>
            </article>
            {% endfor %}
        </div>
    </main>

    <footer class="container">
        <p>Generated by <a href="https://github.com/BryanTegomoh/arxiv-health">arXiv Health Monitor</a> |
        Data from <a href="https://arxiv.org">arXiv.org</a> |
        Last updated: {{ last_updated }}</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
""")

        html = template.render(
            site_title=config.SITE_TITLE,
            site_description=config.SITE_DESCRIPTION,
            papers=papers,
            stats=stats,
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

/* Dark Mode */
[data-theme="dark"] {
    --primary-color: #14b8a6;
    --secondary-color: #06b6d4;
    --accent-color: #10b981;
    --bg-color: #0f172a;
    --card-bg: #1e293b;
    --text-color: #f1f5f9;
    --text-muted: #94a3b8;
    --border-color: #334155;
    --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.3);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.4);
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

/* Responsive */
@media (max-width: 768px) {
    header h1 {
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
        """Generate JavaScript for search and filtering"""
        js = """
// arXiv Health Monitor - Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    const sortSelect = document.getElementById('sort-select');
    const domainFilter = document.getElementById('domain-filter');
    const papersContainer = document.getElementById('papers-container');

    if (!papersContainer) return; // Not on index page

    const papers = Array.from(papersContainer.querySelectorAll('.paper-card'));

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', filterAndSort);
    }

    // Sort functionality
    if (sortSelect) {
        sortSelect.addEventListener('change', filterAndSort);
    }

    // Domain filter
    if (domainFilter) {
        domainFilter.addEventListener('change', filterAndSort);
    }

    function filterAndSort() {
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
        const selectedDomain = domainFilter ? domainFilter.value.toLowerCase() : '';
        const sortBy = sortSelect ? sortSelect.value : 'date';

        // Filter papers
        const filteredPapers = papers.filter(paper => {
            // Search filter
            const title = paper.querySelector('.paper-title').textContent.toLowerCase();
            const summary = paper.querySelector('.paper-summary').textContent.toLowerCase();
            const keywords = paper.dataset.keywords.toLowerCase();
            const domains = paper.dataset.domains.toLowerCase();

            const matchesSearch = !searchTerm ||
                title.includes(searchTerm) ||
                summary.includes(searchTerm) ||
                keywords.includes(searchTerm) ||
                domains.includes(searchTerm);

            // Domain filter
            const matchesDomain = !selectedDomain || domains.includes(selectedDomain);

            return matchesSearch && matchesDomain;
        });

        // Sort papers
        filteredPapers.sort((a, b) => {
            if (sortBy === 'date') {
                const dateA = a.querySelector('.date').textContent;
                const dateB = b.querySelector('.date').textContent;
                return dateB.localeCompare(dateA);
            } else if (sortBy === 'relevance') {
                const relA = parseFloat(a.querySelector('.relevance').textContent.split(' ')[1]);
                const relB = parseFloat(b.querySelector('.relevance').textContent.split(' ')[1]);
                return relB - relA;
            } else if (sortBy === 'title') {
                const titleA = a.querySelector('.paper-title').textContent;
                const titleB = b.querySelector('.paper-title').textContent;
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

        // Show message if no results
        const noResults = document.getElementById('no-results');
        if (filteredPapers.length === 0) {
            if (!noResults) {
                const msg = document.createElement('div');
                msg.id = 'no-results';
                msg.className = 'no-results';
                msg.textContent = 'No papers found matching your criteria.';
                papersContainer.appendChild(msg);
            }
        } else if (noResults) {
            noResults.remove();
        }
    }
});
"""
        (self.output_dir / "script.js").write_text(js, encoding='utf-8')

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
