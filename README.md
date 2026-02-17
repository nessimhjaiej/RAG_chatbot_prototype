# ICC RAG Chatbot - React + Vite Version

A modern knowledge assistant for ICC policy documents using Retrieval-Augmented Generation (RAG). Built with React + Vite frontend and FastAPI backend.

## Architecture

- **Frontend**: React + Vite with Tailwind CSS (modern light theme)
- **Backend**: FastAPI (Python) wrapping existing RAG functionality
- **Database**: MongoDB (user authentication)
- **Vector Store**: ChromaDB with Gemini embeddings
- **LLM**: Google Gemini for answer generation

## Features

- 🔐 User authentication with role-based access (admin/user)
- 💬 Natural language Q&A about ICC policies
- 📚 Retrieved source passages with metadata
- 🔍 Adjustable retrieval parameters (top-k passages)
- 📊 System health monitoring dashboard
- 🎨 Modern, accessible light theme UI
- 📱 Responsive design for mobile and desktop

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- MongoDB instance (local or cloud)
- Gemini API key

## Environment Variables

Create a `.env` file in the project root:

```env
# MongoDB
MONGODB_URI=your_mongodb_connection_string
MONGODB_DB=rag_prototype
MONGODB_USERS_COLLECTION=users

# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Frontend URL (for production CORS)
FRONTEND_URL=http://localhost:5173
```

## Installation

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or if using the existing virtual environment:

```bash
# Activate existing venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install additional FastAPI dependencies
pip install fastapi uvicorn python-multipart
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

### Start Frontend Dev Server

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:5173`

## Usage

1. **Login**: Use your MongoDB credentials to sign in
2. **Ask Questions**: Enter questions about ICC policies in the chat interface
3. **Adjust Parameters**: Use the slider to control number of retrieved passages (1-10)
4. **Review Sources**: Expand source passages to see metadata and distance scores
5. **Admin Mode** (admin users only): Toggle between AI Chat and AI Agent modes

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/verify` - Verify session

### RAG Query
- `POST /api/query` - Submit question and get answer with sources

### Health
- `GET /api/health` - System health status

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
- **Environment**: Use environment variables for all secrets

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
- Verify GEMINI_API_KEY is set
- Ensure ChromaDB directory exists

### Frontend can't reach backend
- Verify backend is running on port 8000
- Check VITE_API_URL in `.env.development`
- Check CORS settings in `backend/main.py`

### Authentication fails
- Verify MongoDB connection string
- Check that users exist in MongoDB
- Ensure password hashes are bcrypt format

## License

Internal ICC project

## Support

For issues or questions, contact the development team.