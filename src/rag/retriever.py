from langchain_community.retrievers import BM25Retriever
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .config import Config
from .indexer import Indexer
from .data_loader import DataLoader
import logging
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Retriever:
    """Retriever class for RAG system using vector search and LLM."""

    def __init__(self) -> None:
        """Initialize the Retriever with config, indexer, and LLM."""
        self.config = Config()
        self.config.validate()  # Validate configuration
        self.indexer = Indexer()
        self.data_loader = DataLoader()
        try:
            self.vectorstore = self.indexer.load_index()
            logger.info("Vectorstore loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load vectorstore: {e}")
            raise
        self.llm = ChatOpenAI(
            model_name=self.config.LLM_MODEL,
            openai_api_key=self.config.GROQ_API_KEY,
            base_url=self.config.BASE_URL,
            temperature=0  # Reduce creativity
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        # Initialize BM25 for hybrid search
        self.bm25_retriever = None
        self._init_bm25()

    def _init_bm25(self) -> None:
        """Initialize BM25 retriever for hybrid search."""
        try:
            docs = self.data_loader.load_documents()
            if docs:
                self.bm25_retriever = BM25Retriever.from_documents(docs)
                self.bm25_retriever.k = 3
                logger.info("BM25 retriever initialized.")
        except Exception as e:
            logger.warning(f"Failed to initialize BM25: {e}")

    def hybrid_search(self, question: str, k: int = 3) -> List:
        """Perform hybrid search using both vector and BM25."""
        vector_docs = self.retriever.invoke(question)
        bm25_docs = self.bm25_retriever.invoke(question) if self.bm25_retriever else []
        
        # Combine and deduplicate
        seen = set()
        combined = []
        for doc in vector_docs + bm25_docs:
            if doc.page_content not in seen:
                combined.append(doc)
                seen.add(doc.page_content)
        return combined[:k]

    def query(self, question: str, use_hybrid: bool = False) -> str:
        """Answer a question using RAG.

        Args:
            question: The question to answer.
            use_hybrid: Whether to use hybrid search (vector + BM25).

        Returns:
            The generated answer.
        """
        # Get relevant documents
        if use_hybrid and self.bm25_retriever:
            docs = self.hybrid_search(question)
        else:
            docs = self.retriever.invoke(question)
        
        # Structure context with metadata
        context_parts = []
        for doc in docs:
            meta = doc.metadata
            title = meta.get('title', 'Unspecified Title')
            authors = meta.get('author', 'Unspecified Authors')
            year = meta.get('creationdate', '')[:4] if meta.get('creationdate') else 'Unspecified Year'
            context_parts.append(f"Title: {title}\nAuthors: {authors}\nYear: {year}\nContent: {doc.page_content}")
        context = "\n\n".join(context_parts)

        # Create prompt
        prompt = self.config.PROMPT_TEMPLATE.format(context=context, question=question)

        # Generate response
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            logger.info(f"Generated answer for question: {question[:50]}...")
            return response.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "An error occurred while generating the answer."