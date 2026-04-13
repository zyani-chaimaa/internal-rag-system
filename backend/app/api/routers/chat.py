from fastapi import APIRouter, Depends
from backend.app.api.schemas import ChatRequest, ChatResponse
from backend.app.api.dependencies import get_valid_session
from backend.app.core.memory import memory
from backend.app.core.llm.claude_client import ClaudeClient
from backend.app.core.vectorstore.chroma_store import VectorStore
from backend.app.core.retrieval.retriever import get_relevant_context

router = APIRouter(prefix="/chat", tags=["Conversation"])

# Initialize our core components
llm = ClaudeClient()
db = VectorStore()

@router.post("/query", response_model=ChatResponse)
async def chat_with_docs(
    request: ChatRequest,
    session_id: str = Depends(get_valid_session)
):
    """The main RAG conversation endpoint."""
   
    # 1. Get previous conversation from memory
    history = memory.get_history(session_id)
   
    # 2. Search ONLY this user's private document collection
    context = get_relevant_context(request.question, db, session_id=session_id)
   
    # 3. Generate answer using Claude + Context + History
    answer = llm.generate_answer(request.question, context, history=history)
   
    # 4. Save this new exchange to the user's memory
    memory.add_message(session_id, "user", request.question)
    memory.add_message(session_id, "assistant", answer)
   
    return ChatResponse(
        answer=answer,
        sources=[], # We will refine source extraction in the next step
        session_id=session_id
    )

@router.post("/clear")
async def clear_chat(session_id: str = Depends(get_valid_session)):
    """Wipes the chat memory for this specific user."""
    memory.clear_history(session_id)
    return {"status": "Memory cleared"}