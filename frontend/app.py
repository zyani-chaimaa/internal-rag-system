import streamlit as st
import os
import sys
import uuid

# --- 1. PROJECT PATH FIX ---
# This ensures the frontend can see the 'backend' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.main import RAGSystem

st.set_page_config(page_title="Advanced RAG", page_icon="🚀")

# --- 2. INITIALIZE ENGINE & SESSION ---
if "rag" not in st.session_state:
    with st.spinner("Initializing RAG Engine..."):
        # This creates the RAG instance once and keeps it in memory
        st.session_state.rag = RAGSystem()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# --- 3. UI LAYOUT ---
st.title("🚀 Internal RAG System")

with st.sidebar:
    st.write(f"Session: `{st.session_state.session_id[:8]}`")
    uploaded_file = st.file_uploader("Upload Knowledge Base (PDF)", type="pdf")
   
    if st.button("Index Document"):
        if uploaded_file:
            with st.spinner("Indexing..."):
                try:
                    # DIRECT CALL: Using your actual method name
                    st.session_state.rag.ingest_file(uploaded_file)
                    st.success("✅ Knowledge Base Updated!")
                except Exception as e:
                    st.error(f"❌ Indexing Error: {e}")
        else:
            st.warning("Please upload a file first.")

# --- 4. CHAT INTERFACE ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        try:
            # DIRECT CALL: Querying the in-memory engine
            response = st.session_state.rag.query(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"AI Error: {e}")