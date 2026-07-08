from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    workspace_id: int


class TagResponse(TagBase):
    id: int
    workspace_id: int

    model_config = ConfigDict(from_attributes=True)
