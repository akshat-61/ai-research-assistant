import pytest
from unittest.mock import patch, AsyncMock
from services.embeddings import generate_embeddings

class MockEmbeddingResponse:
    def __init__(self, embedding):
        self.embedding = embedding

class MockResponse:
    def __init__(self, data):
        self.data = data

@pytest.mark.asyncio
async def test_generate_embeddings():
    # Setup mock data
    texts = ["chunk 1", "chunk 2"]
    mock_data = [
        MockEmbeddingResponse([0.1, 0.2, 0.3]),
        MockEmbeddingResponse([0.4, 0.5, 0.6])
    ]
    mock_response = MockResponse(mock_data)
    
    # Mock the embeddings.create method
    with patch("services.embeddings.client.embeddings.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_response
        
        embeddings = await generate_embeddings(texts)
        
        # Verify
        mock_create.assert_called_once()
        assert len(embeddings) == 2
        assert embeddings[0] == [0.1, 0.2, 0.3]
        assert embeddings[1] == [0.4, 0.5, 0.6]

@pytest.mark.asyncio
async def test_generate_embeddings_empty():
    embeddings = await generate_embeddings([])
    assert embeddings == []
