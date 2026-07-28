"""
Document API Endpoints
Document Q&A and RAG routes
"""

from flask import Blueprint, request, jsonify, current_app
import time
import sys
from datetime import datetime

documents_bp = Blueprint("documents", __name__)

@documents_bp.post("/api/docs/chat")
def document_chat():
    """Document Q&A endpoint with detailed logging."""
    start_time = time.time()
    request_id = request.headers.get('X-Request-ID', f"req-{int(start_time*1000)}")
    
    try:
        data = request.get_json()
        question = data.get("question", "")
        app_name = data.get("app", "all")
        
        print(f"\n{'='*80}", flush=True)
        print(f"[{request_id}] ========== NEW DOCUMENT QUESTION ==========", flush=True)
        print(f"[{request_id}] Question: {question}", flush=True)
        print(f"[{request_id}] Application: {app_name}", flush=True)
        print(f"[{request_id}] Timestamp: {datetime.now().isoformat()}", flush=True)
        print(f"{'='*80}\n", flush=True)
        
        # Step 1: Intent Classification
        print(f"[{request_id}] [1/4] Classifying intent...", flush=True)
        intent_start = time.time()
        if hasattr(current_app, 'intent_classifier'):
            intent = current_app.intent_classifier.classify(question)
            intent_time = time.time() - intent_start
            print(f"[{request_id}]       ✓ Intent detected: {intent} ({intent_time:.2f}s)", flush=True)
        else:
            intent = "document_query"
            print(f"[{request_id}]       ⚠️  Intent classifier not available", flush=True)
        
        # Step 2: RAG Search & Retrieval
        print(f"[{request_id}] [2/4] Searching documents in RAG engine...", flush=True)
        rag_start = time.time()
        response = None
        if hasattr(current_app, 'rag_engine'):
            try:
                print(f"[{request_id}]       - Querying RAG engine for: {question[:60]}...", flush=True)
                response = current_app.rag_engine.query(question)
                rag_time = time.time() - rag_start
                if response:
                    response_preview = str(response)[:150]
                    print(f"[{request_id}]       ✓ RAG query successful ({rag_time:.2f}s)", flush=True)
                    print(f"[{request_id}]       - Response preview: {response_preview}...", flush=True)
                else:
                    print(f"[{request_id}]       ⚠️  No response from RAG engine", flush=True)
            except Exception as e:
                rag_time = time.time() - rag_start
                print(f"[{request_id}]       ✗ RAG query failed ({rag_time:.2f}s): {str(e)}", flush=True)
                response = f"Error querying documents: {str(e)}"
        else:
            print(f"[{request_id}]       ⚠️  RAG engine not available", flush=True)
            response = f"Answer to: {question}"
        
        # Step 3: Format Response
        print(f"[{request_id}] [3/4] Formatting response...", flush=True)
        fmt_start = time.time()
        result = {
            "ok": True,
            "question": question,
            "answer": response if response else "No answer generated",
            "intent": intent,
            "processing_time_ms": round((time.time() - start_time) * 1000, 2)
        }
        fmt_time = time.time() - fmt_start
        print(f"[{request_id}]       ✓ Response formatted ({fmt_time:.2f}s)", flush=True)
        
        # Step 4: Return
        total_time = time.time() - start_time
        print(f"[{request_id}] ✓ Document query complete ({total_time:.2f}s total)", flush=True)
        print(f"[{request_id}] ========== DOCUMENT QUESTION COMPLETE ==========\n", flush=True)
        sys.stdout.flush()
        
        return jsonify(result), 200
    except Exception as e:
        total_time = time.time() - start_time
        print(f"[{request_id}] ✗ ERROR: {str(e)} ({total_time:.2f}s)", flush=True)
        print(f"[{request_id}] ========== DOCUMENT QUESTION FAILED ==========\n", flush=True)
        sys.stdout.flush()
        return jsonify({"ok": False, "error": str(e)}), 500
