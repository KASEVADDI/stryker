"""
Chatbot Configuration
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent.parent.parent

# Flask
CHATBOT_PORT = int(os.getenv("CHATBOT_PORT", "5000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# Database
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "chatbox")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "smartchatbox")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "THA6")

# ChromaDB Vector Database
CHROMADB_HOST = os.getenv("CHROMADB_HOST", "chromadb")
CHROMADB_PORT = int(os.getenv("CHROMADB_PORT", "8000"))

# Ollama LLM
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Features
ENABLE_DOCUMENT_CHAT = os.getenv("ENABLE_DOCUMENT_CHAT", "1").lower() == "1"
ENABLE_SMART_CHAT = os.getenv("ENABLE_SMART_CHAT", "1").lower() == "1"

# Application
APP_VERSION = "4.0.0"
