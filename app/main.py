from fastapi import FastAPI
from app.database import Base, engine

from app.api.documents import router as documents_router

# create database tables
Base.metadata.create_all(bind=engine)

# initialize FastAPI app
app = FastAPI(title="Semantic Search API")

# include routers
app.include_router(documents_router)

# root endpoint
@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Semantic Search API is running"}
