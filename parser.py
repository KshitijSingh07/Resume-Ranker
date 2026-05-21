"""
Resume parser module.
Uses pdfplumber to extract text from PDF files.
"""

from __future__ import annotations

import pdfplumber


def clean_text(text: str) -> str:
    """Lowercase and normalize spaces/newlines."""
    return " ".join(text.lower().split())


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract full text from a PDF file and return cleaned lowercase text.
    """
    collected_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            collected_text.append(page_text)

    raw_text = "\n".join(collected_text)
    return clean_text(raw_text)

