from fastapi import FastAPI

from app.api.documents import router as documents_router

app = FastAPI(title="Semantic Search API")
app.include_router(documents_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Semantic Search API is running"}
