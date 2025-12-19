from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import Config

class DataLoader:
    def __init__(self):
        self.config = Config()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP
        )

    def load_documents(self):
        """Load all documents from the data directory."""
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
        return self.text_splitter.split_documents(documents)

    def load_pdf_documents(self):
        """Load PDF documents."""
        # For simplicity, assuming PDFs in data/pdfs
        pdf_loader = DirectoryLoader(
            "data/pdfs",
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents = pdf_loader.load()
        return self.text_splitter.split_documents(documents)