"""
Pydantic models and state definitions for the RAG application
"""

from typing import List, TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage

class AgentState(TypedDict):
    """State definition for the LangGraph workflow"""
    messages: List[BaseMessage]
    documents: List
    on_topic: str
    rephrased_question: str
    proceed_to_generate: bool
    rephrase_count: int
    question: HumanMessage

class ClassificationScore(BaseModel):
    """Binary score for relevance check"""
    score: str = Field(description="'yes' or 'no'")

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str
    thread_id: str = "persistent_user_1"

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str
    thread_id: str
    source_documents: List[dict] = []

class UploadResponse(BaseModel):
    """Response model for PDF upload endpoint"""
    message: str
    filename: str
    chunks_created: int

class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    pdf_uploaded: bool
    graph_initialized: bool

class NewSessionResponse(BaseModel):
    """Response model for new session endpoint"""
    message: str
    thread_id: str
    note: str

class ClearAllResponse(BaseModel):
    """Response model for clear all endpoint"""
    message: str
    old_checkpoint_db: str
    new_checkpoint_db: str
    note: str
