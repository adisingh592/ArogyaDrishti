"""
SehatSetu Flask API
Wraps the existing analyze_report.py pipeline into REST endpoints for the React frontend.
"""

import os
import sys
import json
import tempfile
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

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
except Exception as e:
    ML_AVAILABLE = False
    ML_IMPORT_ERROR = str(e)
    print(f"[WARNING] ML pipeline not available: {e}")

# ── app ───────────────────────────────────────────────────────────────────────
app = Flask(__name__)

# Broad CORS — allow all origins, methods, and headers
CORS(app,
     origins="*",
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"],
     supports_credentials=False)

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".txt"}


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "ml_available": ML_AVAILABLE,
        "ml_error": ML_IMPORT_ERROR if not ML_AVAILABLE else None,
    })


@app.route("/api/analyze", methods=["POST", "OPTIONS"])
def analyze():
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return jsonify({}), 200
    """
    Accepts:
      • multipart/form-data  with field 'file'  (PDF / image / TXT)
      • application/json     with field 'text'  (raw report text)
    """
    # ── ML not loaded ─────────────────────────────────────────────────────────
    if not ML_AVAILABLE:
        return jsonify({
            "error": f"ML pipeline failed to load: {ML_IMPORT_ERROR}",
            "decision": "SERVICE UNAVAILABLE",
            "conditions": [],
            "findings": [],
            "guidance": [],
            "extracted_values": {},
            "model_results": [],
            "notes": [],
        }), 503

    try:
        # ── file upload ───────────────────────────────────────────────────────
        if "file" in request.files:
            uploaded = request.files["file"]
            if not uploaded.filename:
                return jsonify({"error": "No file selected"}), 400

            suffix = os.path.splitext(uploaded.filename)[1].lower()
            if suffix not in ALLOWED_EXTENSIONS:
                return jsonify({"error": f"Unsupported file type '{suffix}'. Use PDF, PNG, JPG, or TXT."}), 400

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
            return jsonify({"error": "Send a 'file' field (multipart) or JSON {'text': '...'}"}), 400

        return jsonify(_make_serialisable(result))

    except Exception:
        err = traceback.format_exc()
        print(f"[ERROR] /api/analyze failed:\n{err}")
        return jsonify({
            "error": "Analysis failed on the server. Check Railway logs for details.",
            "detail": err.splitlines()[-1],   # last line of traceback
            "decision": "ERROR",
            "conditions": [],
            "findings": [],
            "guidance": [],
            "extracted_values": {},
            "model_results": [],
            "notes": [],
        }), 500


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
