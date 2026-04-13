from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.app.core.config import CHUNK_SIZE, CHUNK_OVERLAP
from backend.app.core.utils.logger import log

def split_documents(raw_docs: List[Dict]) -> List[Dict]:
    """Break documents into smaller chunks for the vector store."""
    log.info(f"Splitting {len(raw_docs)} document pages/rows into chunks...")
   
    # This splitter is smart: it tries to split at paragraphs, then sentences
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
   
    final_chunks = []
    for doc in raw_docs:
        texts = splitter.split_text(doc["text"])
        for i, text in enumerate(texts):
            # Create a new chunk that keeps the original file name and page number
            chunk = doc.copy()
            chunk["text"] = text
            chunk["chunk_id"] = f"{doc['source']}_p{doc.get('page', '0')}_c{i}"
            final_chunks.append(chunk)
           
    log.info(f"Created {len(final_chunks)} total text chunks.")
    return final_chunks