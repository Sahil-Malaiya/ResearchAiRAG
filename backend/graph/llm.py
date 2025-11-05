"""
LLM and embedding initialization functions
"""

import os
from langchain_aws import ChatBedrock, BedrockEmbeddings
from .config import AWS_REGION, BEDROCK_MODEL
from dotenv import load_dotenv

load_dotenv()

def get_chat_model():
    """Initialize ChatBedrock model"""
    llm = ChatBedrock(
        model=BEDROCK_MODEL,
        region_name=AWS_REGION,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    return llm

def get_embedding_function():
    """Initialize Bedrock embeddings"""
    try:
        return BedrockEmbeddings()
    except Exception as e:
        print(f"Couldn't make embeddings - {e}")
        raise e
