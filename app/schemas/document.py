from pydantic import BaseModel


class DocumentCreate(BaseModel):
    title: str
    content: str
    file_path: str | None = None


class DocumentRead(BaseModel):
    id: int
    title: str
    content: str
    file_path: str | None = None

    class Config:
        orm_mode = True
