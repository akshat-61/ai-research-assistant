import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_workspace(async_client: AsyncClient):
    # Register and login to get token
    await async_client.post(
        "/api/auth/register",
        json={"email": "workspace@example.com", "password": "password123"}
    )
    login_response = await async_client.post(
        "/api/auth/login",
        data={"username": "workspace@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Create workspace
    response = await async_client.post(
        "/api/workspaces/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Workspace", "description": "A workspace for testing"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Workspace"
    assert data["description"] == "A workspace for testing"
    assert "id" in data
    assert "owner_id" in data

@pytest.mark.asyncio
async def test_read_workspaces(async_client: AsyncClient):
    login_response = await async_client.post(
        "/api/auth/login",
        data={"username": "workspace@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    response = await async_client.get(
        "/api/workspaces/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Test Workspace"

@pytest.mark.asyncio
async def test_update_and_delete_workspace(async_client: AsyncClient):
    login_response = await async_client.post(
        "/api/auth/login",
        data={"username": "workspace@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get all to find ID
    response = await async_client.get("/api/workspaces/", headers=headers)
    ws_id = response.json()[0]["id"]
    
    # Read single
    single_response = await async_client.get(f"/api/workspaces/{ws_id}", headers=headers)
    assert single_response.status_code == 200
    assert single_response.json()["name"] == "Test Workspace"
    
    # Update
    update_response = await async_client.put(
        f"/api/workspaces/{ws_id}",
        headers=headers,
        json={"name": "Updated Workspace", "description": "Updated"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Workspace"
    
    # Delete
    delete_response = await async_client.delete(f"/api/workspaces/{ws_id}", headers=headers)
    assert delete_response.status_code == 204
    
    # Verify deletion
    verify_response = await async_client.get(f"/api/workspaces/{ws_id}", headers=headers)
    assert verify_response.status_code == 404
