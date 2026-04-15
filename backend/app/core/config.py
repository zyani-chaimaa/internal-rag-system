import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Load .env for local development (no-op on Streamlit Cloud)
load_dotenv()

# Project Paths — use /tmp so writes work on Streamlit Cloud (ephemeral storage is fine)
_TMP = Path(tempfile.gettempdir())
VECTORSTORE_DIR = _TMP / "rag_vectorstore"
UPLOADS_DIR = _TMP / "rag_uploads"
LOGS_DIR = _TMP / "rag_logs"

# Ensure folders exist
for d in [UPLOADS_DIR, VECTORSTORE_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# API & Model Config
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
EMBED_MODEL = "all-MiniLM-L6-v2"

# RAG Settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 5))
MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS", 10))
CHROMA_COLLECTION = "rag_documents"
SUPPORTED_TYPES = [".pdf", ".xlsx", ".xls", ".csv"]
