"""
PDF preprocessing and embedding creation functions
"""

from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
# from marker.converters.pdf import PdfConverter
# from marker.models import create_model_dict
# from marker.output import text_from_rendered
from .config import MARKDOWN_OUTPUT, MARKDOWN_HEADERS, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDINGS_DIR
from .llm import get_embedding_function

def preprocess_pdf(pdf_path: str) -> List[Document]:
    """Extract text from PDF and create document chunks"""
    # Extract text using Marker
    # converter = PdfConverter(artifact_dict=create_model_dict())
    # rendered = converter(pdf_path)
    # text, _, images = text_from_rendered(rendered)
    # print(f"_ hai ---- {_}")

    #Extract text using pypdfloader
    loader = PyPDFLoader(pdf_path)
    text = loader.load()
    text = text[0].page_content
    print(text)
    print(type(text))
    # Save markdown
    with open(MARKDOWN_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(text)
    
    # Split by headers
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=MARKDOWN_HEADERS,
        strip_headers=False
    )
    md_header_splits = markdown_splitter.split_text(text)
    
    # Further chunk splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    splits = text_splitter.split_documents(md_header_splits)
    
    return splits

def create_embeddings(documents: List[Document]):
    """Create and save FAISS embeddings"""
    embedding_function = get_embedding_function()
    db = FAISS.from_documents(documents, embedding_function)
    db.save_local(folder_path=str(EMBEDDINGS_DIR))
    print(f"Saved {len(documents)} document chunks to embeddings")
