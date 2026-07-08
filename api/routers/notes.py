from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.deps import SessionDep, CurrentUser
from models.workspace import Workspace
from models.note import Note
from models.tag import Tag
from schemas.note import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(prefix="/workspaces/{workspace_id}/notes", tags=["notes"])

async def check_workspace_access(workspace_id: int, session: SessionDep, user_id: int) -> Workspace:
    query = select(Workspace).where(Workspace.id == workspace_id, Workspace.owner_id == user_id)
    result = await session.execute(query)
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    workspace_id: int, note_in: NoteCreate, session: SessionDep, current_user: CurrentUser
):
    await check_workspace_access(workspace_id, session, current_user.id)
    
    note_data = note_in.model_dump(exclude={"tag_ids"})
    note = Note(**note_data, workspace_id=workspace_id)
    
    if note_in.tag_ids:
        query = select(Tag).where(Tag.id.in_(note_in.tag_ids), Tag.workspace_id == workspace_id)
        result = await session.execute(query)
        tags = result.scalars().all()
        note.tags = tags
        
    session.add(note)
    await session.commit()
    await session.refresh(note)
    
    # Reload with tags
    query_reload = select(Note).options(selectinload(Note.tags)).where(Note.id == note.id)
    result_reload = await session.execute(query_reload)
    return result_reload.scalar_one()

@router.get("/", response_model=list[NoteResponse])
async def read_notes(
    workspace_id: int, session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    await check_workspace_access(workspace_id, session, current_user.id)
    query = select(Note).options(selectinload(Note.tags)).where(Note.workspace_id == workspace_id).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(
    workspace_id: int, note_id: int, session: SessionDep, current_user: CurrentUser
):
    await check_workspace_access(workspace_id, session, current_user.id)
    query = select(Note).options(selectinload(Note.tags)).where(Note.id == note_id, Note.workspace_id == workspace_id)
    result = await session.execute(query)
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    workspace_id: int, note_id: int, session: SessionDep, current_user: CurrentUser
):
    await check_workspace_access(workspace_id, session, current_user.id)
    query = select(Note).where(Note.id == note_id, Note.workspace_id == workspace_id)
    result = await session.execute(query)
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    await session.delete(note)
    await session.commit()
