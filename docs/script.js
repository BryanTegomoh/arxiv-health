
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
