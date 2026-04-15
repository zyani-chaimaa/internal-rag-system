from backend.app.core.ingestion.pdf_loader import load_pdf
from backend.app.core.ingestion.excel_loader import load_spreadsheet
from backend.app.core.ingestion.processor import split_documents
from backend.app.core.vectorstore.chroma_store import VectorStore
from backend.app.core.retrieval.retriever import get_relevant_context
from backend.app.core.llm.claude_client import ClaudeClient
from backend.app.core.utils.logger import log

class RAGSystem:
    def __init__(self):
        self.db = VectorStore()
        self.llm = ClaudeClient()

    def ingest_file(self, file_path, session_id: str):
        """The full pipeline: Load -> Split -> Store"""
        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            raw_docs = load_pdf(file_path)
        elif suffix in [".csv", ".xlsx", ".xls"]:
            raw_docs = load_spreadsheet(file_path)
        else:
            log.warning(f"Unsupported file type: {suffix}")
            return

        chunks = split_documents(raw_docs)
        self.db.add_documents(chunks, session_id)
        log.info(f"Successfully ingested {file_path.name} for session {session_id}")

    def ask(self, question: str, session_id: str, history: list = None) -> str:
        """The full pipeline: Query DB -> Get Context -> Ask Claude"""
        context = get_relevant_context(question, self.db, session_id)
        if not context:
            return "No relevant documents found. Please upload and index a file first."

        answer = self.llm.generate_answer(question, context, history=history)
        return answer

    def get_doc_count(self, session_id: str) -> int:
        """Returns the number of indexed chunks for this session."""
        return self.db.get_count(session_id)
