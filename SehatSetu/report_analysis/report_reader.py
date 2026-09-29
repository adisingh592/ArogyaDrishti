"""
SehatSetu - Medical Report Reader
Extracts plain text from a medical report file (.txt, .pdf, image scan) or a JSON of values.

PDF support needs:    pip install pypdf
Image (OCR) support:  pip install pytesseract pillow  (+ install the Tesseract OCR program)
"""

import json
import os

TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".log"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}


class ReportReadError(Exception):
    pass


def read_pdf(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ReportReadError("Reading PDF reports needs the 'pypdf' package. Install it with: pip install pypdf")

    reader = PdfReader(path)
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages).strip()
    if not text:
        raise ReportReadError(
            "No text found in this PDF (it is probably a scanned image). "
            "Save the page as an image (PNG/JPG) and pass that instead so OCR can read it."
        )
    return text


def read_image(path):
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        raise ReportReadError(
            "Reading scanned reports needs OCR. Install with: pip install pytesseract pillow "
            "and install the Tesseract program (https://github.com/tesseract-ocr/tesseract)."
        )
    try:
        return pytesseract.image_to_string(Image.open(path))
    except pytesseract.TesseractNotFoundError:
        raise ReportReadError("Tesseract OCR program is not installed or not on PATH.")


def read_report(path):
    """
    Returns (text, values). For a .json file, values is a dict of parameters
    (e.g. {"hba1c": 7.1, "sex": "male"}) and text is empty; otherwise values is None.
    """
    if not os.path.exists(path):
        raise ReportReadError(f"File not found: {path}")

    ext = os.path.splitext(path)[1].lower()

    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return "", json.load(f)
    if ext == ".pdf":
        return read_pdf(path), None
    if ext in IMAGE_EXTENSIONS:
        return read_image(path), None
    if ext in TEXT_EXTENSIONS or ext == "":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(), None

    raise ReportReadError(f"Unsupported report format '{ext}'. Use .txt, .pdf, .json or an image file.")
