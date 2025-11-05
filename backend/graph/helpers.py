"""
Helper utility functions for the RAG application
"""

import shutil
from pathlib import Path
from langchain_community.vectorstores import FAISS
from .config import UPLOAD_DIR, EMBEDDINGS_DIR, MARKDOWN_OUTPUT, RETRIEVAL_TYPE, RETRIEVAL_K
from .llm import get_embedding_function

def load_retriever(embeddings_path: str):
    """Load FAISS retriever from local storage"""
    embedding_function = get_embedding_function()
    db = FAISS.load_local(
        folder_path=embeddings_path,
        embeddings=embedding_function,
        allow_dangerous_deserialization=True
    )
    return db.as_retriever(search_type=RETRIEVAL_TYPE, search_kwargs={"k": RETRIEVAL_K})

def cleanup_old_files():
    """Delete previous PDFs and embeddings"""
    # Clear uploads
    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR)
        UPLOAD_DIR.mkdir()
    
    # Clear embeddings
    if EMBEDDINGS_DIR.exists():
        shutil.rmtree(EMBEDDINGS_DIR)
        EMBEDDINGS_DIR.mkdir()
    
    # Remove markdown output
    if Path(MARKDOWN_OUTPUT).exists():
        Path(MARKDOWN_OUTPUT).unlink()
    
    print("Cleaned up old files")
