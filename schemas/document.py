from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    filename: str
    file_path: str
    status: str = "pending"


class DocumentCreate(DocumentBase):
    workspace_id: int


class DocumentResponse(DocumentBase):
    id: int
    workspace_id: int

    model_config = ConfigDict(from_attributes=True)
