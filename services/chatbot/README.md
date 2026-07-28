# Chatbot Microservice

AI-powered chatbot service with RAG, intent classification, and document Q&A.

## Features
- Document Q&A (RAG)
- Intent Classification
- Smart Chat with BI
- ChromaDB integration
- Ollama LLM integration

## Project Structure

```
app/
├── __init__.py          # Flask app factory
├── api/                 # API endpoints
│   ├── health.py       # Health checks
│   ├── chat.py         # Chat endpoints
│   └── documents.py    # Document Q&A
└── ai/                  # AI engines
    ├── rag_engine.py    # RAG pipeline
    └── intent_classifier.py  # Intent detection
```

## Endpoints

- `GET /api/health` - Health check
- `POST /api/chat` - Main chat
- `POST /api/docs/chat` - Document Q&A
- `POST /api/smart-chat/chat` - Smart chat

## Building
```bash
docker build -f Dockerfile -t chatbot-service .
```

## Running
```bash
python main.py
```

## Configuration
See `config.py` for environment variables.
