import uuid
from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel

class UserSession(BaseModel):
    session_id: str
    created_at: datetime
    last_active: datetime

class SessionManager:
    def __init__(self):
        # This dictionary lives in the server's memory to track active users
        self.sessions: Dict[str, UserSession] = {}

    def create_session(self) -> str:
        """Generates a new unique session ID."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = UserSession(
            session_id=session_id,
            created_at=datetime.now(),
            last_active=datetime.now()
        )
        return session_id

    def validate_session(self, session_id: str) -> bool:
        """Checks if a session ID exists and is still valid."""
        if session_id in self.sessions:
            self.sessions[session_id].last_active = datetime.now()
            return True
        return False

# Initialize a single manager to be used across the app
manager = SessionManager()