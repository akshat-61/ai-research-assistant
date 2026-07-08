import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from schemas.chat import ChatResponse

class MockChoice:
    def __init__(self, message_content):
        self.message = type("Message", (), {"content": message_content})

class MockChatCompletionResponse:
    def __init__(self, message_content):
        self.choices = [MockChoice(message_content)]

@pytest.mark.asyncio
async def test_chat_endpoint(async_client: AsyncClient):
    # Register and login
    await async_client.post(
        "/api/auth/register",
        json={"email": "chat_test@example.com", "password": "password123"}
    )
    login_response = await async_client.post(
        "/api/auth/login",
        data={"username": "chat_test@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create workspace
    workspace_response = await async_client.post(
        "/api/workspaces/",
        headers=headers,
        json={"name": "Chat Workspace"}
    )
    workspace_id = workspace_response.json()["id"]
    
    mock_response = MockChatCompletionResponse("This is a mock AI response.")
    
    with patch("services.llm.client.chat.completions.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_response
        
        response = await async_client.post(
            f"/api/workspaces/{workspace_id}/chat/",
            headers=headers,
            json={"query": "What is AI?"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "This is a mock AI response."
