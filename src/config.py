"""
Configuration settings for the chatbot system.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

# ChromaDB Configuration
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
COLLECTION_NAME = "knowledge_base"

# Text-to-Speech Configuration
TTS_MODEL_NAME = "facebook/mms-tts-eng"  # Multilingual TTS model
AUDIO_OUTPUT_PATH = os.getenv("AUDIO_OUTPUT_PATH", "./audio_responses")

# Conversation Configuration
MAX_HISTORY_TURNS = 10
TOP_K_RESULTS = 3  # Number of relevant documents to retrieve from ChromaDB

# Paths
PROJECT_ROOT = Path(__file__).parent.parent  # Go up to Workshop_03 root
DATA_PATH = PROJECT_ROOT / "data"
CONVERSATION_LOGS_PATH = PROJECT_ROOT / "src" / "conversation_logs"

# Create necessary directories
Path(CHROMA_DB_PATH).mkdir(exist_ok=True)
Path(AUDIO_OUTPUT_PATH).mkdir(exist_ok=True)
Path(DATA_PATH).mkdir(exist_ok=True)
Path(CONVERSATION_LOGS_PATH).mkdir(exist_ok=True)

# Validate configuration
def validate_config():
    """Validate that required configuration is present."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY not found. Please set it in your .env file."
        )
    return True
