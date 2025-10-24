"""
Semantic Scholar API integration for citation counts and paper metadata
"""
import requests
import time
from typing import Dict, List, Optional


class SemanticScholarAPI:
    """Interface to Semantic Scholar Academic Graph API"""

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Health-AI-Hub/1.0 (bryan@arxiv-health.org)'
        })

    def get_paper_by_arxiv_id(self, arxiv_id: str) -> Optional[Dict]:
        """
        Get paper details from Semantic Scholar by arXiv ID

        Args:
            arxiv_id: arXiv ID (e.g., "2301.12345v1")

        Returns:
            Dictionary with citation count, influential citations, references, etc.
        """
        # Clean arXiv ID (remove version if present)
        clean_id = arxiv_id.split('v')[0] if 'v' in arxiv_id else arxiv_id

        # Query Semantic Scholar
        url = f"{self.BASE_URL}/paper/arXiv:{clean_id}"
        params = {
            'fields': 'title,citationCount,influentialCitationCount,referenceCount,publicationDate,authors,year,fieldsOfStudy,s2FieldsOfStudy,embedding,tldr'
        }

        try:
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return self._parse_paper_data(data)
            elif response.status_code == 404:
                # Paper not in Semantic Scholar yet (common for new preprints)
                return None
            else:
                print(f"Semantic Scholar API error: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Semantic Scholar: {e}")
            return None

        finally:
            # Rate limiting: 100 requests per 5 minutes for free tier
            time.sleep(0.1)

    def _parse_paper_data(self, data: Dict) -> Dict:
        """Parse Semantic Scholar API response"""
        return {
            'citation_count': data.get('citationCount', 0),
            'influential_citation_count': data.get('influentialCitationCount', 0),
            'reference_count': data.get('referenceCount', 0),
            'publication_year': data.get('year'),
            'publication_date': data.get('publicationDate'),
            'fields_of_study': data.get('fieldsOfStudy', []),
            's2_fields': [f.get('category') for f in data.get('s2FieldsOfStudy', [])],
            'tldr': data.get('tldr', {}).get('text') if data.get('tldr') else None,
            's2_url': f"https://www.semanticscholar.org/paper/{data.get('paperId')}" if data.get('paperId') else None
        }

    def get_related_papers(self, arxiv_id: str, limit: int = 5) -> List[Dict]:
        """
        Get papers related to the given arXiv paper

        Args:
            arxiv_id: arXiv ID
            limit: Number of related papers to return

        Returns:
            List of related paper dictionaries
        """
        clean_id = arxiv_id.split('v')[0] if 'v' in arxiv_id else arxiv_id

        url = f"{self.BASE_URL}/paper/arXiv:{clean_id}/citations"
        params = {
            'fields': 'title,year,citationCount,authors',
            'limit': limit
        }

        try:
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                return []

        except requests.exceptions.RequestException as e:
            print(f"Error fetching related papers: {e}")
            return []

        finally:
            time.sleep(0.1)

    def search_papers(self, query: str, limit: int = 10, fields: str = None) -> List[Dict]:
        """
        Search for papers by query

        Args:
            query: Search query
            limit: Number of results
            fields: Fields to include in response

        Returns:
            List of paper dictionaries
        """
        if not fields:
            fields = 'title,year,citationCount,authors,abstract'

        url = f"{self.BASE_URL}/paper/search"
        params = {
            'query': query,
            'limit': limit,
            'fields': fields
        }

        try:
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                return []

        except requests.exceptions.RequestException:
            return []

        finally:
            time.sleep(0.1)
