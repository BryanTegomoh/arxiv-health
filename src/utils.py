"""
Utility functions for website generation
"""
from datetime import datetime, timedelta
from typing import List, Dict
from collections import Counter


def get_weekly_stats(papers: List[Dict]) -> Dict:
    """
    Calculate statistics for papers added in the last 7 days

    Args:
        papers: List of paper dictionaries

    Returns:
        Dictionary with weekly statistics
    """
    # Calculate date 7 days ago
    week_ago = datetime.now() - timedelta(days=7)

    # Filter papers from last week
    weekly_papers = []
    for paper in papers:
        published_str = paper.get('published', '')
        if 'T' in published_str:
            # Remove timezone info if present
            published_str = published_str.split('+')[0].split('Z')[0]
        try:
            published_date = datetime.fromisoformat(published_str)
            if published_date >= week_ago:
                weekly_papers.append(paper)
        except (ValueError, TypeError):
            continue

    # Collect domains from weekly papers
    weekly_domains = []
    for paper in weekly_papers:
        weekly_domains.extend(paper.get('medical_domains', []))

    # Count domain frequencies
    domain_counts = Counter(weekly_domains)
    top_weekly_domains = domain_counts.most_common(3)

    return {
        'papers_this_week': len(weekly_papers),
        'top_domains': top_weekly_domains,  # [(domain, count), ...]
        'total_papers': len(papers),
        'weekly_papers': weekly_papers
    }


def format_domain_summary(top_domains: List[tuple]) -> str:
    """
    Format domain list for display

    Args:
        top_domains: List of (domain, count) tuples

    Returns:
        Formatted string like "Oncology (5), Radiology (3), Cardiology (2)"
    """
    if not top_domains:
        return "No domains"

    return ", ".join([f"{domain} ({count})" for domain, count in top_domains])
