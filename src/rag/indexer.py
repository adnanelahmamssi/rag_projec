from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from .config import Config
from .data_loader import DataLoader
from typing import List
import logging

logger = logging.getLogger(__name__)

class Indexer:
    """Indexer class for creating and loading FAISS vector stores."""

    def __init__(self) -> None:
        """Initialize the Indexer with embeddings."""
        self.config = Config()
        self.embeddings = SentenceTransformerEmbeddings(model_name=self.config.EMBEDDING_MODEL)

    def create_index(self, documents: List) -> FAISS:
        """Create and save FAISS index from documents.

        Args:
            documents: List of documents to index.

        Returns:
            The created FAISS vectorstore.
        """
        vectorstore = FAISS.from_documents(documents, self.embeddings)
        vectorstore.save_local(self.config.VECTOR_DB_PATH)
        logger.info(f"Index saved to {self.config.VECTOR_DB_PATH}")
        return vectorstore

    def load_index(self) -> FAISS:
        """Load existing FAISS index.

        Returns:
            The loaded FAISS vectorstore.
        """
        try:
            vectorstore = FAISS.load_local(
                self.config.VECTOR_DB_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info("Index loaded successfully.")
            return vectorstore
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            raise

    def build_index(self) -> FAISS:
        """Full pipeline: load docs and build index.

        Returns:
            The built FAISS vectorstore.
        """
        loader = DataLoader()
        docs = loader.load_documents()
        logger.info(f"Loaded {len(docs)} documents.")
        return self.create_index(docs)