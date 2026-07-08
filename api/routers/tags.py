from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from api.deps import SessionDep, CurrentUser
from models.workspace import Workspace
from models.tag import Tag
from schemas.tag import TagCreate, TagResponse

router = APIRouter(prefix="/workspaces/{workspace_id}/tags", tags=["tags"])

async def check_workspace_access(workspace_id: int, session: SessionDep, user_id: int) -> Workspace:
    query = select(Workspace).where(Workspace.id == workspace_id, Workspace.owner_id == user_id)
    result = await session.execute(query)
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    workspace_id: int, tag_in: TagCreate, session: SessionDep, current_user: CurrentUser
):
    await check_workspace_access(workspace_id, session, current_user.id)
    
    tag = Tag(**tag_in.model_dump(), workspace_id=workspace_id)
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag

@router.get("/", response_model=list[TagResponse])
async def read_tags(
    workspace_id: int, session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    await check_workspace_access(workspace_id, session, current_user.id)
    query = select(Tag).where(Tag.workspace_id == workspace_id).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    workspace_id: int, tag_id: int, session: SessionDep, current_user: CurrentUser
):
    await check_workspace_access(workspace_id, session, current_user.id)
    query = select(Tag).where(Tag.id == tag_id, Tag.workspace_id == workspace_id)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
        
    await session.delete(tag)
    await session.commit()
