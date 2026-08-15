from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


class SearchResult(BaseModel):
    score: float
    document_id: int
    chunk_index: int
    text: str


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]