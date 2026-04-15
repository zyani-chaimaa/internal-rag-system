import streamlit as st
import os
import sys
import uuid
import tempfile
from pathlib import Path

# --- 1. PROJECT PATH FIX ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- 2. INJECT API KEY FROM STREAMLIT SECRETS ---
# Streamlit Cloud secrets → os.environ so the backend config picks it up
if "ANTHROPIC_API_KEY" in st.secrets:
    os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

from backend.app.core.main import RAGSystem

st.set_page_config(page_title="Advanced RAG", page_icon="🚀")

# --- 3. INITIALIZE ENGINE & SESSION ---
if "rag" not in st.session_state:
    with st.spinner("Initializing RAG Engine..."):
        st.session_state.rag = RAGSystem()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# --- 4. UI LAYOUT ---
st.title("🚀 Internal RAG System")

with st.sidebar:
    st.write(f"Session: `{st.session_state.session_id[:8]}`")
    uploaded_file = st.file_uploader("Upload Knowledge Base (PDF)", type="pdf")

    if st.button("Index Document"):
        if uploaded_file:
            with st.spinner("Indexing..."):
                try:
                    # Save UploadedFile to a temp path so the backend gets a real Path object
                    suffix = Path(uploaded_file.name).suffix
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = Path(tmp.name)

                    st.session_state.rag.ingest_file(tmp_path, st.session_state.session_id)
                    tmp_path.unlink(missing_ok=True)  # clean up temp file
                    st.success("✅ Knowledge Base Updated!")
                except Exception as e:
                    st.error(f"❌ Indexing Error: {e}")
        else:
            st.warning("Please upload a file first.")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- 5. CHAT INTERFACE ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.rag.ask(prompt, st.session_state.session_id)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"AI Error: {e}")
