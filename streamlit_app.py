"""
Streamlit Frontend for Dynamic RAG Application
Clean, user-focused interface for research paper Q&A
"""

import streamlit as st
import requests
import json
from pathlib import Path

# =========================
# Configuration
# =========================
API_BASE_URL = "http://localhost:8000"
UPLOAD_ENDPOINT = f"{API_BASE_URL}/upload-pdf"
CHAT_ENDPOINT = f"{API_BASE_URL}/chat"
NEW_SESSION_ENDPOINT = f"{API_BASE_URL}/new-session"
CLEAR_ALL_ENDPOINT = f"{API_BASE_URL}/clear-all"

# =========================
# Helper Functions
# =========================
def upload_pdf(file):
    """Upload PDF to the backend"""
    try:
        files = {"file": (file.name, file.getvalue(), "application/pdf")}
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Upload failed: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Upload error: {str(e)}"

def send_chat_message(question, thread_id="streamlit_user_1"):
    """Send chat message to backend"""
    try:
        payload = {
            "question": question,
            "thread_id": thread_id
        }
        response = requests.post(CHAT_ENDPOINT, json=payload, timeout=60)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Chat failed: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Chat error: {str(e)}"

def start_new_session():
    """Start a new chat session"""
    try:
        response = requests.post(NEW_SESSION_ENDPOINT, timeout=30)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"New session failed: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"New session error: {str(e)}"

def clear_all_data():
    """Clear all data from backend"""
    try:
        response = requests.delete(CLEAR_ALL_ENDPOINT, timeout=30)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Clear all failed: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Clear all error: {str(e)}"

# =========================
# Streamlit App
# =========================
def main():
    st.set_page_config(
        page_title="Research Paper Q&A",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("📚 Research Paper Q&A")
    st.markdown("Upload a research paper and ask questions about it")
    st.markdown("---")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "pdf_uploaded" not in st.session_state:
        st.session_state.pdf_uploaded = False
    
    if "current_pdf" not in st.session_state:
        st.session_state.current_pdf = None
    
    if "current_sources" not in st.session_state:
        st.session_state.current_sources = []
    
    # Sidebar for source documents
    with st.sidebar:
        st.header("📄 Source Documents")
        
        if st.session_state.current_sources:
            st.markdown(f"**{len(st.session_state.current_sources)} relevant chunks found**")
            st.markdown("---")
            
            for i, doc in enumerate(st.session_state.current_sources):
                with st.expander(f"📝 Source {doc.get('chunk_id', i+1)}", expanded=False):
                    # Display metadata if available
                    metadata = doc.get('metadata', {})
                    if metadata:
                        if 'Header 1' in metadata:
                            st.markdown(f"**Section:** {metadata['Header 1']}")
                        if 'Header 2' in metadata:
                            st.markdown(f"**Subsection:** {metadata['Header 2']}")
                        if metadata.get('source'):
                            st.markdown(f"**Source:** {metadata['source']}")
                        st.markdown("---")
                    
                    # Display content
                    content = doc.get('content', '')
                    if len(content) > 300:
                        st.markdown(f"**Preview:** {content[:300]}...")
                        with st.expander("Show full content"):
                            st.markdown(content)
                    else:
                        st.markdown(content)
        else:
            st.info("Ask a question to see relevant document chunks here!")
    
    # PDF Upload Section
    if not st.session_state.pdf_uploaded:
        st.subheader("📄 Upload Research Paper")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a research paper to start asking questions"
        )
        
        if uploaded_file is not None:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📤 Upload & Process", use_container_width=True, type="primary"):
                    with st.spinner("Processing your research paper..."):
                        success, result = upload_pdf(uploaded_file)
                        
                        if success:
                            st.session_state.pdf_uploaded = True
                            st.session_state.current_pdf = uploaded_file.name
                            st.success(f"✅ Successfully processed: {uploaded_file.name}")
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
    
    else:
        # Chat Interface
        st.subheader("💬 Ask Questions")
        
        # Current document indicator
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"📄 Current document: **{st.session_state.current_pdf}**")
            with col2:
                if st.button("🔄 New Document", help="Upload a different document"):
                    st.session_state.pdf_uploaded = False
                    st.session_state.current_pdf = None
                    st.session_state.messages = []
                    st.rerun()
        
        st.markdown("---")
        
        # Chat messages display
        chat_container = st.container()
        with chat_container:
            if st.session_state.messages:
                for message in st.session_state.messages:
                    if message["role"] == "user":
                        with st.chat_message("user"):
                            st.markdown(message["content"])
                    else:
                        with st.chat_message("assistant"):
                            st.markdown(message["content"])
            else:
                st.markdown("👋 **Ready to answer your questions!**")
                st.markdown("Try asking about:")
                st.markdown("- Main findings or conclusions")
                st.markdown("- Methodology used")
                st.markdown("- Key concepts or definitions")
                st.markdown("- Specific sections or data")
        
        # Chat input
        question = st.chat_input("Ask a question about the research paper...")
        
        if question:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": question})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(question)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    success, result = send_chat_message(question)
                    
                    if success:
                        answer = result["answer"]
                        source_docs = result.get("source_documents", [])
                        st.markdown(answer)
                        
                        # Store source documents for sidebar display
                        st.session_state.current_sources = source_docs
                        
                        # Add assistant message to chat history
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        error_msg = f"Sorry, I encountered an error: {result}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        st.session_state.current_sources = []
            
            st.rerun()
        
        # Session controls (only show if there are messages)
        if st.session_state.messages:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("🆕 New Chat", help="Start a fresh conversation", use_container_width=True):
                    success, result = start_new_session()
                    if success:
                        st.session_state.messages = []
                        st.session_state.current_sources = []
                        st.success("Started new conversation!")
                        st.rerun()
                    else:
                        st.error("Failed to start new session")
            
            with col3:
                if st.button("🗑️ Clear All", help="Remove all data and start over", use_container_width=True):
                    success, result = clear_all_data()
                    if success:
                        st.session_state.messages = []
                        st.session_state.pdf_uploaded = False
                        st.session_state.current_pdf = None
                        st.session_state.current_sources = []
                        st.success("All data cleared!")
                        st.rerun()
                    else:
                        st.error("Failed to clear data")

if __name__ == "__main__":
    main()
