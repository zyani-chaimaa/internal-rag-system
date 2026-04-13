from fastapi import APIRouter
from backend.app.core.session import manager
from backend.app.api.schemas import SessionCreate
from datetime import datetime

router = APIRouter(prefix="/session", tags=["Session Management"])

@router.post("/start", response_model=SessionCreate)
async def start_session():
    """Endpoint to initialize a new user session."""
    new_id = manager.create_session()
    return {
        "session_id": new_id,
        "created_at": datetime.now()
    }