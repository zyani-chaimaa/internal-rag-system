from src.vectorstore.chroma_store import VectorStore
from src.config import TOP_K_RESULTS
from src.utils.logger import log

def get_relevant_context(query: str, db: VectorStore) -> str:
    """Fetches text from the DB and formats it into a single string for Claude."""
    results = db.query(query, n_results=TOP_K_RESULTS)
   
    context_parts = []
    # results['documents'][0] contains the list of text chunks found
    # results['metadatas'][0] contains info about which file they came from
    for text, meta in zip(results['documents'][0], results['metadatas'][0]):
        source_info = f"[Source: {meta['source']}]"
        context_parts.append(f"{source_info}\n{text}")
   
    # Combine all chunks into one big string for the AI to read
    full_context = "\n\n---\n\n".join(context_parts)
    log.info(f"Retrieved {len(context_parts)} context chunks.")
    return full_context