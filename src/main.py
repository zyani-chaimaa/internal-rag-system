from src.ingestion.pdf_loader import load_pdf
from src.ingestion.excel_loader import load_spreadsheet
from src.ingestion.processor import split_documents
from src.vectorstore.chroma_store import VectorStore
from src.retrieval.retriever import get_relevant_context
from src.llm.claude_client import ClaudeClient
from src.utils.logger import log

class RAGSystem:
    def __init__(self):
        self.db = VectorStore()
        self.llm = ClaudeClient()

    def ingest_file(self, file_path):
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
        self.db.add_documents(chunks)
        log.info(f"Successfully ingested {file_path.name}")

    def ask(self, question: str, history: list = None) -> str:
        """The full pipeline: Query DB -> Get Context -> Ask Claude"""
        context = get_relevant_context(question, self.db)
        if not context:
            return "No relevant documents found."
       
        answer = self.llm.generate_answer(question, context, history)
        return answer
