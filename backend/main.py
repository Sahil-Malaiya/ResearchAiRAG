"""
FastAPI application for Research Paper RAG
"""

import uuid
import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from graph.config import ensure_directories, UPLOAD_DIR, EMBEDDINGS_DIR, CHECKPOINT_DB
from models import (
    ChatRequest, ChatResponse, UploadResponse, 
    HealthResponse, NewSessionResponse, ClearAllResponse
)
from graph.helpers import cleanup_old_files
from graph.preprocess import preprocess_pdf, create_embeddings
from graph.graph import create_graph

# Initialize directories
ensure_directories()

# FastAPI app
app = FastAPI(title="Research Paper RAG API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global graph instance
graph = None

@app.post("/upload-pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a new research paper PDF.
    This will:
    1. Delete previous uploads and embeddings
    2. Process the new PDF
    3. Create and store embeddings
    """
    global graph
    
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Cleanup old files
        cleanup_old_files()
        
        # Save uploaded file
        pdf_path = UPLOAD_DIR / file.filename
        with open(pdf_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # Preprocess PDF
        print(f"Processing PDF: {file.filename}")
        documents = preprocess_pdf(str(pdf_path))
        
        # Create embeddings
        print("Creating embeddings...")
        create_embeddings(documents)
        print("Embeddings created")
        
        # Reinitialize graph with new checkpointer
        graph = create_graph()
        
        return UploadResponse(
            message="PDF uploaded and processed successfully",
            filename=file.filename,
            chunks_created=len(documents)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the uploaded research paper.
    Maintains conversation history using thread_id.
    """
    global graph
    
    if graph is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF first using /upload-pdf endpoint"
        )
    
    try:
        # Create config with thread_id
        config = {
            "configurable": {
                "thread_id": request.thread_id
            }
        }
        
        # Create initial state - let LangGraph load existing conversation from checkpoint
        initial_state = {
            "question": HumanMessage(content=request.question),
            # Don't initialize messages as empty - let the checkpointer load existing conversation
            "documents": [],
            "on_topic": "",
            "rephrased_question": "",
            "proceed_to_generate": False,
            "rephrase_count": 0
        }
        
        # Run graph
        result = graph.invoke(initial_state, config=config)
        
        # Extract answer and source documents
        if result["messages"]:
            answer = result["messages"][-1].content
        else:
            answer = "I couldn't generate an answer. Please try rephrasing your question."
        
        # Format source documents for response
        source_docs = []
        if "documents" in result and result["documents"]:
            for i, doc in enumerate(result["documents"]):
                source_docs.append({
                    "chunk_id": i + 1,
                    "content": doc.page_content,
                    "metadata": doc.metadata if hasattr(doc, 'metadata') else {}
                })
        
        return ChatResponse(
            answer=answer,
            thread_id=request.thread_id,
            source_documents=source_docs
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/new-session", response_model=NewSessionResponse)
async def new_session():
    """
    Start a new chat session by generating a new thread ID.
    This effectively creates a new conversation thread while keeping the uploaded PDF.
    """
    try:
        # Generate a new unique thread ID
        new_thread_id = f"session_{uuid.uuid4().hex[:8]}"
        
        return NewSessionResponse(
            message="New session started successfully",
            thread_id=new_thread_id,
            note="Use this thread_id in your chat requests to start fresh conversation"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        pdf_uploaded=(EMBEDDINGS_DIR / "index.faiss").exists(),
        graph_initialized=graph is not None
    )

@app.delete("/clear-all", response_model=ClearAllResponse)
async def clear_all():
    """
    Clear all data including PDFs, embeddings, and chat history.
    Creates a new checkpoint database to avoid file locking issues.
    """
    global graph, CHECKPOINT_DB
    
    try:
        cleanup_old_files()
        
        # Generate new database filename with timestamp to avoid file deletion
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        old_checkpoint_db = CHECKPOINT_DB
        new_checkpoint_db = f"checkpoints_{timestamp}.sqlite"
        
        # Update the global CHECKPOINT_DB
        import graph.config
        graph.config.CHECKPOINT_DB = new_checkpoint_db
        
        # Recreate graph with new database (this effectively clears all conversation history)
        graph = create_graph()
        
        return ClearAllResponse(
            message="All data cleared successfully",
            old_checkpoint_db=old_checkpoint_db,
            new_checkpoint_db=new_checkpoint_db,
            note="Old checkpoint database file can be manually deleted later if needed"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
