from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from api.deps import SessionDep, CurrentUser
from models.workspace import Workspace
from schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse

router = APIRouter(prefix="/workspaces", tags=["workspaces"])

@router.post("/", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(workspace_in: WorkspaceCreate, session: SessionDep, current_user: CurrentUser):
    workspace = Workspace(**workspace_in.model_dump(), owner_id=current_user.id)
    session.add(workspace)
    await session.commit()
    await session.refresh(workspace)
    return workspace

@router.get("/", response_model=list[WorkspaceResponse])
async def read_workspaces(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100):
    query = select(Workspace).where(Workspace.owner_id == current_user.id).offset(skip).limit(limit)
    result = await session.execute(query)
    workspaces = result.scalars().all()
    return workspaces

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def read_workspace(workspace_id: int, session: SessionDep, current_user: CurrentUser):
    query = select(Workspace).where(Workspace.id == workspace_id, Workspace.owner_id == current_user.id)
    result = await session.execute(query)
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.put("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: int, workspace_in: WorkspaceUpdate, session: SessionDep, current_user: CurrentUser
):
    query = select(Workspace).where(Workspace.id == workspace_id, Workspace.owner_id == current_user.id)
    result = await session.execute(query)
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    update_data = workspace_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workspace, field, value)
        
    await session.commit()
    await session.refresh(workspace)
    return workspace

@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(workspace_id: int, session: SessionDep, current_user: CurrentUser):
    query = select(Workspace).where(Workspace.id == workspace_id, Workspace.owner_id == current_user.id)
    result = await session.execute(query)
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
        
    await session.delete(workspace)
    await session.commit()
