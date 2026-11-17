from pydantic import BaseModel, Field
from uuid import UUID

class FolderCreate(BaseModel):
    name: str = Field(min_length=1)

class FolderResponse(FolderCreate):
    id: UUID

class FolderUpdate(FolderCreate):
    pass