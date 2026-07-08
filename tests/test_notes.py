import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_notes_crud(async_client: AsyncClient):
    # 1. Register and Login
    await async_client.post(
        "/api/auth/register",
        json={"email": "notes_test@example.com", "password": "password123"}
    )
    login_response = await async_client.post(
        "/api/auth/login",
        data={"username": "notes_test@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create Workspace
    ws_response = await async_client.post(
        "/api/workspaces/",
        headers=headers,
        json={"name": "Notes Workspace"}
    )
    ws_id = ws_response.json()["id"]
    
    # 3. Create Note
    note_response = await async_client.post(
        f"/api/workspaces/{ws_id}/notes/",
        headers=headers,
        json={"title": "First Note", "content": "This is the content"}
    )
    assert note_response.status_code == 201
    note_id = note_response.json()["id"]
    assert note_response.json()["title"] == "First Note"
    
    # 4. Read Notes
    list_response = await async_client.get(
        f"/api/workspaces/{ws_id}/notes/",
        headers=headers
    )
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    
    # 5. Read Single Note
    get_response = await async_client.get(
        f"/api/workspaces/{ws_id}/notes/{note_id}",
        headers=headers
    )
    assert get_response.status_code == 200
    assert get_response.json()["content"] == "This is the content"
    
    # 6. Update Note
    update_response = await async_client.put(
        f"/api/workspaces/{ws_id}/notes/{note_id}",
        headers=headers,
        json={"title": "Updated Note"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Note"
    assert update_response.json()["content"] == "This is the content"
    
    # 7. Delete Note
    delete_response = await async_client.delete(
        f"/api/workspaces/{ws_id}/notes/{note_id}",
        headers=headers
    )
    assert delete_response.status_code == 204
    
    # Verify deletion
    verify_del = await async_client.get(
        f"/api/workspaces/{ws_id}/notes/{note_id}",
        headers=headers
    )
    assert verify_del.status_code == 404
