"""
PDF/Document Reader Tool
Fallback-based PDF text extraction (no external deps required).
"""

import os
import subprocess
from typing import Optional
from pathlib import Path


class PDFDocReader:
    """PDF and document reader with multiple fallback strategies."""
    
    def __init__(self):
        self.max_chars = 10000  # Limit extraction size
    
    def read_pdf(self, filepath: str) -> Optional[str]:
        """
        Read PDF using available system tools.
        Tries: pdftotext -> pdfgrep -> fallback
        """
        if not os.path.exists(filepath):
            return None
        
        # Try pdftotext (poppler-utils)
        try:
            result = subprocess.run(
                ['pdftotext', filepath, '-'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout[:self.max_chars]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Try pdfgrep (fallback)
        try:
            result = subprocess.run(
                ['pdfgrep', '-a', '.', filepath],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout[:self.max_chars]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return None
    
    def read_markdown(self, filepath: str) -> Optional[str]:
        """Read markdown file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()[:self.max_chars]
        except Exception:
            return None
    
    def read_text(self, filepath: str) -> Optional[str]:
        """Read plain text file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()[:self.max_chars]
        except Exception:
            return None
    
    def read_document(self, filepath: str) -> Optional[str]:
        """Auto-detect and read document type."""
        ext = Path(filepath).suffix.lower()
        
        if ext == '.pdf':
            return self.read_pdf(filepath)
        elif ext in ['.md', '.markdown']:
            return self.read_markdown(filepath)
        elif ext in ['.txt', '.text']:
            return self.read_text(filepath)
        else:
            # Try as text fallback
            return self.read_text(filepath)
