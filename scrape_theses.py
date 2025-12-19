#!/usr/bin/env python3
"""
Script to scrape academic theses from ArXiv and download PDFs.
"""

import arxiv
import requests
import os
from pathlib import Path

def scrape_theses(query="deep learning", max_results=5):
    """
    Search and download theses from ArXiv.
    """
    # Create directories
    data_dir = Path("data/documents")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Search ArXiv
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    links = []
    for result in search.results():
        print(f"Downloading: {result.title}")
        try:
            # Download PDF
            pdf_url = result.pdf_url
            response = requests.get(pdf_url)
            filename = f"{result.entry_id.split('/')[-1]}_{result.title.replace(' ', '_')[:50]}.pdf"
            filepath = data_dir / filename

            with open(filepath, 'wb') as f:
                f.write(response.content)

            links.append(str(result.entry_id))
            print(f"Saved to: {filepath}")
        except Exception as e:
            print(f"Error downloading {result.title}: {e}")

    # Save links
    links_file = data_dir / "scraped_links.txt"
    with open(links_file, 'w') as f:
        for link in links:
            f.write(f"{link}\n")

    print(f"Downloaded {len(links)} theses. Links saved to {links_file}")

if __name__ == "__main__":
    # Example usage
    scrape_theses(query="evidential deep learning", max_results=5)