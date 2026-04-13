from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routers import session, chat, upload

app = FastAPI(
    title="Advanced RAG API",
    description="Multi-user isolated RAG backend",
    version="2.0.0"
)

# IMPORTANT: This allows your Streamlit "Face" to talk to your FastAPI "Brain"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you'd limit this to your website URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our routes
app.include_router(session.router)
app.include_router(chat.router)
app.include_router(upload.router)

@app.get("/")
async def root():
    return {"message": "Advanced RAG API is Online"}