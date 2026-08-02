from datetime import datetime

from pydantic import BaseModel, ConfigDict

class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    stored_filename: str
    file_size: int
    content_type: str
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
