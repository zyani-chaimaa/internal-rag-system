import anthropic
from src.config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from src.utils.logger import log

# This is the "brain" instruction for the AI
RAG_SYSTEM_PROMPT = """
You are a professional assistant. Use the provided Context to answer the User's question.
Rules:
1. Only use the information provided in the Context.
2. If the answer is not in the context, politely say you don't have enough information.
3. Always cite which [Source: filename] you got the information from.
4. Keep your answer concise and accurate.
"""

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def generate_answer(self, question: str, context: str, history: list = None) -> str:
        """Sends context, history, and question to Claude."""
        log.info("Requesting answer from Claude...")
       
        # Build the message list
        messages = []
       
        # Add history if it exists (Streamlit passes this as a list of dicts)
        if history:
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})
       
        # Add the current prompt with context
        prompt_with_context = f"Context:\n{context}\n\nQuestion: {question}"
        messages.append({"role": "user", "content": prompt_with_context})
       
        try:
            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1024,
                system=RAG_SYSTEM_PROMPT,
                messages=messages
            )
            return message.content[0].text
        except Exception as e:
            log.error(f"Claude API Error: {e}")
            return "I'm sorry, I encountered an error talking to my AI brain."