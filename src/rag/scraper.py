import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import arxiv
from pypdf import PdfReader
import time

class ThesisScraper:
    def __init__(self, base_dir="data/documents"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def scrape_arxiv(self, query, max_results=5):
        """Scrape papers from ArXiv."""
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        papers = []
        for result in search.results():
            try:
                import re
                safe_title = re.sub(r'[^\w\-_\. ]', '_', result.title)
                pdf_filename = f"{result.entry_id.split('/')[-1]}_{safe_title[:50]}.pdf"
                result.download_pdf(dirpath=self.base_dir, filename=pdf_filename)
                pdf_path = os.path.join(self.base_dir, pdf_filename)
                papers.append({
                    "title": result.title,
                    "authors": [str(a) for a in result.authors],
                    "year": result.published.year,
                    "pdf_path": pdf_path,
                    "abstract": result.summary,
                    "link": result.entry_id
                })
                time.sleep(1)
            except Exception as e:
                print(f"Error downloading {result.title}: {e}")
        return papers

    def scrape_hal(self, query, max_results=5):
        """Scrape from HAL (Hyper Articles en Ligne)."""
        base_url = "https://hal.archives-ouvertes.fr/search/"
        params = {
            "q": query + " thesis",
            "rows": max_results
        }
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        papers = []
        for item in soup.find_all('div', class_='result-item'):
            title_tag = item.find('h3')
            if title_tag:
                title = title_tag.text.strip()
                link = title_tag.find('a')['href'] if title_tag.find('a') else None
                if link and link.endswith('.pdf'):
                    pdf_url = urljoin(base_url, link)
                    pdf_response = requests.get(pdf_url)
                    pdf_name = os.path.basename(link)
                    pdf_path = os.path.join(self.base_dir, pdf_name)
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_response.content)
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
        return papers

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF."""
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def scrape_and_process(self, query, source="arxiv", max_results=5):
        """Scrape and process documents."""
        if source == "arxiv":
            papers = self.scrape_arxiv(query, max_results)
        elif source == "hal":
            papers = self.scrape_hal(query, max_results)
        else:
            raise ValueError("Source not supported")

        processed = []
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
        return processed