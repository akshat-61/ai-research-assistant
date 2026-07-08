import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_tags_crud(async_client: AsyncClient):
    # 1. Register and Login
    await async_client.post(
        "/api/auth/register",
        json={"email": "tags_test@example.com", "password": "password123"}
    )
    login_response = await async_client.post(
        "/api/auth/login",
        data={"username": "tags_test@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create Workspace
    ws_response = await async_client.post(
        "/api/workspaces/",
        headers=headers,
        json={"name": "Tags Workspace"}
    )
    ws_id = ws_response.json()["id"]
    
    # 3. Create Tag
    tag_response = await async_client.post(
        f"/api/workspaces/{ws_id}/tags/",
        headers=headers,
        json={"name": "Important"}
    )
    assert tag_response.status_code == 201
    tag_id = tag_response.json()["id"]
    assert tag_response.json()["name"] == "Important"
    
    # 4. Read Tags
    list_response = await async_client.get(
        f"/api/workspaces/{ws_id}/tags/",
        headers=headers
    )
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    
    # 5. Delete Tag
    delete_response = await async_client.delete(
        f"/api/workspaces/{ws_id}/tags/{tag_id}",
        headers=headers
    )
    assert delete_response.status_code == 204
    
    # Verify deletion
    verify_del = await async_client.get(
        f"/api/workspaces/{ws_id}/tags/",
        headers=headers
    )
    assert len(verify_del.json()) == 0
