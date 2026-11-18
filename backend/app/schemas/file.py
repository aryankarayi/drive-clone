from pydantic import BaseModel, Field
from uuid import UUID

class FileCreate(BaseModel):
    name: str = Field(min_length=1, default='File')


class FileResponse(FileCreate):
    id: UUID
    parent_id: UUID | None = None