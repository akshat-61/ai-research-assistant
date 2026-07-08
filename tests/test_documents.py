import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_upload_document(async_client: AsyncClient):
    # Register and login
    await async_client.post(
        "/api/auth/register",
        json={"email": "doc_test@example.com", "password": "password123"}
    )
    login_response = await async_client.post(
        "/api/auth/login",
        data={"username": "doc_test@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create workspace
    workspace_response = await async_client.post(
        "/api/workspaces/",
        headers=headers,
        json={"name": "Doc Workspace"}
    )
    workspace_id = workspace_response.json()["id"]
    
    # Upload document
    file_content = b"This is a test document."
    files = {"file": ("test_doc.txt", file_content, "text/plain")}
    
    response = await async_client.post(
        f"/api/workspaces/{workspace_id}/documents/",
        headers=headers,
        files=files
    )
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "test_doc.txt"
    assert data["status"] == "uploaded"
    assert "id" in data
    
    # Clean up (Optional, since it's an in-memory DB, but uploads directory might have the file)
    # We can delete it or just let the test finish.
    
    # Verify retrieval
    doc_id = data["id"]
    get_response = await async_client.get(
        f"/api/workspaces/{workspace_id}/documents/{doc_id}",
        headers=headers
    )
    assert get_response.status_code == 200
    assert get_response.json()["filename"] == "test_doc.txt"
    
    # Verify list
    list_response = await async_client.get(
        f"/api/workspaces/{workspace_id}/documents/",
        headers=headers
    )
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    
    # Delete document
    delete_response = await async_client.delete(
        f"/api/workspaces/{workspace_id}/documents/{doc_id}",
        headers=headers
    )
    assert delete_response.status_code == 204
    
    # Verify deletion
    verify_del = await async_client.get(
        f"/api/workspaces/{workspace_id}/documents/{doc_id}",
        headers=headers
    )
    assert verify_del.status_code == 404
