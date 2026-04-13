from fastapi import Header, HTTPException, Depends
from backend.app.core.session import manager

def get_valid_session(session_id: str = Header(None)):
    """
    This function acts as a 'Check-In' desk.
    It ensures the user actually has a valid session before they can talk to the RAG.
    """
    if not session_id or not manager.validate_session(session_id):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired session. Please refresh the page."
        )
    return session_id