# Advanced RAG System Project

A comprehensive Retrieval-Augmented Generation (RAG) system built with LangChain for educational purposes. This project demonstrates advanced concepts in AI, NLP, and information retrieval.

## Project Overview

This RAG system allows users to query a knowledge base of AI and machine learning documents through a web interface. It features document indexing, semantic search, and generative question answering.

## Architecture

```
src/rag/
├── __init__.py          # Package initialization
├── config.py            # Configuration settings
├── data_loader.py       # Document loading and preprocessing (PDF/text)
├── indexer.py           # Vector indexing with FAISS
├── retriever.py         # Query processing and answer generation
├── scraper.py           # Thesis scraping from academic sources
└── evaluator.py         # Performance evaluation metrics

data/
├── documents/           # Scraped PDFs and source documents
└── vectorstore/         # FAISS vector database (generated)

tests/                   # Unit tests
scrape_theses.py         # Scraping script
app.py                  # Streamlit web interface
build_index.py          # Index building script
```

## Features

- **Thesis Scraping**: Automatically scrape and download thesis PDFs from academic repositories (ArXiv, HAL)
- **PDF Support**: Load and index PDF documents with text extraction
- **Multi-document Support**: Handle multiple PDF and text documents
- **Semantic Search**: FAISS-based vector similarity search
- **Hybrid Search**: Combine vector and keyword-based search (BM25)
- **Generative QA**: Groq LLM integration for answer generation
- **Academic Citations**: Responses include in-text citations from document metadata
- **Web Interface**: Streamlit-based user interface with evaluation metrics
- **Evaluation Metrics**: Built-in performance evaluation with RAGAS
- **Modular Design**: Clean separation of concerns
- **Extensible**: Easy to add new document types and sources

## Setup Instructions

### Prerequisites
- Python 3.8+
- Groq API key

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag_projec
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

4. Build the vector index:
   ```bash
   python build_index.py
   ```

5. Run the web application:
   ```bash
   streamlit run app.py
   ```

## Usage

### Web Interface
- Open the Streamlit app in your browser
- Enter questions about AI, machine learning, NLP, computer vision, or deep learning
- Choose between standard vector search or hybrid search (vector + keyword)
- View generated answers and evaluation metrics

### Programmatic Usage
```python
from src.rag.retriever import Retriever

retriever = Retriever()
answer = retriever.query("What is deep learning?")
print(answer)
```

## Document Management

Add new documents by scraping theses:
```bash
python scrape_theses.py "machine learning" arxiv 5
```

This will scrape 5 theses from ArXiv related to "machine learning", download PDFs, extract text, and rebuild the index.

Supported sources: arxiv, hal

Rebuild the index after manual additions:
```bash
python build_index.py
```

## Testing

Run the test suite:
```bash
pytest tests/
```

## Configuration

Modify `src/rag/config.py` to adjust:
- Embedding model
- LLM model
- Chunk size and overlap
- Data directories

## Evaluation

The system includes evaluation metrics for:
- Retrieval precision, recall, and F1-score
- Generation quality (Jaccard similarity, response length)

## Security

- API keys are stored in `.env` file (not committed to version control)
- Use strong, unique API keys for production
- Regularly rotate API keys
- Never share `.env` files or commit them to repositories

## Technologies Used

- **LangChain**: Framework for LLM applications
- **Groq**: Embeddings and language models
- **FAISS**: Vector similarity search
- **Streamlit**: Web interface
- **Scikit-learn**: Evaluation metrics
- **Python**: Core programming language

## Academic Context

This project serves as a comprehensive example of modern AI system design, covering:
- Information retrieval
- Natural language processing
- Vector databases
- Web application development
- Software engineering best practices

## License

This project is for educational purposes.