"""
Dashboard Configuration
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent.parent.parent

# Flask
FLASK_PORT = int(os.getenv("FLASK_PORT", "3000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# Database
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "chatbox")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "smartchatbox")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "THA6")

# Chatbot Service
CHATBOT_SERVICE_URL = os.getenv("CHATBOT_SERVICE_URL", "http://localhost:5000")

# Application
APP_VERSION = "4.0.0"
