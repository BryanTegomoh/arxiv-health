"""
Additional features and enhancements for Health AI Hub
"""
import json
from typing import Dict, List
from datetime import datetime, timedelta


class PaperEnhancements:
    """Helper class for paper enhancements like trending, bookmarks, etc."""

    @staticmethod
    def calculate_trending_score(paper: Dict) -> float:
        """
        Calculate trending score based on recency and relevance

        Args:
            paper: Paper dictionary

        Returns:
            Trending score (0-100)
        """
        # Get paper age in days
        published_str = paper.get('published', datetime.now().isoformat())
        # Remove timezone info if present for comparison
        if 'T' in published_str:
            published_str = published_str.split('+')[0].split('Z')[0]
        published = datetime.fromisoformat(published_str)
        age_days = (datetime.now() - published).days

        # Recency score (newer = higher)
        if age_days == 0:
            recency_score = 100
        elif age_days <= 3:
            recency_score = 90
        elif age_days <= 7:
            recency_score = 70
        elif age_days <= 14:
            recency_score = 50
        elif age_days <= 30:
            recency_score = 30
        else:
            recency_score = 10

        # Relevance score (from AI)
        relevance_score = paper.get('relevance_score', 0.5) * 100

        # Citation score (if available)
        citation_count = paper.get('citation_count', 0)
        citation_score = min(citation_count * 5, 50)  # Cap at 50

        # Combined trending score
        trending_score = (recency_score * 0.5) + (relevance_score * 0.3) + (citation_score * 0.2)

        return round(trending_score, 2)

    @staticmethod
    def generate_bibtex(paper: Dict) -> str:
        """
        Generate BibTeX citation for a paper

        Args:
            paper: Paper dictionary

        Returns:
            BibTeX formatted string
        """
        arxiv_id = paper['arxiv_id'].replace('/', '_')
        year = paper.get('published', '')[:4]
        authors = ' and '.join(paper.get('authors', [])[:3])

        bibtex = f"""@article{{{arxiv_id},
  title={{{paper['title']}}},
  author={{{authors}}},
  journal={{arXiv preprint arXiv:{paper['arxiv_id']}}},
  year={{{year}}},
  url={{{paper['arxiv_url']}}}
}}"""
        return bibtex

    @staticmethod
    def generate_ris(paper: Dict) -> str:
        """
        Generate RIS citation format

        Args:
            paper: Paper dictionary

        Returns:
            RIS formatted string
        """
        authors = paper.get('authors', [])
        year = paper.get('published', '')[:4]

        ris = f"""TY  - JOUR
TI  - {paper['title']}
"""
        for author in authors[:5]:
            ris += f"AU  - {author}\n"

        ris += f"""PY  - {year}
JO  - arXiv preprint
UR  - {paper['arxiv_url']}
AB  - {paper.get('abstract', '')[:500]}
ER  -
"""
        return ris

    @staticmethod
    def generate_endnote(paper: Dict) -> str:
        """
        Generate EndNote citation format

        Args:
            paper: Paper dictionary

        Returns:
            EndNote formatted string
        """
        authors = paper.get('authors', [])
        year = paper.get('published', '')[:4]

        endnote = f"""%T {paper['title']}
"""
        for author in authors[:5]:
            endnote += f"%A {author}\n"

        endnote += f"""%D {year}
%J arXiv preprint
%U {paper['arxiv_url']}
%X {paper.get('abstract', '')[:500]}
"""
        return endnote

    @staticmethod
    def extract_author_info(papers: List[Dict]) -> Dict[str, Dict]:
        """
        Extract and aggregate author information from papers

        Args:
            papers: List of paper dictionaries

        Returns:
            Dictionary mapping author names to their papers and stats
        """
        authors = {}

        for paper in papers:
            for author_name in paper.get('authors', []):
                if author_name not in authors:
                    authors[author_name] = {
                        'name': author_name,
                        'paper_count': 0,
                        'papers': [],
                        'domains': set(),
                        'total_relevance': 0
                    }

                authors[author_name]['paper_count'] += 1
                authors[author_name]['papers'].append({
                    'arxiv_id': paper['arxiv_id'],
                    'title': paper['title'],
                    'published': paper.get('published')
                })
                authors[author_name]['domains'].update(paper.get('medical_domains', []))
                authors[author_name]['total_relevance'] += paper.get('relevance_score', 0)

        # Convert sets to lists for JSON serialization
        for author in authors.values():
            author['domains'] = list(author['domains'])
            author['avg_relevance'] = author['total_relevance'] / author['paper_count'] if author['paper_count'] > 0 else 0

        return authors

    @staticmethod
    def get_domain_stats(papers: List[Dict]) -> Dict:
        """
        Calculate comprehensive domain statistics

        Args:
            papers: List of paper dictionaries

        Returns:
            Dictionary with domain trends and statistics
        """
        domain_stats = {}
        domain_timeline = {}

        for paper in papers:
            pub_date = paper.get('published', '')[:7]  # YYYY-MM format

            for domain in paper.get('medical_domains', []):
                # Overall stats
                if domain not in domain_stats:
                    domain_stats[domain] = {
                        'count': 0,
                        'total_relevance': 0,
                        'papers': []
                    }

                domain_stats[domain]['count'] += 1
                domain_stats[domain]['total_relevance'] += paper.get('relevance_score', 0)
                domain_stats[domain]['papers'].append(paper['arxiv_id'])

                # Timeline stats
                if domain not in domain_timeline:
                    domain_timeline[domain] = {}

                if pub_date not in domain_timeline[domain]:
                    domain_timeline[domain][pub_date] = 0

                domain_timeline[domain][pub_date] += 1

        # Calculate averages
        for domain in domain_stats:
            count = domain_stats[domain]['count']
            domain_stats[domain]['avg_relevance'] = domain_stats[domain]['total_relevance'] / count if count > 0 else 0

        return {
            'stats': domain_stats,
            'timeline': domain_timeline
        }
