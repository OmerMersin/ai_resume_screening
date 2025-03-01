import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Flask settings
FLASK_ENV = os.getenv("FLASK_ENV", "production")
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5001))

# File constraints
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 16))
ALLOWED_EXT = os.getenv("ALLOWED_EXTENSIONS", "pdf,txt").split(",")

# SpaCy NER model
SPACY_MODEL_PATH = os.getenv("SPACY_MODEL_PATH", "en_core_web_trf")

# Transformer model (for similarity)
TRANSFORMER_MODEL_NAME = os.getenv("TRANSFORMER_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
POOLING_STRATEGY = os.getenv("POOLING_STRATEGY", "mean")

# Summarization (Optional)
SUMMARIZATION_MODEL_NAME = os.getenv("SUMMARIZATION_MODEL_NAME", "facebook/bart-large-cnn")