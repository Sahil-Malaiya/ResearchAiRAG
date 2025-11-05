# Research Assist AI

A sophisticated Research Paper Question & Answering system that allows users to upload PDF research papers and ask intelligent questions about their content using advanced AI techniques including Retrieval-Augmented Generation (RAG), LangGraph workflows, and vector embeddings.

## 📸 Screenshots

### React Frontend Interface

#### PDF Upload Interface
![PDF Upload Interface](screenshots/2025-10-30-225846_1920x1080_scrot.png)
*Clean, intuitive drag-and-drop interface for uploading research papers*

#### Processing State
![Processing State](screenshots/2025-10-30-225854_1920x1080_scrot.png)
*Real-time feedback during PDF processing and embedding creation*

#### Main Chat Interface
![Main Chat Interface](screenshots/2025-10-30-225836_1920x1080_scrot.png)
*Ready-to-use interface with suggested question categories*

#### Q&A in Action with Source Citations
![Q&A Interface](screenshots/2025-10-30-225817_1920x1080_scrot.png)
*Interactive chat with comprehensive answers and source document sidebar showing relevant chunks*

## 🏛️ LangGraph Architecture

![Agent Architecture](screenshots/agent_architecture.jpeg)

The system implements a sophisticated 5-node LangGraph workflow:

1. **question_rewriter** - Rephrases questions based on conversation history
2. **question_classifier** - Determines if questions are relevant to the document
3. **retrieve** - Finds relevant document chunks using vector search (on-topic path)
4. **generate_answer** - Creates comprehensive answers with retrieved context
5. **off_topic_response** - Handles questions unrelated to the uploaded document

The workflow uses conditional routing to ensure only relevant questions proceed to retrieval and answer generation.

## 🚀 Features

- **PDF Upload & Processing**: Upload research papers and automatically extract and process content
- **Intelligent Q&A**: Ask questions about uploaded papers and get contextual, accurate answers
- **Source Citations**: View relevant document chunks that informed each answer
- **Conversation History**: Maintain context across multiple questions in a session
- **Multiple Interfaces**: Choose between React frontend or Streamlit interface
- **Session Management**: Start new conversations or clear all data as needed
- **Smart Question Processing**: Automatic question rephrasing based on conversation context
- **Off-topic Detection**: Filters questions unrelated to the uploaded document

## 🏗️ Architecture

### Backend (FastAPI + LangGraph)
- **FastAPI server** with RESTful API endpoints
- **LangGraph workflow** implementing a 5-node AI pipeline:
  1. Question Rewriter - Rephrases questions based on chat history
  2. Question Classifier - Determines question relevance
  3. Off-topic Response - Handles irrelevant questions
  4. Retrieve - Finds relevant document chunks using vector search
  5. Generate Answer - Creates comprehensive answers with context
- **FAISS vector store** for efficient semantic search
- **SQLite checkpointing** for conversation persistence

### Frontend Options
- **React Application**: Modern UI with drag-and-drop, real-time chat, and source document sidebar
- **Streamlit Interface**: Simpler alternative interface for quick deployment

## 🛠️ Technology Stack

- **Backend**: FastAPI, LangChain, LangGraph, FAISS, SQLite
- **Frontend**: React, Vite, Tailwind CSS, Streamlit
- **AI/ML**: Vector embeddings, RAG architecture, LLM integration
- **Document Processing**: PyPDFLoader, text splitters, markdown processing
- **Deployment**: Uvicorn, CORS middleware

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+ (for React frontend)
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Research-Assist-AI
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (OpenAI, Anthropic, etc.)

# Start the backend server
cd backend
python main.py
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup (React)
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start the development server
npm run dev
```

The React frontend will be available at `http://localhost:5173`

### 4. Alternative: Streamlit Interface
```bash
# Run Streamlit app (from project root)
streamlit run streamlit_app.py
```

The Streamlit interface will be available at `http://localhost:8501`

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:

```env
# LLM API Keys (choose one or more)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key

# AWS Credentials (if using Bedrock)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1

# Optional: Custom model configurations
LLM_PROVIDER=openai  # openai, anthropic, google, bedrock
EMBEDDING_MODEL=text-embedding-ada-002
```

### LLM Provider Configuration
The system supports multiple LLM providers. Configure your preferred provider in the backend configuration files:

- **OpenAI**: GPT-3.5/GPT-4 models
- **Anthropic**: Claude models
- **Google**: Gemini models
- **AWS Bedrock**: Various foundation models

## 📁 Project Structure

```
Research-Assist-AI/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py              # Pydantic models and state definitions
│   ├── checkpoints.sqlite     # Conversation history database
│   ├── embeddings/            # FAISS vector store
│   ├── uploads/               # Uploaded PDF files
│   └── graph/
│       ├── graph.py           # LangGraph workflow compilation
│       ├── nodes.py           # Workflow node functions
│       ├── edges.py           # Workflow routing logic
│       ├── chains.py          # LangChain prompt chains
│       ├── config.py          # Configuration settings
│       ├── helpers.py         # Utility functions
│       ├── llm.py            # LLM and embedding configurations
│       └── preprocess.py      # PDF processing pipeline
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React application
│   │   ├── main.jsx          # React entry point
│   │   └── index.css         # Tailwind CSS styles
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js        # Vite configuration
├── streamlit_app.py          # Alternative Streamlit interface
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🔌 API Endpoints

### Backend API (FastAPI)
- `POST /upload-pdf` - Upload and process a PDF file
- `POST /chat` - Send a question and get an AI response
- `POST /new-session` - Start a new conversation thread
- `DELETE /clear-all` - Clear all data and conversations
- `GET /health` - Health check endpoint

### Example API Usage
```bash
# Upload a PDF
curl -X POST "http://localhost:8000/upload-pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@research_paper.pdf"

# Ask a question
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main findings?", "thread_id": "user_1"}'
```

## 🎯 Usage Examples

1. **Upload a Research Paper**: Drag and drop or select a PDF file
2. **Ask Questions**: 
   - "What are the main findings of this paper?"
   - "Explain the methodology used in this study"
   - "What are the limitations mentioned?"
   - "How does this compare to previous work?"
3. **View Sources**: Check the sidebar to see which document sections informed each answer
4. **Manage Sessions**: Start new conversations or clear all data as needed

## 🔍 Advanced Features

### Question Processing Pipeline
The system uses a sophisticated workflow to process questions:
1. **Context Integration**: Rephrases questions based on conversation history
2. **Relevance Filtering**: Ensures questions relate to the uploaded document
3. **Semantic Retrieval**: Finds the most relevant document sections
4. **Contextual Generation**: Creates comprehensive answers with proper citations

### Document Processing
- **Intelligent Chunking**: Preserves document structure and headers
- **Metadata Preservation**: Maintains section information for better citations
- **Vector Embeddings**: Creates semantic representations for accurate retrieval



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📞 Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the API documentation

---

**Happy researching! 📚🤖**
