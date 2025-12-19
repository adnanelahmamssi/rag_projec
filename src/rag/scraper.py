import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import arxiv
from pypdf import PdfReader
import time
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ThesisScraper:
    """Scraper for academic theses from ArXiv and HAL."""

    def __init__(self, base_dir: str = "data/documents") -> None:
        """Initialize the scraper with base directory."""
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def scrape_arxiv(self, query: str, max_results: int = 5) -> List[Dict]:
        """Scrape papers from ArXiv with retries."""
        papers = []
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            for result in search.results():
                try:
                    import re
                    safe_title = re.sub(r'[^\w\-_\. ]', '_', result.title)
                    pdf_filename = f"{result.entry_id.split('/')[-1]}_{safe_title[:50]}.pdf"
                    pdf_path = os.path.join(self.base_dir, pdf_filename)
                    
                    # Download with retry
                    self._download_with_retry(result.pdf_url, pdf_path)
                    
                    papers.append({
                        "title": result.title,
                        "authors": [str(a) for a in result.authors],
                        "year": result.published.year,
                        "pdf_path": pdf_path,
                        "abstract": result.summary,
                        "link": result.entry_id
                    })
                    time.sleep(1)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error downloading {result.title}: {e}")
        except Exception as e:
            logger.error(f"Error in ArXiv search: {e}")
        return papers

    def _download_with_retry(self, url: str, path: str, retries: int = 3) -> None:
        """Download file with retries."""
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                with open(path, 'wb') as f:
                    f.write(response.content)
                return
            except Exception as e:
                logger.warning(f"Download attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        raise Exception(f"Failed to download after {retries} attempts")

    def scrape_hal(self, query: str, max_results: int = 5) -> List[Dict]:
        """Scrape from HAL (Hyper Articles en Ligne) with error handling."""
        base_url = "https://hal.archives-ouvertes.fr/search/"
        params = {
            "q": query + " thesis",
            "rows": max_results
        }
        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            papers = []
            for item in soup.find_all('div', class_='result-item'):
                try:
                    title_tag = item.find('h3')
                    if title_tag:
                        title = title_tag.text.strip()
                        link = title_tag.find('a')['href'] if title_tag.find('a') else None
                        if link and link.endswith('.pdf'):
                            pdf_url = urljoin(base_url, link)
                            pdf_name = os.path.basename(link)
                            pdf_path = os.path.join(self.base_dir, pdf_name)
                            self._download_with_retry(pdf_url, pdf_path)
                            # Extract metadata (simplified)
                            authors = item.find('span', class_='authors').text.strip() if item.find('span', class_='authors') else "Unknown"
                            year = item.find('span', class_='year').text.strip() if item.find('span', class_='year') else "Unknown"
                            papers.append({
                                "title": title,
                                "authors": authors.split(', '),
                                "year": year,
                                "pdf_path": pdf_path,
                                "link": pdf_url
                            })
                            time.sleep(1)
                except Exception as e:
                    logger.error(f"Error processing HAL item: {e}")
            return papers
        except Exception as e:
            logger.error(f"Error scraping HAL: {e}")
            return []

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return ""

    def scrape_and_process(self, query: str, source: str = "arxiv", max_results: int = 5) -> List[Dict]:
        """Scrape and process documents."""
        if source == "arxiv":
            papers = self.scrape_arxiv(query, max_results)
        elif source == "hal":
            papers = self.scrape_hal(query, max_results)
        else:
            raise ValueError("Source not supported")

        processed = []
        try:
            with open(os.path.join(self.base_dir, "scraped_links.txt"), "a") as f:
                for paper in papers:
                    text = self.extract_text_from_pdf(paper["pdf_path"])
                    processed.append({
                        "content": text,
                        "metadata": {
                            "title": paper["title"],
                            "authors": paper["authors"],
                            "year": paper["year"],
                            "source": source
                        }
                    })
                    # Save link
                    link = paper["link"]
                    f.write(f"{link}\n")
        except Exception as e:
            logger.error(f"Error processing papers: {e}")
        return processed