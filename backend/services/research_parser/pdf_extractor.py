# pdf_extractor.py — extracts raw text from uploaded PDF files
import fitz  # PyMuPDF
import pdfplumber
from pathlib import Path


def extract_text_pymupdf(pdf_path: str) -> str:
    """Primary extraction using PyMuPDF — fast and reliable."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"PyMuPDF extraction failed: {e}")
    return text


def extract_text_pdfplumber(pdf_path: str) -> str:
    """Fallback extraction using pdfplumber — better for tables."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber extraction failed: {e}")
    return text


def extract_text(pdf_path: str) -> str:
    """Try PyMuPDF first, fall back to pdfplumber if too short."""
    text = extract_text_pymupdf(pdf_path)
    if len(text.strip()) < 100:
        print("PyMuPDF got too little text, trying pdfplumber...")
        text = extract_text_pdfplumber(pdf_path)
    return text


def get_pdf_metadata(pdf_path: str) -> dict:
    """Extract basic metadata from PDF file."""
    metadata = {}
    try:
        doc = fitz.open(pdf_path)
        meta = doc.metadata
        metadata = {
            "title": meta.get("title", ""),
            "author": meta.get("author", ""),
            "subject": meta.get("subject", ""),
            "pages": doc.page_count,
        }
        doc.close()
    except Exception as e:
        print(f"Metadata extraction failed: {e}")
    return metadata