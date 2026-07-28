"""
Chatbot Microservice
Main entry point for chatbot service with AI capabilities
"""

import sys
import os
import logging
from app import create_app

# Ensure unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'
sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', buffering=1)

if __name__ == "__main__":
    print("\n" + "="*80, flush=True)
    print("🚀 STARTING CHATBOT MICROSERVICE (v2 WITH REQUEST LOGGING)...", flush=True)
    print("="*80 + "\n", flush=True)
    sys.stdout.flush()
    
    app = create_app()
    
    # Suppress Flask's default Werkzeug access logger (to avoid duplicate logs)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # Only show errors, not every request
    
    print("\n" + "="*80, flush=True)
    print("✅ Flask app configured - Launching on 0.0.0.0:5000", flush=True)
    print("📝 All requests will be logged with detailed processing info", flush=True)
    print("="*80 + "\n", flush=True)
    sys.stdout.flush()
    
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True, use_reloader=False)
