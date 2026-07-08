from typing import Any
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

def chunk_markdown(
    markdown_text: str,
    base_metadata: dict[str, Any],
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[dict[str, Any]]:
    """
    Splits markdown text into smaller chunks based on headers, and then by character
    length if sections are too large.
    Returns a list of dictionaries, each containing 'page_content' and 'metadata'.
    """
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
    ]
    
    # 1. Split by Markdown headers
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False,
    )
    md_header_splits = markdown_splitter.split_text(markdown_text)
    
    # 2. Split large sections by characters to fit LLM context window
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    final_splits = text_splitter.split_documents(md_header_splits)
    
    # 3. Add base metadata (e.g., workspace_id, document_id) to all chunks
    chunks = []
    for i, split in enumerate(final_splits):
        metadata = base_metadata.copy()
        metadata.update(split.metadata)
        metadata["chunk_index"] = i
        
        chunks.append({
            "page_content": split.page_content,
            "metadata": metadata
        })
        
    return chunks
