import os
import uuid
import aiofiles
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from sqlalchemy import select

from api.deps import SessionDep, CurrentUser
from models.workspace import Workspace
from models.document import Document
from schemas.document import DocumentResponse

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/workspaces/{workspace_id}/documents", tags=["documents"])

async def check_workspace_access(workspace_id: int, session: SessionDep, user_id: int) -> Workspace:
    query = select(Workspace).where(Workspace.id == workspace_id, Workspace.owner_id == user_id)
    result = await session.execute(query)
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    workspace_id: int, session: SessionDep, current_user: CurrentUser, file: UploadFile = File(...)
):
    await check_workspace_access(workspace_id, session, current_user.id)
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(1024 * 1024):  # 1MB chunks
            await out_file.write(content)
    
    document = Document(
        filename=file.filename,
        file_path=file_path,
        status="uploaded",
        workspace_id=workspace_id
    )
    session.add(document)
    await session.commit()
    await session.refresh(document)
    return document

@router.get("/", response_model=list[DocumentResponse])
async def read_documents(
    workspace_id: int, session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    await check_workspace_access(workspace_id, session, current_user.id)
    query = select(Document).where(Document.workspace_id == workspace_id).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/{document_id}", response_model=DocumentResponse)
async def read_document(
    workspace_id: int, document_id: int, session: SessionDep, current_user: CurrentUser
):
    await check_workspace_access(workspace_id, session, current_user.id)
    query = select(Document).where(Document.id == document_id, Document.workspace_id == workspace_id)
    result = await session.execute(query)
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    workspace_id: int, document_id: int, session: SessionDep, current_user: CurrentUser
):
    await check_workspace_access(workspace_id, session, current_user.id)
    query = select(Document).where(Document.id == document_id, Document.workspace_id == workspace_id)
    result = await session.execute(query)
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
        
    await session.delete(document)
    await session.commit()
