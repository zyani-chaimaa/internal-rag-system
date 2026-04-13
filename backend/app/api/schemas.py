from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- SESSION SCHEMAS ---
class SessionCreate(BaseModel):
    """What the frontend receives when a new session starts."""
    session_id: str
    created_at: datetime

# --- CHAT SCHEMAS ---
class ChatRequest(BaseModel):
    """What the frontend sends when a user asks a question."""
    question: str = Field(..., example="What is the total revenue in the Excel file?")
    session_id: str = Field(..., example="uuid-string-here")

class ChatResponse(BaseModel):
    """What the backend sends back to the user."""
    answer: str
    sources: List[str]
    session_id: str

# --- STATUS SCHEMAS ---
class SystemStatus(BaseModel):
    """To check if the API is actually awake and running."""
    status: str
    version: str
    active_sessions: int