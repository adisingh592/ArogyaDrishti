==================================================
SEHATSETU - APPLICATION USER INTERFACE
==================================================

1. Overview:
   This folder is designated for the final interactive user interface application (Streamlit / Flask / FastAPI / React).

2. Future Architecture:
   - User inputs medical parameters or uploads medical scans (X-rays, dermoscopy, cell smears).
   - Backend calls SehatSetu/prediction/ to run model inference.
   - Prediction results are passed to SehatSetu/recommendation/ to fetch lifestyle guidance.
   - Comprehensive interactive report is rendered with interactive charts and advice.
