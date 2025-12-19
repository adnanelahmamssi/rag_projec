from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import Config
from typing import List
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """DataLoader class for loading and splitting documents."""

    def __init__(self) -> None:
        """Initialize the DataLoader with text splitter."""
        self.config = Config()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP
        )

    def load_documents(self) -> List:
        """Load all documents from the data directory.

        Returns:
            List of split documents.
        """
        try:
            # Load PDFs
            pdf_loader = DirectoryLoader(
                self.config.DATA_DIR,
                glob="**/*.pdf",
                loader_cls=PyMuPDFLoader
            )
            pdf_documents = pdf_loader.load()

            # Optionally load text files if any
            text_loader = DirectoryLoader(
                self.config.DATA_DIR,
                glob="**/*.txt",
                loader_cls=TextLoader
            )
            text_documents = text_loader.load()

            documents = pdf_documents + text_documents
            logger.info(f"Loaded {len(pdf_documents)} PDFs and {len(text_documents)} text files.")
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            return []

    def load_pdf_documents(self) -> List:
        """Load PDF documents.

        Returns:
            List of split PDF documents.
        """
        # For simplicity, assuming PDFs in data/pdfs
        try:
            pdf_loader = DirectoryLoader(
                "data/pdfs",
                glob="**/*.pdf",
                loader_cls=PyMuPDFLoader
            )
            documents = pdf_loader.load()
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            logger.error(f"Error loading PDF documents: {e}")
            return []