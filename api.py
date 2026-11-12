"""
SehatSetu Flask API
Wraps the existing analyze_report.py pipeline into REST endpoints for the React frontend.

Endpoints:
  POST /api/analyze   — upload a file (PDF/JPG/PNG) or send text, get full analysis JSON
  GET  /api/health    — healthcheck
"""

import os
import sys
import json
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS

# ── path setup so imports inside SehatSetu work ──────────────────────────────
CURRENT_DIR   = os.path.dirname(os.path.abspath(__file__))
SEHATSETU_DIR = os.path.join(CURRENT_DIR, "SehatSetu")
REPORT_DIR    = os.path.join(SEHATSETU_DIR, "report_analysis")
RECOM_DIR     = os.path.join(SEHATSETU_DIR, "recommendation")

for p in (REPORT_DIR, RECOM_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

from analyze_report import analyze_report_file, analyze_report_text   # noqa: E402

# ── app ───────────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "https://*.vercel.app"])

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".txt"}


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Accepts either:
      • multipart/form-data  with field 'file'  (PDF / image / TXT)
      • application/json     with field 'text'  (raw report text)
    Returns the full analysis dict.
    """
    try:
        # ── file upload ───────────────────────────────────────────────────────
        if "file" in request.files:
            uploaded = request.files["file"]
            suffix = os.path.splitext(uploaded.filename)[1].lower()
            if suffix not in ALLOWED_EXTENSIONS:
                return jsonify({"error": f"Unsupported file type: {suffix}"}), 400

            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                uploaded.save(tmp.name)
                tmp_path = tmp.name

            try:
                result = analyze_report_file(tmp_path, use_ml=True)
            finally:
                os.unlink(tmp_path)

        # ── raw text ──────────────────────────────────────────────────────────
        elif request.is_json and request.json.get("text"):
            result = analyze_report_text(request.json["text"], use_ml=True)

        else:
            return jsonify({"error": "Send a 'file' or JSON {'text': '...'}"}), 400

        return jsonify(_make_serialisable(result))

    except Exception as exc:   # never crash the UI
        return jsonify({"error": str(exc)}), 500


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
    app.run(debug=True, port=8000)
