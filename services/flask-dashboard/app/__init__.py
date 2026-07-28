"""
Dashboard Flask Application Factory
"""

import os
import sys
from pathlib import Path
from flask import Flask, jsonify
from dotenv import load_dotenv

# Setup paths for module imports
# __file__ = /app/app/__init__.py
# .parent = /app/app
# .parent.parent = /app
APP_DIR = Path(__file__).resolve().parent.parent  # /app
DASHBOARD_DIR = APP_DIR / "files" / "dashboard"

# Add dashboard directory to Python path (for py_dashboard and db modules)
sys.path.insert(0, str(DASHBOARD_DIR))
sys.path.insert(0, str(APP_DIR))

print(f"[Dashboard] APP_DIR: {APP_DIR}")
print(f"[Dashboard] DASHBOARD_DIR: {DASHBOARD_DIR}")
print(f"[Dashboard] DASHBOARD_DIR exists: {DASHBOARD_DIR.exists()}")
print(f"[Dashboard] py_dashboard exists: {(DASHBOARD_DIR / 'py_dashboard').exists()}")
print(f"[Dashboard] Python path: {DASHBOARD_DIR} added to sys.path")

# Load environment
load_dotenv(APP_DIR / ".env")
load_dotenv(DASHBOARD_DIR / ".env")

CHATBOT_SERVICE_URL = os.getenv("CHATBOT_SERVICE_URL", "http://localhost:5000")


def create_app():
    """Create and configure Flask app."""
    
    app = None
    load_error = None
    
    # Try to load the actual py_dashboard app
    try:
        print("[Dashboard] Attempting to import py_dashboard...")
        from py_dashboard.web.app import create_app as create_dashboard
        print("[Dashboard] Successfully imported create_app from py_dashboard")
        
        app = create_dashboard()
        print("[Dashboard] ✓ Successfully loaded py_dashboard (Metrics Dashboard)")
        
    except ImportError as e:
        load_error = f"ImportError: {e}"
        print(f"[Dashboard] ✗ Import failed: {load_error}")
    except Exception as e:
        load_error = f"{type(e).__name__}: {e}"
        print(f"[Dashboard] ✗ Failed to create dashboard: {load_error}")
        import traceback
        traceback.print_exc()
    
    # Create fallback app if needed
    if app is None:
        print("[Dashboard] Creating fallback Flask app...")
        app = Flask(__name__)
        app.config["JSON_SORT_KEYS"] = False
        
        @app.get("/")
        def home():
            return {
                "error": "Could not load metrics dashboard",
                "reason": load_error,
                "hint": "py_dashboard module should be in /files/dashboard/py_dashboard",
                "debug_info": {
                    "dashboard_dir": str(DASHBOARD_DIR),
                    "exists": DASHBOARD_DIR.exists(),
                    "py_dashboard_exists": (DASHBOARD_DIR / "py_dashboard").exists(),
                }
            }, 500
    
    # Override health endpoint
    @app.get("/api/app/health")
    def health():
        return jsonify({
            "ok": True,
            "service": "flask-dashboard",
            "version": "4.0.0",
            "chatbot_service": CHATBOT_SERVICE_URL,
        }), 200

    # Add preflight check
    @app.get("/api/app/preflight")
    def preflight():
        db_ok = False
        try:
            from db.mysql_manager import get_sql_reader_connection
            conn = get_sql_reader_connection("THA6.0")
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
            cur.close()
            conn.close()
            db_ok = True
        except Exception as e:
            print(f"[Dashboard] Database check failed: {e}")

        return jsonify({
            "ok": db_ok,
            "database_ok": db_ok,
            "chatbot_service": CHATBOT_SERVICE_URL,
        }), 200

    return app
