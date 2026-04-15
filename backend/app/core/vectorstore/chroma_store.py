import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from backend.app.core.config import VECTORSTORE_DIR
from backend.app.core.utils.logger import log
from typing import List, Dict

class VectorStore:
    def __init__(self):
        # DefaultEmbeddingFunction uses ONNX (no PyTorch needed) — works on Streamlit Cloud
        self.embedding_fn = DefaultEmbeddingFunction()

        self.client = chromadb.PersistentClient(path=str(VECTORSTORE_DIR))
        log.info(f"Vector Store initialized at {VECTORSTORE_DIR}")

    def _get_user_collection(self, session_id: str):
        """Each user session gets its own isolated collection."""
        safe_name = f"user_{session_id.replace('-', '_')}"
        return self.client.get_or_create_collection(
            name=safe_name,
            embedding_function=self.embedding_fn
        )

    def add_documents(self, chunks: List[Dict], session_id: str):
        """Store text chunks in the user's private collection."""
        collection = self._get_user_collection(session_id)

        ids = [c["chunk_id"] for c in chunks]
        texts = [c["text"] for c in chunks]
        metadatas = [{k: v for k, v in c.items() if k != "text"} for c in chunks]

        collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        log.info(f"Added {len(chunks)} chunks for session: {session_id}")

    def query(self, query_text: str, session_id: str, n_results: int = 5):
        """Search only the collection belonging to this session_id."""
        log.info(f"Searching session {session_id} for: {query_text}")
        collection = self._get_user_collection(session_id)

        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

    def get_count(self, session_id: str):
        """Returns how many items this specific user has indexed."""
        collection = self._get_user_collection(session_id)
        return collection.count()

    def delete_user_data(self, session_id: str):
        """Allows a user to wipe their own data without affecting others."""
        safe_name = f"user_{session_id.replace('-', '_')}"
        try:
            self.client.delete_collection(name=safe_name)
            log.info(f"Deleted collection for session: {session_id}")
        except Exception as e:
            log.error(f"Could not delete collection {safe_name}: {e}")
