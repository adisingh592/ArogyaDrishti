"""
SehatSetu Flask API
Wraps the existing analyze_report.py pipeline into REST endpoints for the React frontend.
"""

import os
import sys
import json
import tempfile
import traceback
from flask import Flask, request, jsonify, make_response

# ── path setup ────────────────────────────────────────────────────────────────
CURRENT_DIR   = os.path.dirname(os.path.abspath(__file__))
SEHATSETU_DIR = os.path.join(CURRENT_DIR, "SehatSetu")
REPORT_DIR    = os.path.join(SEHATSETU_DIR, "report_analysis")
RECOM_DIR     = os.path.join(SEHATSETU_DIR, "recommendation")

for p in (REPORT_DIR, RECOM_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

# ── try importing the ML pipeline ────────────────────────────────────────────
try:
    from analyze_report import analyze_report_file, analyze_report_text
    ML_AVAILABLE = True
    ML_IMPORT_ERROR = None
except Exception as e:
    ML_AVAILABLE = False
    ML_IMPORT_ERROR = str(e)
    print(f"[WARNING] ML pipeline not available: {e}")

# ── app ───────────────────────────────────────────────────────────────────────
app = Flask(__name__)
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".txt"}


def cors_response(data, status=200):
    """Create a JSON response with CORS headers on every response."""
    if isinstance(data, dict):
        resp = make_response(json.dumps(data), status)
    else:
        resp = make_response(data, status)
    resp.headers["Content-Type"] = "application/json"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    resp.headers["Access-Control-Max-Age"] = "86400"
    return resp


@app.after_request
def add_cors(response):
    """Add CORS headers to every response."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    response.headers["Access-Control-Max-Age"] = "86400"
    return response


@app.before_request
def handle_preflight():
    """Handle OPTIONS preflight immediately — before any route logic."""
    if request.method == "OPTIONS":
        return cors_response({}, 200)


# ── routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return cors_response({
        "name": "SehatSetu API",
        "version": "1.0",
        "status": "running",
        "ml_available": ML_AVAILABLE,
        "endpoints": {
            "health": "GET /api/health",
            "analyze": "POST /api/analyze"
        }
    })


@app.route("/api/health")
def health():
    return cors_response({
        "status": "ok",
        "ml_available": ML_AVAILABLE,
        "ml_error": ML_IMPORT_ERROR,
    })


@app.route("/api/analyze", methods=["GET", "POST", "OPTIONS"])
def analyze():
    if request.method in ("GET", "OPTIONS"):
        return cors_response({"message": "Send a POST request with a 'file' field."})

    # ── ML not loaded ─────────────────────────────────────────────────────────
    if not ML_AVAILABLE:
        return cors_response({
            "error": f"ML pipeline failed to load: {ML_IMPORT_ERROR}",
            "decision": "SERVICE UNAVAILABLE",
            "conditions": [], "findings": [], "guidance": [],
            "extracted_values": {}, "model_results": [], "notes": [],
        }, 503)

    try:
        # ── file upload ───────────────────────────────────────────────────────
        if "file" in request.files:
            uploaded = request.files["file"]
            if not uploaded.filename:
                return cors_response({"error": "No file selected"}, 400)

            suffix = os.path.splitext(uploaded.filename)[1].lower()
            if suffix not in ALLOWED_EXTENSIONS:
                return cors_response({"error": f"Unsupported file type '{suffix}'. Use PDF, PNG, JPG, or TXT."}, 400)

            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                uploaded.save(tmp.name)
                tmp_path = tmp.name

            try:
                result = analyze_report_file(tmp_path, use_ml=True)
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

        # ── raw text ──────────────────────────────────────────────────────────
        elif request.is_json and request.json.get("text"):
            result = analyze_report_text(request.json["text"], use_ml=True)

        else:
            return cors_response({"error": "Send a 'file' field (multipart) or JSON {'text': '...'}"}, 400)

        return cors_response(_make_serialisable(result))

    except Exception:
        err = traceback.format_exc()
        print(f"[ERROR] /api/analyze failed:\n{err}")
        return cors_response({
            "error": "Analysis failed on the server. Check Railway logs.",
            "detail": err.splitlines()[-1],
            "decision": "ERROR",
            "conditions": [], "findings": [], "guidance": [],
            "extracted_values": {}, "model_results": [], "notes": [],
        }, 500)


def _make_serialisable(obj):
    """Recursively convert numpy / non-JSON-serialisable types."""
    if isinstance(obj, dict):
        return {k: _make_serialisable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_make_serialisable(i) for i in obj]
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        return str(obj)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[SehatSetu API] Starting on port {port} | ML available: {ML_AVAILABLE}")
    app.run(host="0.0.0.0", port=port, debug=False)
