# Advanced RAG System

A production-ready **Retrieval-Augmented Generation (RAG)** platform built with FastAPI, Streamlit, ChromaDB, and Claude (Anthropic). Upload your documents and ask questions — the system retrieves the most relevant context and generates grounded, source-cited answers.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Setup](#local-setup)
  - [Docker Compose](#docker-compose)
  - [Streamlit Cloud](#streamlit-cloud)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [How It Works](#how-it-works)

---

## Overview

This system allows users to upload private documents (PDF, Excel, CSV) and have a grounded conversation with them via a Claude-powered chat interface. Each user session operates in complete isolation — documents and conversation history are siloed per session, ensuring no data leakage between users.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit Frontend                        │
│          Upload Documents · Chat Interface · Session UI          │
└───────────────────────────────┬─────────────────────────────────┘
                                │ HTTP (REST)
┌───────────────────────────────▼─────────────────────────────────┐
│                        FastAPI Backend                           │
│   /session   ·   /upload   ·   /chat/query   ·   /chat/clear    │
└──────────┬──────────────────────────────────────────────────────┘
           │
    ┌──────┴──────────────────────────────────┐
    │                                         │
┌───▼────────────┐                  ┌─────────▼──────────┐
│   ChromaDB     │                  │   Claude (Sonnet)   │
│  Vector Store  │                  │   Anthropic API     │
│ (per-session   │                  │                     │
│  collections)  │                  └─────────────────────┘
└────────────────┘
         ▲
         │ Embed (all-MiniLM-L6-v2)
┌────────┴────────┐
│  Ingestion      │
│  PDF / Excel /  │
│  CSV Loaders    │
│  + Text Chunker │
└─────────────────┘
```

---

## Features

- **Multi-user session isolation** — each session gets its own private ChromaDB collection; documents and history never cross sessions
- **Multi-format document ingestion** — supports PDF, XLSX, XLS, and CSV files
- **Intelligent text chunking** — recursive character splitter with configurable chunk size and overlap
- **Semantic retrieval** — sentence-transformer embeddings (`all-MiniLM-L6-v2`) with top-K similarity search
- **Grounded answers with source citation** — Claude is instructed to cite source filenames in every response
- **Conversation memory** — per-session rolling chat history (configurable window)
- **REST API** — clean FastAPI backend, usable independently of the Streamlit UI
- **Cloud-ready** — runs on Streamlit Cloud with ephemeral `/tmp` storage; Docker Compose for self-hosted deployments

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Claude Sonnet (`claude-sonnet-4-6`) via Anthropic API |
| Orchestration | LangChain |
| Vector Store | ChromaDB |
| Embeddings | `all-MiniLM-L6-v2` (sentence-transformers) |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Document Parsing | pdfplumber, pypdf, openpyxl, pandas |
| Logging | Loguru |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
RAG_Project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routers/
│   │   │   │   ├── session.py      # Session lifecycle endpoints
│   │   │   │   ├── upload.py       # Document upload & indexing
│   │   │   │   └── chat.py         # RAG query & memory clear
│   │   │   ├── dependencies.py     # FastAPI dependency injection
│   │   │   └── schemas.py          # Pydantic request/response models
│   │   ├── core/
│   │   │   ├── config.py           # Centralised settings & env vars
│   │   │   ├── main.py             # RAGSystem orchestrator class
│   │   │   ├── memory.py           # Per-session chat history store
│   │   │   ├── session.py          # Session manager
│   │   │   ├── ingestion/
│   │   │   │   ├── pdf_loader.py   # PDF → raw document dicts
│   │   │   │   ├── excel_loader.py # Excel/CSV → raw document dicts
│   │   │   │   └── processor.py    # Recursive text chunker
│   │   │   ├── retrieval/
│   │   │   │   └── retriever.py    # Semantic search against ChromaDB
│   │   │   ├── llm/
│   │   │   │   └── claude_client.py # Anthropic API wrapper
│   │   │   ├── vectorstore/
│   │   │   │   └── chroma_store.py # ChromaDB add/query interface
│   │   │   └── utils/
│   │   │       └── logger.py       # Loguru logger setup
│   │   └── main.py                 # FastAPI app factory & CORS
├── frontend/
│   └── app.py                      # Streamlit UI (sidebar upload + chat)
├── backend.Dockerfile
├── frontend.Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)
- Docker & Docker Compose *(optional, for containerised deployment)*

---

### Local Setup

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd RAG_Project
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-6    # optional — this is the default
CHUNK_SIZE=800                    # optional
CHUNK_OVERLAP=100                 # optional
TOP_K_RESULTS=5                   # optional
MAX_HISTORY_TURNS=10              # optional
```

**5. Start the backend**

```bash
uvicorn backend.app.main:app --reload --port 8000
```

**6. Start the frontend** (in a separate terminal)

```bash
streamlit run frontend/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

### Docker Compose

```bash
# Copy and fill in your API key
cp .env.example .env

docker compose up --build
```

| Service | URL |
|---|---|
| Streamlit UI | http://localhost:8501 |
| FastAPI docs | http://localhost:8000/docs |

---

### Streamlit Cloud

1. Push the repository to GitHub.
2. Create a new app on [Streamlit Cloud](https://streamlit.io/cloud) pointing to `frontend/app.py`.
3. Under **Settings → Secrets**, add:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

The app uses `/tmp` for all file and vector store operations — no persistent storage is required.

---

## Configuration

All settings are controlled via environment variables with sensible defaults:

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | **Required.** Anthropic API key |
| `CLAUDE_MODEL` | `claude-sonnet-4-6` | Claude model ID |
| `CHUNK_SIZE` | `800` | Maximum characters per text chunk |
| `CHUNK_OVERLAP` | `100` | Overlap between consecutive chunks |
| `TOP_K_RESULTS` | `5` | Number of chunks retrieved per query |
| `MAX_HISTORY_TURNS` | `10` | Conversation turns kept in memory per session |

---

## API Reference

Interactive docs available at `http://localhost:8000/docs` when the backend is running.

### Session

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/session/start` | Create a new isolated session. Returns `session_id`. |

### Document Upload

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload/file` | Upload and index a document. Requires `session-id` header. Supports PDF. |

### Chat

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/chat/query` | Ask a question against your indexed documents. |
| `POST` | `/chat/clear` | Clear the conversation history for a session. |

**Example — start a session and ask a question:**

```bash
# 1. Create a session
SESSION=$(curl -s -X POST http://localhost:8000/session/start | jq -r '.session_id')

# 2. Upload a document
curl -X POST http://localhost:8000/upload/file \
  -H "session-id: $SESSION" \
  -F "file=@report.pdf"

# 3. Ask a question
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What are the key findings?\", \"session_id\": \"$SESSION\"}"
```

---

## How It Works

### Ingestion Pipeline

```
File Upload → Loader (PDF / Excel / CSV) → RecursiveCharacterTextSplitter
    → Embed (all-MiniLM-L6-v2) → ChromaDB (session-scoped collection)
```

1. **Load** — `pdf_loader` or `excel_loader` converts files into a list of `{text, source, page}` dicts.
2. **Split** — `RecursiveCharacterTextSplitter` breaks documents into overlapping chunks (800 chars, 100 overlap by default) to preserve sentence context.
3. **Embed & Store** — each chunk is embedded and stored in a ChromaDB collection namespaced by `session_id`.

### Query Pipeline

```
User Question → Embed → ChromaDB similarity search (top-K, session-scoped)
    → Context assembly → Claude (system prompt + context + history) → Answer
```

1. **Retrieve** — the question is embedded and the top-K most similar chunks are fetched from the user's private collection.
2. **Generate** — Claude receives the retrieved context, the conversation history, and the question. It is instructed to answer only from the provided context and cite sources.
3. **Memory** — the exchange is appended to the session's rolling history window for follow-up questions.
