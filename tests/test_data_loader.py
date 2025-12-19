import pytest
from src.rag.data_loader import DataLoader

def test_data_loader_init():
    """Test DataLoader initialization."""
    loader = DataLoader()
    assert loader.config is not None
    assert loader.text_splitter is not None

def test_load_documents():
    """Test loading documents (may be empty if no files)."""
    loader = DataLoader()
    docs = loader.load_documents()
    assert isinstance(docs, list)