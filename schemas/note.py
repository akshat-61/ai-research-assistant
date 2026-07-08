from typing import Optional
from pydantic import BaseModel, ConfigDict
from .tag import TagResponse


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    workspace_id: int
    tag_ids: Optional[list[int]] = []


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tag_ids: Optional[list[int]] = None


class NoteResponse(NoteBase):
    id: int
    workspace_id: int
    tags: list[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)
