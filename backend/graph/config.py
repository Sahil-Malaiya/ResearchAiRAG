"""
Configuration settings for the RAG application
"""

from pathlib import Path

# Directory paths
UPLOAD_DIR = Path("uploads")
EMBEDDINGS_DIR = Path("embeddings")
CHECKPOINT_DB = "checkpoints.sqlite"
MARKDOWN_OUTPUT = "marker_out.md"

# AWS Configuration
AWS_REGION = "ap-south-1"
BEDROCK_MODEL = "apac.anthropic.claude-sonnet-4-20250514-v1:0"

# Text splitting configuration
MARKDOWN_HEADERS = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]

CHUNK_SIZE = 512
CHUNK_OVERLAP = 80

# Retrieval configuration
RETRIEVAL_K = 4
RETRIEVAL_TYPE = "mmr"

def ensure_directories():
    """Create necessary directories if they don't exist"""
    UPLOAD_DIR.mkdir(exist_ok=True)
    EMBEDDINGS_DIR.mkdir(exist_ok=True)
