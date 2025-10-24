"""
arXiv API client for fetching medical and health-related papers
"""
import arxiv
import time
from datetime import datetime, timedelta
from typing import List, Dict
import config


class ArxivHealthClient:
    """Client for searching and fetching health-related papers from arXiv"""

    def __init__(self):
        self.client = arxiv.Client()
        self.keywords = config.HEALTH_KEYWORDS
        self.categories = config.ARXIV_CATEGORIES

    def build_search_query(self, days_back: int = None) -> str:
        """
        Build arXiv search query for medical/health papers

        Args:
            days_back: Number of days to look back for papers

        Returns:
            Query string for arXiv API
        """
        if days_back is None:
            days_back = config.DAYS_TO_LOOK_BACK

        # Build keyword search (title or abstract contains health keywords)
        keyword_queries = []
        for keyword in self.keywords[:30]:  # Limit to avoid query length issues
            keyword_queries.append(f'ti:"{keyword}" OR abs:"{keyword}"')

        keyword_query = " OR ".join(keyword_queries)

        # Add category filters
        category_queries = []
        for cat in self.categories:
            if "*" in cat:
                # For wildcard categories, just use the base
                base_cat = cat.replace(".*", "")
                category_queries.append(f'cat:{base_cat}.*')
            else:
                category_queries.append(f'cat:{cat}')

        category_query = " OR ".join(category_queries)

        # Combine queries
        full_query = f"({keyword_query}) AND ({category_query})"

        return full_query

    def fetch_recent_papers(self, max_results: int = None, days_back: int = None) -> List[Dict]:
        """
        Fetch recent health-related papers from arXiv

        Args:
            max_results: Maximum number of papers to fetch
            days_back: Number of days to look back

        Returns:
            List of paper dictionaries
        """
        if max_results is None:
            max_results = config.MAX_RESULTS_PER_RUN

        query = self.build_search_query(days_back)

        print(f"Searching arXiv with query (limited display): {query[:200]}...")

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

        papers = []
        try:
            for result in self.client.results(search):
                paper = self._parse_arxiv_result(result)
                papers.append(paper)
                print(f"  Found: {paper['title'][:80]}... ({paper['arxiv_id']})")

        except Exception as e:
            print(f"Error fetching papers: {e}")

        print(f"\nFetched {len(papers)} papers from arXiv")
        return papers

    def _parse_arxiv_result(self, result) -> Dict:
        """
        Parse arXiv search result into structured dictionary

        Args:
            result: arXiv API result object

        Returns:
            Dictionary with paper information
        """
        return {
            "arxiv_id": result.entry_id.split("/")[-1],
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "abstract": result.summary,
            "categories": result.categories,
            "published": result.published.isoformat(),
            "updated": result.updated.isoformat(),
            "pdf_url": result.pdf_url,
            "arxiv_url": result.entry_id,
            "primary_category": result.primary_category,
            "comment": result.comment if hasattr(result, 'comment') else None,
            "journal_ref": result.journal_ref if hasattr(result, 'journal_ref') else None,
        }

    def download_pdf(self, paper: Dict, output_dir: str = None) -> str:
        """
        Download PDF for a paper

        Args:
            paper: Paper dictionary with pdf_url
            output_dir: Directory to save PDF

        Returns:
            Path to downloaded PDF file
        """
        if output_dir is None:
            output_dir = config.PAPERS_DIR

        arxiv_id = paper['arxiv_id']
        pdf_path = output_dir / f"{arxiv_id.replace('/', '_')}.pdf"

        # Skip if already downloaded
        if pdf_path.exists():
            print(f"  PDF already exists: {pdf_path.name}")
            return str(pdf_path)

        try:
            # Use arxiv library to download
            search = arxiv.Search(id_list=[arxiv_id])
            result = next(self.client.results(search))
            result.download_pdf(filename=str(pdf_path))
            print(f"  Downloaded PDF: {pdf_path.name}")
            time.sleep(1)  # Be nice to arXiv servers
            return str(pdf_path)

        except Exception as e:
            print(f"  Error downloading PDF for {arxiv_id}: {e}")
            return None
