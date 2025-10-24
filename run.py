#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv Health Monitor - Main Script

Fetches, filters, summarizes, and publishes medical/health papers from arXiv.
"""
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from src.arxiv_client import ArxivHealthClient
from src.ai_summarizer import AISummarizer
from src.database import PaperDatabase
from src.website_generator import WebsiteGenerator


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='Fetch and summarize medical/health papers from arXiv'
    )
    parser.add_argument(
        '--max-results',
        type=int,
        default=config.MAX_RESULTS_PER_RUN,
        help=f'Maximum number of papers to fetch (default: {config.MAX_RESULTS_PER_RUN})'
    )
    parser.add_argument(
        '--days-back',
        type=int,
        default=config.DAYS_TO_LOOK_BACK,
        help=f'Number of days to look back (default: {config.DAYS_TO_LOOK_BACK})'
    )
    parser.add_argument(
        '--provider',
        type=str,
        choices=['gemini', 'openai', 'claude', 'grok'],
        default=config.AI_PROVIDER,
        help=f'AI provider for summarization (default: {config.AI_PROVIDER})'
    )
    parser.add_argument(
        '--skip-download',
        action='store_true',
        help='Skip PDF downloads (only fetch metadata and summaries)'
    )
    parser.add_argument(
        '--rebuild-site',
        action='store_true',
        help='Rebuild website without fetching new papers'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("arXiv Health Monitor")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"AI Provider: {args.provider}")
    print(f"Max Results: {args.max_results}")
    print(f"Days Back: {args.days_back}")
    print("=" * 70)
    print()

    # Initialize components
    db = PaperDatabase()
    arxiv_client = ArxivHealthClient()

    if args.rebuild_site:
        print("Rebuilding website from existing database...")
        papers = db.get_all_papers()
        stats = db.get_statistics()

        website_gen = WebsiteGenerator()
        website_gen.generate_website(papers, stats)

        print("\n" + "=" * 70)
        print("Website rebuilt successfully!")
        print(f"Total papers: {len(papers)}")
        print(f"Website: {config.WEBSITE_DIR / 'index.html'}")
        print("=" * 70)
        return

    # Initialize AI summarizer
    try:
        summarizer = AISummarizer(provider=args.provider)
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please check your .env file and ensure the API key is set.")
        sys.exit(1)

    # Fetch papers from arXiv
    print("\n[1/4] Fetching papers from arXiv...")
    print("-" * 70)
    papers = arxiv_client.fetch_recent_papers(
        max_results=args.max_results,
        days_back=args.days_back
    )

    if not papers:
        print("No papers found. Exiting.")
        return

    # Process each paper
    print(f"\n[2/4] Processing {len(papers)} papers...")
    print("-" * 70)

    new_papers = 0
    skipped_papers = 0
    irrelevant_papers = 0

    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] {paper['title'][:70]}...")

        # Check if already processed
        if db.paper_exists(paper['arxiv_id']):
            print(f"  [SKIP] Already in database, skipping")
            skipped_papers += 1
            continue

        # Check relevance with AI
        print(f"  Checking medical/health relevance...")
        is_relevant, score, reasoning, domains, ai_app = summarizer.check_relevance(paper)

        if not is_relevant or score < config.MIN_RELEVANCE_SCORE:
            print(f"  [REJECT] Not relevant (score: {score:.2f})")
            print(f"    Reason: {reasoning}")
            irrelevant_papers += 1
            continue

        print(f"  [OK] Relevant! Score: {score:.2f}")
        print(f"    Domains: {', '.join(domains)}")

        # Generate summary
        print(f"  Generating AI summary...")
        summary = summarizer.summarize_paper(paper)

        # Download PDF
        if not args.skip_download:
            print(f"  Downloading PDF...")
            pdf_path = arxiv_client.download_pdf(paper)
            paper['pdf_path'] = pdf_path

        # Add to database
        relevance_info = {
            'relevance_score': score,
            'reasoning': reasoning,
            'ai_health_application': ai_app
        }
        db.add_paper(paper, summary, relevance_info)
        new_papers += 1

        print(f"  [DONE] Paper processed and added to database")

    # Generate website
    print(f"\n[3/4] Generating website...")
    print("-" * 70)

    papers = db.get_all_papers()
    stats = db.get_statistics()

    website_gen = WebsiteGenerator()
    website_gen.generate_website(papers, stats)

    # Update metadata
    db.update_last_run()

    # Summary
    print("\n[4/4] Summary")
    print("=" * 70)
    print(f"Papers fetched from arXiv: {len(papers)}")
    print(f"New papers added: {new_papers}")
    print(f"Skipped (already in DB): {skipped_papers}")
    print(f"Rejected (not relevant): {irrelevant_papers}")
    print(f"\nTotal papers in database: {stats['total_papers']}")
    print(f"Medical domains: {len(stats['domains'])}")
    print(f"\nTop 5 domains:")
    for domain, count in stats['top_domains'][:5]:
        print(f"  - {domain}: {count} papers")

    print(f"\nWebsite generated at: {config.WEBSITE_DIR}")
    print(f"  → Open: {config.WEBSITE_DIR / 'index.html'}")
    print(f"\nPDFs saved in: {config.PAPERS_DIR}")

    print("\n" + "=" * 70)
    print("[SUCCESS] Complete!")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Close database
    db.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
