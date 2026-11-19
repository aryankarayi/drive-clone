from pydantic import BaseModel, Field
from uuid import UUID

class FileRead(BaseModel):
    name: str
    id: UUID
    parent_id: UUID | None = None