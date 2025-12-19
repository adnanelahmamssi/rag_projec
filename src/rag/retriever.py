from langchain_community.retrievers import BM25Retriever
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .config import Config
from .indexer import Indexer
from .data_loader import DataLoader

class Retriever:
    def __init__(self):
        self.config = Config()
        self.indexer = Indexer()
        self.data_loader = DataLoader()
        self.vectorstore = self.indexer.load_index()
        self.llm = ChatOpenAI(
            model_name=self.config.LLM_MODEL,
            openai_api_key=self.config.GROQ_API_KEY,
            base_url=self.config.BASE_URL,
            temperature=0  # Reduce creativity
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    def query(self, question):
        """Answer a question using RAG."""
        # Get relevant documents
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
        prompt = f"""You are an expert in deep learning and mathematics. Answer the question directly and concisely using only the provided context. Base your answer on the context, paraphrase or quote where appropriate, and include citations [Authors, Year].

If the context does not contain information to answer the question, say "The provided context does not contain the answer to this question."

Context:
{context}

Question: {question}

Direct Answer:"""

        # Generate response
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content