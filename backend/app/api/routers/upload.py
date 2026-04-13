from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Header
from backend.app.api.dependencies import get_valid_session
from backend.app.core.ingestion.pdf_loader import load_pdf
from backend.app.core.ingestion.processor import split_documents
from backend.app.core.vectorstore.chroma_store import VectorStore
from backend.app.core.session import manager
from pathlib import Path
import shutil

router = APIRouter(prefix="/upload", tags=["Document Management"])
db = VectorStore()

@router.post("/file")
async def upload_document(
    file: UploadFile = File(...),
    session_id: str = Header(None)
):
    if not session_id or not manager.validate_session(session_id):
        raise HTTPException(status_code=401, detail="Invalid session ID in Header")

    """Uploads and indexes a document for a specific user."""
   
    # 1. Create a private temp folder for this session
    upload_path = Path(f"data/uploads/{session_id}")
    upload_path.mkdir(parents=True, exist_ok=True)
   
    file_path = upload_path / file.filename
   
    # 2. Save file locally
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
           
        # 3. Process based on type (extending our old loaders)
        if file.filename.endswith(".pdf"):
            raw_docs = load_pdf(file_path)
            chunks = split_documents(raw_docs)
           
            # 4. Add to the USER'S private database collection
            db.add_documents(chunks, session_id=session_id)
           
            return {"filename": file.filename, "chunks_indexed": len(chunks)}
        else:
            raise HTTPException(status_code=400, detail="Only PDFs are supported in this version.")
           
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))