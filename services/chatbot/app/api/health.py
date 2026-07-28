"""
Health Check API Endpoints
"""

from flask import Blueprint, jsonify
import os

health_bp = Blueprint("health", __name__)

@health_bp.get("/api/health")
def health():
    """Service health check."""
    return jsonify({
        "ok": True,
        "service": "chatbot-service",
        "version": os.getenv("APP_VERSION", "4.0.0"),
        "port": 5000,
    }), 200

@health_bp.get("/")
def home():
    """Service info."""
    return jsonify({
        "service": "Smart Chatbot Service",
        "version": os.getenv("APP_VERSION", "4.0.0"),
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat",
            "documents": "/api/docs/chat",
            "smart_chat": "/api/smart-chat/chat",
        }
    }), 200
