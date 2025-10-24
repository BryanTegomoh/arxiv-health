// Health AI Hub - Enhanced JavaScript with all features
// Dark Mode, Bookmarks, Advanced Search, Social Sharing, Export, etc.

(function() {
    'use strict';

    // ============================================
    // DARK MODE
    // ============================================
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // ============================================
    // BOOKMARKS
    // ============================================
    class BookmarkManager {
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

            // Fetch citation data
            try {
                const response = await fetch(`/api/citation/${currentPaperId}/${format}`);
                if (response.ok) {
                    const citation = await response.text();
                    citationOutput.value = citation;
                } else {
                    // Fallback: generate simple citation
                    citationOutput.value = generateFallbackCitation(currentPaperId, format);
                }
            } catch (error) {
                citationOutput.value = generateFallbackCitation(currentPaperId, format);
            }
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
