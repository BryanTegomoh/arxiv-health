"""
Enhanced HTML templates for Health AI Hub with all new features
"""

def get_enhanced_index_template():
    """Returns enhanced index page template with all new features"""
    return """<!DOCTYPE html>
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

    <!-- Favicons -->
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">

    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Dark Mode Toggle -->
    <button id="theme-toggle" class="theme-toggle" aria-label="Toggle dark mode">
        <span class="theme-toggle-light">🌙</span>
        <span class="theme-toggle-dark">☀️</span>
    </button>

    <header>
        <div class="container">
            <div class="header-content">
                <div>
                    <h1>{{ site_title }}</h1>
                    <p class="tagline">{{ tagline }}</p>
                </div>
                <div class="header-actions">
                    <a href="{{ substack_url }}" target="_blank" class="btn btn-cta">
                        📧 Subscribe to Newsletter
                    </a>
                    <a href="https://twitter.com/{{ twitter_handle[1:] }}" target="_blank" class="btn btn-secondary">
                        𝕏 Follow @{{ twitter_handle[1:] }}
                    </a>
                </div>
            </div>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{{ stats.total_papers }}</div>
                    <div class="stat-label">Papers Curated</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ stats.domains|length }}</div>
                    <div class="stat-label">Medical Domains</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ total_citations }}</div>
                    <div class="stat-label">Total Citations</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">Daily</div>
                    <div class="stat-label">Updates</div>
                </div>
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
                <button id="show-bookmarks" class="btn btn-outline">
                    🔖 My Bookmarks (<span id="bookmark-count">0</span>)
                </button>
            </div>
        </div>
    </nav>

    {% if trending_papers %}
    <section class="container trending-section">
        <h2>🔥 Trending This Week</h2>
        <div class="trending-grid">
            {% for paper in trending_papers[:3] %}
            <div class="trending-card">
                <div class="trending-badge">Trending #{{ loop.index }}</div>
                <h3><a href="papers/{{ paper.arxiv_id|replace('/', '_') }}.html">{{ paper.title }}</a></h3>
                <p class="trending-meta">
                    ⭐ {{ "%.2f"|format(paper.relevance_score) }} |
                    📖 {{ paper.citation_count or 0 }} citations |
                    🔥 Score: {{ paper.trending_score }}
                </p>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    <main class="container">
        <div class="papers-grid" id="papers-container">
            {% for paper in papers %}
            <article class="paper-card"
                     data-arxiv-id="{{ paper.arxiv_id }}"
                     data-domains="{{ paper.medical_domains|join(',') }}"
                     data-keywords="{{ paper.keywords|join(',') }}"
                     data-authors="{{ paper.authors|join(',') }}">

                <button class="bookmark-btn" data-paper-id="{{ paper.arxiv_id }}" aria-label="Bookmark this paper">
                    <span class="bookmark-icon">🔖</span>
                </button>

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

                <div class="paper-actions">
                    <div class="paper-links">
                        <a href="papers/{{ paper.arxiv_id|replace('/', '_') }}.html" class="btn btn-primary">Read Full Summary</a>
                        <a href="{{ paper.arxiv_url }}" target="_blank" class="btn btn-secondary">arXiv</a>
                        <a href="{{ paper.pdf_url }}" target="_blank" class="btn btn-secondary">PDF</a>
                    </div>
                    <div class="share-buttons">
                        <button class="share-btn" data-share="twitter" data-paper-id="{{ paper.arxiv_id }}" title="Share on X/Twitter">
                            𝕏
                        </button>
                        <button class="export-btn" data-paper-id="{{ paper.arxiv_id }}" title="Export Citation">
                            📚
                        </button>
                    </div>
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
                <p>Powered by AI | Updated Daily</p>
            </div>
            <div class="footer-section">
                <h3>Connect</h3>
                <p><a href="https://twitter.com/{{ twitter_handle[1:] }}" target="_blank">Twitter/X</a></p>
                <p><a href="{{ substack_url }}" target="_blank">Newsletter</a></p>
                <p><a href="https://github.com/BryanTegomoh/arxiv-health" target="_blank">GitHub</a></p>
            </div>
            <div class="footer-section">
                <h3>Resources</h3>
                <p><a href="https://arxiv.org" target="_blank">arXiv.org</a></p>
                <p><a href="mailto:{{ contact_email }}">Contact</a></p>
                <p><a href="https://github.com/BryanTegomoh/arxiv-health/discussions" target="_blank">Discussions</a></p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2025 Health AI Hub | Last updated: {{ last_updated }} |
            <a href="https://github.com/BryanTegomoh/arxiv-health">Open Source</a></p>
        </div>
    </footer>

    <!-- Export Modal -->
    <div id="export-modal" class="modal">
        <div class="modal-content">
            <span class="modal-close">&times;</span>
            <h2>Export Citation</h2>
            <div class="export-options">
                <button class="export-format" data-format="bibtex">BibTeX</button>
                <button class="export-format" data-format="ris">RIS (EndNote, Mendeley)</button>
                <button class="export-format" data-format="endnote">EndNote</button>
            </div>
            <textarea id="citation-output" readonly></textarea>
            <button id="copy-citation" class="btn btn-primary">Copy to Clipboard</button>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
"""


def get_enhanced_css():
    """Returns enhanced CSS with all new features"""
    # This is too long for one message - will create separately
    pass
