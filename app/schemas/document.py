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


class ChunkRead(BaseModel):
    chunk_index: int
    text: str


class DocumentChunksResponse(BaseModel):
    document_id: int
    total_chunks: int
    chunks: list[ChunkRead]