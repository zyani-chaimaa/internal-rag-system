import chromadb
from chromadb.utils import embedding_functions
from src.config import VECTORSTORE_DIR, EMBED_MODEL
from src.utils.logger import log
from typing import List, Dict

class VectorStore:
    def __init__(self):
        # 1. Initialize the embedding function (the "Translator" from text to numbers)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBED_MODEL
        )
       
        # 2. Set up the database on your hard drive
        self.client = chromadb.PersistentClient(path=str(VECTORSTORE_DIR))
       
        # 3. Create or get the "Collection" (like a table in a database)
        self.collection = self.client.get_or_create_collection(
            name="rag_documents",
            embedding_function=self.embedding_fn
        )
        log.info(f"Vector Store initialized at {VECTORSTORE_DIR}")

    def add_documents(self, chunks: List[Dict]):
        """Store text chunks and their metadata in the database."""
        ids = [c["chunk_id"] for c in chunks]
        texts = [c["text"] for c in chunks]
        # Metadata allows us to tell the user which file/page the info came from
        metadatas = [{k: v for k, v in c.items() if k != "text"} for c in chunks]

        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        log.info(f"Added {len(chunks)} chunks to the vector store.")

    def query(self, query_text: str, n_results: int = 5):
        """Search for the most relevant chunks based on a question."""
        log.info(f"Searching for: {query_text}")
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

    def get_count(self):
        """Returns how many items are in our database."""
        return self.collection.count()
