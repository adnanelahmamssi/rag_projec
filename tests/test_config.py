import pytest
from src.rag.config import Config

def test_config_validation():
    """Test that config validation raises error if API key is missing."""
    # Temporarily unset the key
    original_key = Config.GROQ_API_KEY
    Config.GROQ_API_KEY = None
    try:
        with pytest.raises(ValueError, match="GROQ_API_KEY not found"):
            Config.validate()
    finally:
        Config.GROQ_API_KEY = original_key

def test_config_attributes():
    """Test that config has required attributes."""
    assert hasattr(Config, 'GROQ_API_KEY')
    assert hasattr(Config, 'DATA_DIR')
    assert hasattr(Config, 'VECTOR_DB_PATH')
    assert Config.CHUNK_SIZE == 1000