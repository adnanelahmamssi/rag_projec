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