import os
import pymupdf4llm

async def parse_document(file_path: str) -> str:
    """
    Parse a document (PDF, etc.) into Markdown text.
    Uses pymupdf4llm for highly accurate PDF to Markdown conversion.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    # pymupdf4llm.to_markdown returns markdown text directly
    md_text = pymupdf4llm.to_markdown(file_path)
    return md_text
