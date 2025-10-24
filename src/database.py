"""
Database management for tracking processed papers
"""
from tinydb import TinyDB, Query
from datetime import datetime
from typing import Dict, List, Optional
import re
import config


class PaperDatabase:
    """Manages storage and retrieval of processed papers"""

    def __init__(self, db_path: str = None):
        """
        Initialize database

        Args:
            db_path: Path to database file
        """
        if db_path is None:
            db_path = config.DATABASE_PATH

        self.db = TinyDB(str(db_path), indent=2, sort_keys=True)
        self.papers = self.db.table('papers')
        self.metadata = self.db.table('metadata')
        print(f"Database initialized at: {db_path}")

    def paper_exists(self, arxiv_id: str) -> bool:
        """
        Check if paper already exists in database

        Args:
            arxiv_id: arXiv ID of paper

        Returns:
            True if paper exists
        """
        Paper = Query()
        return len(self.papers.search(Paper.arxiv_id == arxiv_id)) > 0

    def add_paper(self, paper: Dict, summary: Dict, relevance_info: Dict) -> bool:
        """
        Add a paper to the database

        Args:
            paper: Paper metadata from arXiv
            summary: AI-generated summary
            relevance_info: Relevance check results

        Returns:
            True if added successfully
        """
        # Check if already exists
        if self.paper_exists(paper['arxiv_id']):
            print(f"  Paper {paper['arxiv_id']} already in database, skipping")
            return False

        # Combine all information
        full_record = {
            **paper,
            'summary': summary.get('summary', ''),
            'key_points': summary.get('key_points', []),
            'medical_relevance': summary.get('medical_relevance', ''),
            'keywords': summary.get('keywords', []),
            'medical_domains': summary.get('medical_domains', []),
            'methodology': summary.get('methodology', ''),
            'key_findings': summary.get('key_findings', ''),
            'clinical_impact': summary.get('clinical_impact', ''),
            'limitations': summary.get('limitations', ''),
            'future_directions': summary.get('future_directions', ''),
            'relevance_score': relevance_info.get('relevance_score', 0.0),
            'relevance_reasoning': relevance_info.get('reasoning', ''),
            'ai_health_application': relevance_info.get('ai_health_application', ''),
            'added_to_db': datetime.now().isoformat(),
            'pdf_path': paper.get('pdf_path', None)
        }

        self.papers.insert(full_record)
        print(f"  Added paper to database: {paper['arxiv_id']}")
        return True

    def get_all_papers(self, limit: int = None, sort_by: str = 'published') -> List[Dict]:
        """
        Get all papers from database

        Args:
            limit: Maximum number of papers to return
            sort_by: Field to sort by (published, relevance_score, added_to_db)

        Returns:
            List of paper records
        """
        papers = self.papers.all()

        # Sort papers
        if sort_by == 'published':
            papers.sort(key=lambda x: x.get('published', ''), reverse=True)
        elif sort_by == 'relevance_score':
            papers.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        elif sort_by == 'added_to_db':
            papers.sort(key=lambda x: x.get('added_to_db', ''), reverse=True)

        if limit:
            return papers[:limit]
        return papers

    def get_paper_by_id(self, arxiv_id: str) -> Optional[Dict]:
        """
        Get a specific paper by arXiv ID

        Args:
            arxiv_id: arXiv ID

        Returns:
            Paper record or None
        """
        Paper = Query()
        results = self.papers.search(Paper.arxiv_id == arxiv_id)
        return results[0] if results else None

    def search_papers(self, query: str) -> List[Dict]:
        """
        Search papers by keyword in title, abstract, or keywords

        Args:
            query: Search query

        Returns:
            List of matching papers
        """
        Paper = Query()
        query_lower = query.lower()

        results = self.papers.search(
            (Paper.title.search(query_lower, flags=re.IGNORECASE)) |
            (Paper.abstract.search(query_lower, flags=re.IGNORECASE)) |
            (Paper.keywords.any(query_lower))
        )

        return results

    def get_papers_by_domain(self, domain: str) -> List[Dict]:
        """
        Get papers by medical domain

        Args:
            domain: Medical domain (e.g., 'oncology', 'cardiology')

        Returns:
            List of papers in that domain
        """
        Paper = Query()
        return self.papers.search(Paper.medical_domains.any(domain.lower()))

    def get_statistics(self) -> Dict:
        """
        Get database statistics

        Returns:
            Dictionary with statistics
        """
        papers = self.papers.all()

        # Collect all domains
        all_domains = []
        for paper in papers:
            all_domains.extend(paper.get('medical_domains', []))

        # Count domains
        domain_counts = {}
        for domain in all_domains:
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        # Get date range
        dates = [p.get('published', '') for p in papers if p.get('published')]
        dates.sort()

        stats = {
            'total_papers': len(papers),
            'date_range': {
                'earliest': dates[0] if dates else None,
                'latest': dates[-1] if dates else None
            },
            'average_relevance': sum(p.get('relevance_score', 0) for p in papers) / len(papers) if papers else 0,
            'domains': domain_counts,
            'top_domains': sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        }

        return stats

    def update_last_run(self):
        """Update last run timestamp in metadata"""
        Metadata = Query()
        self.metadata.upsert(
            {'key': 'last_run', 'timestamp': datetime.now().isoformat()},
            Metadata.key == 'last_run'
        )

    def get_last_run(self) -> Optional[str]:
        """
        Get timestamp of last run

        Returns:
            ISO timestamp string or None
        """
        Metadata = Query()
        result = self.metadata.search(Metadata.key == 'last_run')
        return result[0]['timestamp'] if result else None

    def close(self):
        """Close database connection"""
        self.db.close()
