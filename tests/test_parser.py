import os
import pytest
import pymupdf
from services.parser import parse_document

@pytest.mark.asyncio
async def test_parse_document():
    # Create a dummy PDF file
    test_pdf_path = "test_doc.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Hello, World! This is a test PDF.")
    doc.save(test_pdf_path)
    doc.close()
    
    try:
        # Test the parsing service
        markdown_text = await parse_document(test_pdf_path)
        
        assert markdown_text is not None
        assert "Hello, World!" in markdown_text
        assert "This is a test PDF." in markdown_text
    finally:
        # Cleanup
        if os.path.exists(test_pdf_path):
            os.remove(test_pdf_path)
