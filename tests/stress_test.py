import asyncio
import time
import httpx
from fastapi.testclient import TestClient

async def stress_test_auth():
    print("Starting Auth Stress Test (100 concurrent registrations)...")
    
    async with httpx.AsyncClient(base_url="http://test") as client:
        # Note: For httpx.AsyncClient to work without a real server, we use ASGITransport
        pass

# Actually, it's better to test against the real local ASGI app
from main import app
from httpx import ASGITransport, AsyncClient

async def run_stress_test():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        start_time = time.time()
        
        # 1. 50 Concurrent Registrations (Heavy bcrypt hashing)
        print("Starting 50 concurrent user registrations...")
        register_tasks = []
        for i in range(50):
            register_tasks.append(
                client.post("/api/auth/register", json={"email": f"stress_{i}@example.com", "password": "password123"})
            )
        
        responses = await asyncio.gather(*register_tasks)
        successes = sum(1 for r in responses if r.status_code == 201)
        print(f"Registrations Completed: {successes}/50 in {time.time() - start_time:.2f}s")
        
        # 2. 50 Concurrent Logins (Heavy bcrypt verification)
        start_time = time.time()
        print("Starting 50 concurrent user logins...")
        login_tasks = []
        for i in range(50):
            login_tasks.append(
                client.post("/api/auth/login", data={"username": f"stress_{i}@example.com", "password": "password123"})
            )
            
        responses = await asyncio.gather(*login_tasks)
        tokens = [r.json()["access_token"] for r in responses if r.status_code == 200]
        print(f"Logins Completed: {len(tokens)}/50 in {time.time() - start_time:.2f}s")
        
        # 3. Create a workspace and 100 concurrent note creations
        if not tokens:
            print("No tokens obtained, aborting further tests.")
            return
            
        token = tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        
        ws_res = await client.post("/api/workspaces/", headers=headers, json={"name": "Stress Workspace"})
        ws_id = ws_res.json()["id"]
        
        start_time = time.time()
        print("Starting 100 concurrent note creations...")
        note_tasks = []
        for i in range(100):
            note_tasks.append(
                client.post(f"/api/workspaces/{ws_id}/notes/", headers=headers, json={"title": f"Note {i}", "content": "Stress test content"})
            )
            
        responses = await asyncio.gather(*note_tasks)
        successes = sum(1 for r in responses if r.status_code == 201)
        print(f"Notes Created: {successes}/100 in {time.time() - start_time:.2f}s")
        
        # 4. Upload 20 Concurrent 1MB "Files" (simulate file uploads)
        start_time = time.time()
        print("Starting 20 concurrent file uploads...")
        upload_tasks = []
        file_content = b"a" * (1024 * 1024) # 1MB of data
        for i in range(20):
            files = {"file": (f"stress_{i}.txt", file_content, "text/plain")}
            upload_tasks.append(
                client.post(f"/api/workspaces/{ws_id}/documents/", headers=headers, files=files)
            )
            
        responses = await asyncio.gather(*upload_tasks)
        successes = sum(1 for r in responses if r.status_code == 201)
        print(f"Files Uploaded: {successes}/20 in {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(run_stress_test())
