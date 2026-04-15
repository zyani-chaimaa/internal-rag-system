import anthropic
from backend.app.core.config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_HISTORY_TURNS
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
        """Sends the context, conversation history, and question to Claude."""
        log.info("Requesting answer from Claude...")

        # Build message list: previous turns (windowed) + current question with context
        messages = []
        if history:
            # Each turn = 1 user message + 1 assistant message; keep last MAX_HISTORY_TURNS turns
            max_msgs = MAX_HISTORY_TURNS * 2
            messages = list(history[-max_msgs:])

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
