"""
Chatbot Flask Application Factory
Orchestrates AI, RAG, and API endpoints
"""

import os
import time
import sys
from pathlib import Path
from flask import Flask, jsonify, request
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

def create_app():
    """Create and configure Flask app with chatbot features."""
    app = Flask(__name__)
    
    # Configuration
    app.config["JSON_SORT_KEYS"] = False
    app.config["CHATBOT_PORT"] = int(os.getenv("CHATBOT_PORT", "5000"))
    
    # Middleware: Log ALL incoming requests (except health checks)
    @app.before_request
    def log_request():
        """Log every incoming request with timestamp."""
        # Skip health checks to keep logs clean
        if request.path == '/api/health':
            return
        
        request.start_time = time.time()
        print(f"\n{'='*80}", flush=True)
        print(f"[REQUEST] {request.method} {request.path}", flush=True)
        print(f"[REQUEST] Remote: {request.remote_addr}", flush=True)
        print(f"[REQUEST] Content-Type: {request.content_type}", flush=True)
        if request.method in ['POST', 'PUT']:
            try:
                data = request.get_json(silent=True) or {}
                print(f"[REQUEST] Payload: {str(data)[:200]}", flush=True)
            except:
                pass
        sys.stdout.flush()
    
    @app.after_request
    def log_response(response):
        """Log response status."""
        # Skip health checks
        if request.path == '/api/health':
            return response
        
        elapsed = time.time() - request.start_time if hasattr(request, 'start_time') else 0
        print(f"[RESPONSE] Status: {response.status_code} | Time: {elapsed:.2f}s", flush=True)
        print(f"{'='*80}\n", flush=True)
        sys.stdout.flush()
        return response
    
    # Register API blueprints
    from app.api import health_bp, chat_bp, documents_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(documents_bp)
    
    # Initialize AI engines
    try:
        from app.ai import init_rag_engine, init_intent_classifier
        app.rag_engine = init_rag_engine()
        app.intent_classifier = init_intent_classifier()
        print("✓ AI engines initialized", flush=True)
    except Exception as e:
        print(f"⚠️  Warning: AI engines not fully initialized: {e}", flush=True)
    
    # Load metadata
    try:
        from chatbox.dashboard.discovery import ensure_metadata_loaded
        _meta = ensure_metadata_loaded()
        _meta = _meta or {}
        intents_count = len(_meta.get('intents', {}))
        print(f"✓ Metadata loaded ({intents_count} intents)", flush=True)
    except Exception as e:
        print(f"⚠️  Metadata cache skipped: {e}", flush=True)
    
    sys.stdout.flush()
    return app
