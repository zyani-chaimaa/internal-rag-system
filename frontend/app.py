import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL","http://localhost:8000")

st.set_page_config(page_title="Advanced RAG", page_icon="🚀")

# --- 1. INITIALIZE ALL STATE VARIABLES IMMEDIATELY ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# --- 2. CONNECTION CHECK & SESSION START ---
if st.session_state.session_id is None:
    try:
        # Try to start a session
        resp = requests.post(f"{API_URL}/session/start", timeout=2)
        if resp.status_code == 200:
            st.session_state.session_id = resp.json()["session_id"]
            st.rerun() # Refresh to show the UI
        else:
            st.error("Backend is awake but refused to start a session.")
            st.stop()
    except Exception:
        st.error("❌ Backend Offline. Please start Uvicorn in your other terminal.")
        st.info("Command: python3 -m uvicorn backend.app.main:app --reload --port 8000")
        st.stop()

# --- 3. THE UI (Only runs if session_id exists) ---
st.title("🚀 Advanced Multi-User RAG")

with st.sidebar:
    st.write(f"Connected as: `{st.session_state.session_id[:8]}`")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
   
    if st.button("Index Document"):
        if uploaded_file:
            with st.spinner("Processing PDF..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                # We send the session_id in the HEADERS as a security check
                headers = {"session-id": st.session_state.session_id}
               
                try:
                    r = requests.post(f"{API_URL}/upload/file", files=files, headers=headers)
                    if r.status_code == 200:
                        st.success("✅ Document indexed!")
                    else:
                        # This tells us EXACTLY what the backend didn't like
                        error_detail = r.json().get('detail', 'Unknown error')
                        st.error(f"❌ Upload Failed: {error_detail}")
                except Exception as e:
                    st.error(f"❌ Connection error: {e}")

# --- 4. CHAT INTERFACE ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        headers = {"session-id": st.session_state.session_id}
        payload = {"question": prompt, "session_id": st.session_state.session_id}
       
        try:
            r = requests.post(f"{API_URL}/chat/query", json=payload, headers=headers)
            if r.status_code == 200:
                ans = r.json()["answer"]
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                st.error("Backend error during chat.")
        except Exception as e:
            st.error(f"Connection lost: {e}")