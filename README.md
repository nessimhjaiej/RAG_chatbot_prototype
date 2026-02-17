# ICC RAG Chatbot - React + Vite Version

A modern knowledge assistant for ICC policy documents using Retrieval-Augmented Generation (RAG). Built with React + Vite frontend and FastAPI backend.

## Architecture

- **Frontend**: React + Vite with Tailwind CSS (modern light theme)
- **Backend**: FastAPI (Python) wrapping existing RAG functionality
- **Database**: MongoDB (user authentication)
- **Vector Store**: ChromaDB with Ollama embeddings
- **LLM**: Ollama (qwen2.5:7b) for answer generation
- **Embeddings**: Ollama (qwen2.5:7b) for vector embeddings

## Features

- 🔐 User authentication with role-based access (admin/user)
- 💬 Natural language Q&A about ICC policies
- 🌍 **Bilingual support** - ask in French or English, AI responds in your language (translates French docs to English when needed)
- 📚 Retrieved source passages with metadata and similarity scores
- 🔍 Adjustable retrieval parameters (top-k passages: 1-10)
- 📊 System health monitoring dashboard
- 🎨 Modern, accessible light theme UI
- 📱 Responsive design for mobile and desktop
- ⚡ Optimized response generation with configurable timeouts
- 🧠 Detailed AI explanations with proper context and citations

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- MongoDB instance (local or cloud)
- Ollama installed locally with qwen2.5:7b model

## Ollama Setup

Install Ollama and download the model:

```bash
# Install Ollama from https://ollama.ai

# Pull the model
ollama pull qwen2.5:7b

# Verify installation
ollama list
```

## Environment Variables

Create a `.env` file in the project root:

```env
# MongoDB
MONGODB_URI=your_mongodb_connection_string
MONGODB_DB=rag_prototype
MONGODB_USERS_COLLECTION=users

# Ollama Configuration
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_EMBEDDING_MODEL=qwen2.5:7b

# Frontend URL (for production CORS)
FRONTEND_URL=http://localhost:5173
```

## Installation

### 1. Install Ollama and Model

```bash
# Download and install Ollama from https://ollama.ai
# Then pull the required model:
ollama pull qwen2.5:7b

# Verify installation
ollama list
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or if using the existing virtual environment:

```bash
# Activate existing venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r backend/requirements.txt
```

### 4. Setup MongoDB

Ensure MongoDB is running and accessible. Create users:

```bash
python scripts/setup_mongo.py
```

### 5. Ingest Documents (Optional)

If you need to populate the vector store:

```bash
python scripts/ingest.py
```

## Development

### Start Backend Server

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`

**Note**: Ensure Ollama is running and the model is available before starting the backend.

### Start Frontend Dev Server

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:5173`

### Quick Start with Batch Files (Windows)

```bash
# Start backend
start-backend.bat

# Start frontend  
start-frontend.bat
```

## Usage

1. **Login**: Use your MongoDB credentials to sign in
2. **Ask Questions**: Enter questions in French or English about ICC policies
3. **AI Responses**: Receive detailed explanations in the same language as your question with source citations
4. **Adjust Parameters**: Use the slider to control number of retrieved passages (1-10)
5. **Review Sources**: Expand source passages to see metadata and similarity scores
6. **Admin Mode** (admin users only): Toggle between AI Chat and AI Agent modes

## Performance & Configuration

### AI Response Settings

The system is configured for optimal performance:
- **Timeout**: 90 seconds for AI generation (frontend)
- **Max Tokens**: 1024 tokens per response
- **Temperature**: 0.7 (balanced creativity)
- **Context Window**: 4096 tokens
- **Keep-Alive**: 120 seconds (server connection)

### Response Quality

The AI is configured to provide:
- Detailed explanations with relevant context
- Clear breakdowns of complex topics
- Source citations using bracketed numbers [1], [2], etc.
- **Automatic language matching**: Detects if your question is in French or English and responds in the same language
- **Cross-language translation**: Source documents are in French, but the AI translates to English when you ask in English
- Maintains proper grammar and clarity in both languages

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
  - Body: `{ "username": "string", "password": "string" }`
  - Returns: User object with role and session info
- `POST /api/auth/logout` - User logout
- `GET /api/auth/verify` - Verify session
  - Returns: User object if authenticated

### RAG Query
- `POST /api/query` - Submit question and get answer with sources
  - Body: `{ "question": "string", "top_k": 5 }`
  - Returns: `{ "answer": "string", "contexts": [...] }`
  - Each context includes: `text`, `metadata`, `distance`
  - Timeout: Up to 90 seconds for AI generation

### Health
- `GET /api/health` - System health status
  - Returns: Database, vector store, and LLM status

### API Documentation
- `GET /docs` - Interactive Swagger UI documentation
- `GET /redoc` - ReDoc API documentation

## Project Structure

```
├── frontend/                  # React + Vite application
│   ├── src/
│   │   ├── api/              # API client functions
│   │   ├── components/       # Reusable React components
│   │   ├── context/          # Authentication context
│   │   ├── pages/            # Page components
│   │   ├── App.jsx           # Main app with routing
│   │   └── index.css         # Tailwind CSS + custom styles
│   ├── tailwind.config.js    # Tailwind configuration
│   └── vite.config.js        # Vite configuration
├── backend/                   # FastAPI server
│   ├── routers/              # API route handlers
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── query.py         # RAG query endpoints
│   │   └── health.py        # Health check endpoints
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── app/                      # Existing RAG modules (reused)
│   ├── auth.py              # Authentication logic
│   ├── rag_chain.py         # RAG pipeline
│   ├── vectorstore.py       # ChromaDB interface
│   └── embeddings.py        # Gemini embeddings
└── chromadb/                # Vector store persistence
```

## Building for Production

### Frontend

```bash
cd frontend
npm run build
```

The production build will be in `frontend/dist/`

### Backend

The FastAPI backend can be deployed using:
- **Uvicorn**: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
- **Docker**: Create a Dockerfile based on Python 3.10
- **Cloud**: Deploy to Railway, Heroku, or Google Cloud Run

### Deployment Recommendations

- **Frontend**: Netlify, Vercel, or GitHub Pages
- **Backend**: Railway, Heroku, or Google Cloud Run
- **Database**: MongoDB Atlas (cloud)
- **Ollama**: Deploy on a server with sufficient resources or use Ollama cloud services
- **Environment**: Use environment variables for all secrets

## Recent Improvements

### v1.2 - Multilingual Support
- ✅ **Automatic language detection** - AI detects question language and responds accordingly
- ✅ **Cross-language translation** - Translates French documents to English when questions are in English
- ✅ Seamless bilingual experience (French ↔ English) without manual language selection
- ✅ Maintains quality and detail in both supported languages

### v1.1 - Performance & Quality Enhancements
- ✅ Increased frontend timeout to 90 seconds for AI generation
- ✅ Added Ollama generation options (temperature, token limits, context window)
- ✅ Improved AI prompts for detailed yet focused responses
- ✅ Better error handling with informative messages
- ✅ Extended server keep-alive timeouts (120 seconds)
- ✅ Optimized response generation with token limits (1024 max)

### v1.0 - Initial Release
- ✅ React + Vite frontend with Tailwind CSS
- ✅ FastAPI backend with RESTful API
- ✅ MongoDB authentication system
- ✅ ChromaDB vector store integration
- ✅ Ollama-powered RAG pipeline
- ✅ French language support

## Migrating from Streamlit

The original Streamlit app (`app/ui.py`) is preserved. To use the new React version:

1. Ensure all environment variables are set
2. Start the FastAPI backend
3. Start the React frontend
4. Login with existing MongoDB credentials

All functionality from the Streamlit app has been migrated:
- ✅ Authentication with MongoDB
- ✅ RAG query processing
- ✅ Source passage display
- ✅ System health monitoring
- ✅ Admin/user roles
- ✅ Adjustable retrieval parameters

## Troubleshooting

### Backend won't start
- Check that MongoDB is accessible
- Verify Ollama is running (`ollama list`)
- Ensure qwen2.5:7b model is installed (`ollama pull qwen2.5:7b`)
- Ensure ChromaDB directory exists

### Frontend can't reach backend
- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Ensure VITE_API_URL points to http://localhost:8000

### Authentication fails
- Verify MongoDB connection string
- Check that users exist in MongoDB
- Ensure password hashes are bcrypt format
- Run `scripts/setup_mongo.py` to create test users

### AI responses timeout
- Check Ollama is running and responsive (`ollama run qwen2.5:7b`)
- Reduce number of retrieved passages (top_k)
- Verify system has enough resources (RAM/CPU)
- Frontend timeout is set to 90 seconds - adjust in `frontend/src/api/client.js` if needed

### ChromaDB errors
- Delete and reinitialize: `Remove-Item -Path "backend\chromadb" -Recurse -Force`
- Run ingestion script: `python scripts/ingest.py`
- Verify Ollama embeddings are working

## Data Ingestion

To populate the vector store with ICC policy documents:

```bash
# Run the ingestion script
python scripts/ingest.py

# This will:
# - Load documents from your data directory
# - Split into chunks using the configured splitter
# - Generate embeddings using Ollama
# - Store vectors in ChromaDB
```

## License

Internal ICC project

## Development Team

For issues, questions, or feature requests, contact the development team.

## Tech Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend Framework | React 18 + Vite | Modern, fast UI development |
| UI Styling | Tailwind CSS | Utility-first styling |
| Backend Framework | FastAPI | High-performance Python API |
| Authentication | MongoDB + bcrypt | User management |
| Vector Database | ChromaDB | Document embeddings storage |
| Embeddings | Ollama (qwen2.5:7b) | Text vectorization |
| LLM | Ollama (qwen2.5:7b) | Answer generation |
| HTTP Client | Axios | Frontend API calls |
| Server | Uvicorn | ASGI web server |

## Performance Tips

1. **Hardware**: Ollama works best with:
   - 8GB+ RAM for qwen2.5:7b model
   - Modern CPU (or GPU for faster inference)
   - SSD for faster model loading

2. **Optimization**:
   - Adjust `top_k` parameter (fewer passages = faster)
   - Use GPU acceleration if available
   - Monitor Ollama resource usage
   - Keep MongoDB indexes optimized

3. **Scaling**:
   - Deploy Ollama on dedicated server
   - Use MongoDB replica sets for HA
   - Consider CDN for frontend assets
   - Implement response caching for common queries