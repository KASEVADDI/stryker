"""
Chat API Endpoints
Main chat and smart chat routes
"""

from flask import Blueprint, request, jsonify, current_app
import json
import time
import sys
from datetime import datetime

chat_bp = Blueprint("chat", __name__)

@chat_bp.post("/api/chat")
def chat():
    """Main chat endpoint with detailed logging."""
    start_time = time.time()
    request_id = request.headers.get('X-Request-ID', f"req-{int(start_time*1000)}")
    
    try:
        # Log incoming request
        data = request.get_json()
        message = data.get("message", "")
        app_name = data.get("app", "all")
        
        print(f"\n{'='*80}", flush=True)
        print(f"[{request_id}] ========== NEW QUESTION ==========", flush=True)
        print(f"[{request_id}] Question: {message}", flush=True)
        print(f"[{request_id}] Application: {app_name}", flush=True)
        print(f"[{request_id}] Timestamp: {datetime.now().isoformat()}", flush=True)
        print(f"{'='*80}\n", flush=True)
        
        # Step 1: Intent Classification
        print(f"[{request_id}] [1/4] Classifying intent...", flush=True)
        intent_start = time.time()
        if hasattr(current_app, 'intent_classifier'):
            intent = current_app.intent_classifier.classify(message)
            print(f"[{request_id}]       ✓ Intent detected: {intent} ({time.time()-intent_start:.2f}s)", flush=True)
        else:
            intent = "general"
            print(f"[{request_id}]       ⚠️  Intent classifier not available, using 'general'", flush=True)
        
        # Step 2: RAG Retrieval
        print(f"[{request_id}] [2/4] Retrieving documents from RAG...", flush=True)
        rag_start = time.time()
        documents = []
        if hasattr(current_app, 'rag_engine'):
            try:
                search_result = current_app.rag_engine.search(message, app=app_name)
                documents = search_result if search_result else []
                print(f"[{request_id}]       ✓ Retrieved {len(documents)} documents ({time.time()-rag_start:.2f}s)", flush=True)
                for i, doc in enumerate(documents[:3], 1):
                    doc_str = str(doc)[:100] if doc else "empty"
                    print(f"[{request_id}]       - Doc {i}: {doc_str}...", flush=True)
            except Exception as e:
                print(f"[{request_id}]       ✗ RAG search failed: {str(e)}", flush=True)
                documents = []
        else:
            print(f"[{request_id}]       ⚠️  RAG engine not available", flush=True)
            documents = []
        
        # Step 3: Generate Response
        print(f"[{request_id}] [3/4] Generating response...", flush=True)
        gen_start = time.time()
        response_text = f"Intent: {intent}. Query about {app_name} metrics. Found {len(documents)} relevant documents."
        print(f"[{request_id}]       ✓ Response generated ({time.time()-gen_start:.2f}s)", flush=True)
        
        # Step 4: Format Response
        print(f"[{request_id}] [4/4] Formatting response...", flush=True)
        response = {
            "ok": True,
            "message": response_text,
            "intent": intent,
            "app": app_name,
            "documents_found": len(documents),
            "processing_time_ms": round((time.time() - start_time) * 1000, 2)
        }
        
        total_time = time.time() - start_time
        print(f"[{request_id}] ✓ Response ready ({total_time:.2f}s total)", flush=True)
        print(f"[{request_id}] ========== QUESTION COMPLETE ==========\n", flush=True)
        sys.stdout.flush()
        
        return jsonify(response), 200
    except Exception as e:
        total_time = time.time() - start_time
        print(f"[{request_id}] ✗ ERROR: {str(e)} ({total_time:.2f}s)", flush=True)
        print(f"[{request_id}] ========== QUESTION FAILED ==========\n", flush=True)
        sys.stdout.flush()
        return jsonify({"ok": False, "error": str(e)}), 500

@chat_bp.post("/api/smart-chat/chat")
def smart_chat():
    """Smart chat with business intelligence."""
    try:
        data = request.get_json()
        message = data.get("message", "")
        
        # Use BI orchestrator
        response = {
            "ok": True,
            "message": f"Smart response for: {message}",
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
