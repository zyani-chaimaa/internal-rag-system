import streamlit as st
import shutil
from pathlib import Path
from backend.app.core.main import RAGSystem
from backend.app.core.config import UPLOADS_DIR
from backend.app.core.utils.logger import log

# 1. Page Configuration
st.set_page_config(page_title="My Personal RAG", page_icon="🤖", layout="wide")
st.title("🤖 Claude-Powered RAG System")

# 2. Initialize the RAG System in the "Session State"
# This ensures we don't reload the whole system every time you click a button
if "rag" not in st.session_state:
    with st.spinner("Initializing RAG Engine..."):
        st.session_state.rag = RAGSystem()
        st.session_state.messages = []

# 3. Sidebar for File Uploads
with st.sidebar:
    st.header("Document Center")
    uploaded_files = st.file_uploader(
        "Upload PDF or Excel files",
        type=["pdf", "xlsx", "csv"],
        accept_multiple_files=True
    )
   
    if st.button("Process Documents"):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Save the file locally to the data/uploads folder
                file_path = UPLOADS_DIR / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
               
                # Run the ingestion pipeline
                with st.spinner(f"Ingesting {uploaded_file.name}..."):
                    st.session_state.rag.ingest_file(file_path)
            st.success("Documents indexed!")
        else:
            st.warning("Please select files first.")
   
    st.divider()
    st.info(f"Indexed Chunks: {st.session_state.rag.db.get_count()}")

# 4. Chat Interface
# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about your documents:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Searching documents & thinking..."):
            response = st.session_state.rag.ask(prompt)
            st.markdown(response)
   
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
