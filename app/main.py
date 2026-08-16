from fastapi import FastAPI

from app.database import Base, engine

# Import models so SQLAlchemy registers them with Base.metadata
from app.models.user import User
from app.models.document import Document

from app.api.documents import router as documents_router
from app.api.auth import router as auth_router
from app.api.dependencies import get_current_user
from app.models.user import User
from fastapi import Depends


# Create database tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI app
app = FastAPI(title="Semantic Search API")


# Include routers
app.include_router(auth_router)
app.include_router(documents_router)


# Root endpoint
@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Semantic Search API is running"}

@app.get("/auth/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email
    }