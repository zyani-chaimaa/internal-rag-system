# Advanced RAG System

A **Retrieval-Augmented Generation (RAG)** platform built with Streamlit, ChromaDB, and Claude (Anthropic). Upload your documents and ask questions — the system retrieves the most relevant context and generates grounded, source-cited answers.

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
  - [Streamlit Cloud](#streamlit-cloud)
- [Configuration](#configuration)
- [How It Works](#how-it-works)

---

## Overview

This system allows users to upload PDF documents and have a grounded conversation with them via a Claude-powered chat interface. Each user session operates in complete isolation — documents and conversation history are siloed per session using separate ChromaDB collections, ensuring no data leakage between users.

The app is **monolithic**: Streamlit directly imports and runs the Python backend in-process — no separate API server is needed. It is designed to run locally or on Streamlit Cloud.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit App (frontend/app.py)        │
│         Upload Documents · Chat Interface · Session UI   │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │              RAGSystem (backend/app/core/main.py)  │  │
│  │                                                    │  │
│  │   ingest_file()         ask()                      │  │
│  │        │                  │                        │  │
│  │   ┌────▼──────┐    ┌──────▼──────┐                │  │
│  │   │ Ingestion │    │  Retriever  │                 │  │
│  │   │  Pipeline │    │  (ChromaDB) │                 │  │
│  │   └────┬──────┘    └──────┬──────┘                │  │
│  │        │                  │                        │  │
│  │   ┌────▼──────────────────▼──────┐                │  │
│  │   │   VectorStore (ChromaDB)     │                 │  │
│  │   │   per-session collections    │                 │  │
│  │   └──────────────────────────────┘                │  │
│  │                                                    │  │
│  │   ┌──────────────────────┐                        │  │
│  │   │  ClaudeClient        │                        │  │
│  │   │  Anthropic API       │                        │  │
│  │   └──────────────────────┘                        │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Features

- **Monolithic design** — Streamlit directly calls the Python backend; no HTTP layer or separate server required
- **Multi-user session isolation** — each Streamlit session gets its own private ChromaDB collection; documents never cross sessions
- **Multi-format document ingestion** — supports PDF, XLSX, XLS, and CSV via the UI uploader
- **Intelligent text chunking** — `RecursiveCharacterTextSplitter` with configurable chunk size and overlap
- **Semantic retrieval** — ChromaDB's built-in ONNX embedding function (no PyTorch required) with top-K similarity search
- **Grounded answers with source citation** — Claude is instructed to cite source filenames in every response
- **Conversation memory** — prior turns are passed to Claude each time (windowed to `MAX_HISTORY_TURNS`)
- **Live index counter** — sidebar shows how many chunks are indexed for the current session
- **Cloud-ready** — runs on Streamlit Cloud with ephemeral `/tmp` storage; no persistent storage required

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Claude (`claude-sonnet-4-6`) via Anthropic API |
| Text Splitting | LangChain `RecursiveCharacterTextSplitter` |
| Vector Store | ChromaDB (persistent, per-session collections) |
| Embeddings | ChromaDB `DefaultEmbeddingFunction` (ONNX-based) |
| Frontend | Streamlit |
| Document Parsing | pdfplumber, pandas, openpyxl |
| Logging | Loguru |

---

## Project Structure

```
RAG_Project/
├── backend/
│   └── app/
│       └── core/
│           ├── main.py             # RAGSystem orchestrator (ingest_file + ask + get_doc_count)
│           ├── config.py           # Centralised settings & env vars
│           ├── ingestion/
│           │   ├── pdf_loader.py   # PDF → raw document dicts (with table extraction)
│           │   ├── excel_loader.py # Excel/CSV → raw document dicts
│           │   └── processor.py    # RecursiveCharacterTextSplitter wrapper
│           ├── retrieval/
│           │   └── retriever.py    # Top-K similarity search against ChromaDB
│           ├── vectorstore/
│           │   └── chroma_store.py # ChromaDB add/query/delete interface
│           ├── llm/
│           │   └── claude_client.py # Anthropic API wrapper + system prompt
│           └── utils/
│               └── logger.py       # Loguru logger setup
├── frontend/
│   └── app.py                      # Streamlit UI (sidebar upload + chat)
├── data/
│   └── vectorstore/                # ChromaDB persistence (local dev)
├── logs/
│   └── rag_system.log
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

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

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-6    # optional — this is the default
CHUNK_SIZE=800                    # optional
CHUNK_OVERLAP=100                 # optional
TOP_K_RESULTS=5                   # optional
MAX_HISTORY_TURNS=10              # optional
```

**5. Run the app**

```bash
streamlit run frontend/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

### Streamlit Cloud

1. Push the repository to GitHub.
2. Create a new app on [Streamlit Cloud](https://streamlit.io/cloud) pointing to `frontend/app.py`.
3. Under **Settings → Secrets**, add:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

All file and vector store operations use `/tmp` — no persistent storage is required.

---

## Configuration

All settings are controlled via environment variables (or Streamlit secrets) with sensible defaults:

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | **Required.** Anthropic API key |
| `CLAUDE_MODEL` | `claude-sonnet-4-6` | Claude model ID |
| `CHUNK_SIZE` | `800` | Maximum characters per text chunk |
| `CHUNK_OVERLAP` | `100` | Overlap between consecutive chunks |
| `TOP_K_RESULTS` | `5` | Number of chunks retrieved per query |
| `MAX_HISTORY_TURNS` | `10` | Conversation turns kept in memory per session |

---

## How It Works

### Ingestion Pipeline

```
File Upload → Loader (PDF / Excel / CSV) → RecursiveCharacterTextSplitter
    → Embed (ONNX DefaultEmbeddingFunction) → ChromaDB (session-scoped collection)
```

1. **Load** — `pdf_loader` extracts text and tables page-by-page using `pdfplumber`. `excel_loader` converts each row into a `"Column: Value | ..."` string using `pandas`.
2. **Split** — `RecursiveCharacterTextSplitter` breaks documents into overlapping chunks (800 chars, 100 overlap by default), trying to split at paragraph, sentence, and word boundaries.
3. **Embed & Store** — ChromaDB automatically embeds each chunk with its built-in ONNX model and stores it in a collection namespaced by `session_id`.

### Query Pipeline

```
User Question → ChromaDB similarity search (top-K, session-scoped)
    → Context assembly → Claude (system prompt + context) → Answer
```

1. **Retrieve** — the question is embedded and the top-K most similar chunks are fetched from the user's private collection (`TOP_K_RESULTS` from config).
2. **Generate** — Claude receives the retrieved context, the windowed conversation history (up to `MAX_HISTORY_TURNS` prior turns), and the current question. It is instructed to answer only from the provided context and cite the source filename.
