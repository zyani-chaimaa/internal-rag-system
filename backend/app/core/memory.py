from typing import List, Dict
from collections import defaultdict

class ChatMemory:
    def __init__(self, max_history: int = 10):
        # We use a dictionary where the Key is the Session ID
        # and the Value is a list of messages.
        self.user_histories = defaultdict(list)
        self.max_history = max_history

    def add_message(self, session_id: str, role: str, content: str):
        """Adds a message to a specific user's history."""
        self.user_histories[session_id].append({"role": role, "content": content})
       
        # Keep only the last X messages so the AI doesn't get confused
        if len(self.user_histories[session_id]) > self.max_history:
            self.user_histories[session_id] = self.user_histories[session_id][-self.max_history:]

    def get_history(self, session_id: str) -> List[Dict]:
        """Retrieves the history for a specific user."""
        return self.user_histories[session_id]

    def clear_history(self, session_id: str):
        """Wipes the memory for one specific user."""
        if session_id in self.user_histories:
            del self.user_histories[session_id]

# Initialize a single memory bank
memory = ChatMemory()