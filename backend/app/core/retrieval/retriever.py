from backend.app.core.vectorstore.chroma_store import VectorStore
from backend.app.core.config import TOP_K_RESULTS
from backend.app.core.utils.logger import log
from typing import List

from typing import List
from backend.app.core.vectorstore.chroma_store import VectorStore

def get_relevant_context(query: str, db: VectorStore, session_id: str, n_results: int = 5) -> str:
    """
    Fetches the most relevant chunks specifically for the given session_id.
    """
    # Pass the session_id to the db.query method we updated earlier
    results = db.query(query, session_id=session_id, n_results=n_results)
   
    # Extract the text from the results
    # results['documents'] is usually a list of lists: [[doc1, doc2...]]
    if results and results.get('documents'):
        context_chunks = results['documents'][0]
        return "\n\n".join(context_chunks)
   
    return ""