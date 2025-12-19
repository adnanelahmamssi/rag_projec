from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from .config import Config
from .data_loader import DataLoader

class Indexer:
    def __init__(self):
        self.config = Config()
        self.embeddings = SentenceTransformerEmbeddings(model_name=self.config.EMBEDDING_MODEL)

    def create_index(self, documents):
        """Create and save FAISS index from documents."""
        vectorstore = FAISS.from_documents(documents, self.embeddings)
        vectorstore.save_local(self.config.VECTOR_DB_PATH)
        return vectorstore

    def load_index(self):
        """Load existing FAISS index."""
        return FAISS.load_local(
            self.config.VECTOR_DB_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    def build_index(self):
        """Full pipeline: load docs and build index."""
        loader = DataLoader()
        docs = loader.load_documents()
        return self.create_index(docs)