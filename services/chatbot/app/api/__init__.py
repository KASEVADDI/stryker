"""
API Module Init
Export all blueprints
"""

from app.api.health import health_bp
from app.api.chat import chat_bp
from app.api.documents import documents_bp

__all__ = ["health_bp", "chat_bp", "documents_bp"]
