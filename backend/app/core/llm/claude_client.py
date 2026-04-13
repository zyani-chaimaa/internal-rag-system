import anthropic
from backend.app.core.config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from backend.app.core.utils.logger import log

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
        """Sends the context and question to Claude and returns the response."""
        log.info("Requesting answer from Claude...")
       
        # We combine the context from our database with the user's question
        prompt_with_context = f"Context:\n{context}\n\nQuestion: {question}"
       
        try:
            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1024,
                system=RAG_SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": prompt_with_context}
                ]
            )
            return message.content[0].text
        except Exception as e:
            log.error(f"Claude API Error: {e}")
            return "I'm sorry, I encountered an error talking to my AI brain."
