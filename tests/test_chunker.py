import pytest
from services.chunker import chunk_markdown

def test_chunk_markdown():
    markdown_text = """
# Introduction
Welcome to the AI assistant. This is an introduction.

## Details
Here are the details about the assistant.
It can parse PDFs and chunk markdown files.

### Specifics
The text should be split based on these headers.
"""
    base_metadata = {"document_id": 1, "workspace_id": 2}
    
    chunks = chunk_markdown(
        markdown_text=markdown_text,
        base_metadata=base_metadata,
        chunk_size=100, # Small chunk size to force recursive splitting if needed
        chunk_overlap=20
    )
    
    assert len(chunks) > 0
    
    # Check that metadata is preserved and extended
    for chunk in chunks:
        assert chunk["metadata"]["document_id"] == 1
        assert chunk["metadata"]["workspace_id"] == 2
        assert "chunk_index" in chunk["metadata"]
        assert "page_content" in chunk
        
    # Check if header metadata is extracted
    # The first chunk should have 'Header 1' set to 'Introduction'
    assert chunks[0]["metadata"].get("Header 1") == "Introduction"
