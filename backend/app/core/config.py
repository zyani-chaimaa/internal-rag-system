import os
from pathlib import Path
from dotenv import load_dotenv

# Load the .env file 
load_dotenv()

# Project Paths 
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"
LOGS_DIR = BASE_DIR / "logs"

# Ensure folders exist 
for d in [UPLOADS_DIR, VECTORSTORE_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# API & Model Config 
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
EMBED_MODEL = "all-MiniLM-L6-v2" # The free local model 

# RAG Settings 
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE",800))     # Size of each text piece 
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP",100))  # Overlap to keep context 
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS",5))    # How many chunks to show Claude 
MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS",10))
CHROMA_COLLECTION = "rag_documents" # collection name in chromaDB
SUPPORTED_TYPES = [".pdf", ".xlsx", ".xls", ".csv"] #Supported file types