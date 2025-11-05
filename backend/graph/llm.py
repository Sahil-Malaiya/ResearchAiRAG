from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
import os

def get_chat_model():
    os.environ["OLLAMA_USE_GPU"] = "0"   # CPU mode
    llm = ChatOllama(
        model="llama3.2:1b",   # lightweight model
        temperature=0.3,
        num_ctx=4096
    )
    return llm

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    return embeddings
