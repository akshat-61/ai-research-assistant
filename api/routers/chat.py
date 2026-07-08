from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from api.deps import SessionDep, CurrentUser
from models.workspace import Workspace
from schemas.chat import ChatRequest, ChatResponse
from services.llm import generate_chat_response

router = APIRouter(prefix="/workspaces/{workspace_id}/chat", tags=["chat"])

async def check_workspace_access(workspace_id: int, session: SessionDep, user_id: int) -> Workspace:
    query = select(Workspace).where(Workspace.id == workspace_id, Workspace.owner_id == user_id)
    result = await session.execute(query)
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.post("/", response_model=ChatResponse)
async def chat_with_workspace(
    workspace_id: int, request: ChatRequest, session: SessionDep, current_user: CurrentUser
):
    await check_workspace_access(workspace_id, session, current_user.id)
    
    # Hardcoded context for Phase 2
    dummy_context = "This workspace contains documents about Artificial Intelligence and its applications in modern research."
    
    answer = await generate_chat_response(request.query, dummy_context)
    
    return ChatResponse(answer=answer)
