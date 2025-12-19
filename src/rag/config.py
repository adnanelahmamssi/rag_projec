import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DATA_DIR = "data/documents"
    VECTOR_DB_PATH = "data/vectorstore"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 0
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # SentenceTransformer model
    LLM_MODEL = "llama-3.1-8b-instant"
    BASE_URL = "https://api.groq.com/openai/v1"
    PROMPT_TEMPLATE = """You are an expert in deep learning and mathematics. Answer the question directly and concisely using only the provided context. Base your answer on the context, paraphrase or quote where appropriate, and include citations [Authors, Year].

If the context does not contain information to answer the question, say "The provided context does not contain the answer to this question."

Context:
{context}

Question: {question}

Direct Answer:"""

    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in .env file.")
        return True