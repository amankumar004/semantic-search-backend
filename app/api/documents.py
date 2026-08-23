from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session
from typing import Any, cast

from app.database import get_db
from app.schemas.document import DocumentChunksResponse, DocumentRead
from app.services.document_service import DocumentService
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search_service import SearchService
from app.api.dependencies import get_current_user
from app.models.user import User
from app.tasks.document_tasks import enqueue_document_processing


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post(
    "/upload",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> DocumentRead:

    service = DocumentService(db)

    document = service.upload_document(
        file=file,
        user_id=current_user.id,
    )

    enqueue_document_processing(
        document_id=document.id,
        user_id=current_user.id,
    )

    return document


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> DocumentRead:
    service = DocumentService(db)
    return service.get_document(document_id=document_id, user_id=current_user.id)

@router.get("/", response_model=list[DocumentRead])
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[DocumentRead]:
    service = DocumentService(db)
    return service.list_documents(user_id=current_user.id)

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = DocumentService(db)
    service.delete_document(document_id=document_id, user_id=current_user.id)

@router.get("/{document_id}/chunks", response_model=DocumentChunksResponse)
def get_document_chunks(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = DocumentService(db)
    return service.get_document_chunks(document_id=document_id, user_id=current_user.id)

@router.post("/{document_id}/process", status_code=status.HTTP_200_OK)
def process_document(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = DocumentService(db)
    return service.process_document(document_id=document_id, user_id=current_user.id)

@router.post("/search/{document_id}", response_model=SearchResponse)
def search_documents(document_id: int, request: SearchRequest, current_user: User = Depends(get_current_user)):
    search_service = SearchService()
    results = search_service.search(
        query=request.query,
        document_id=document_id,
        user_id=current_user.id,
        limit=request.limit
    )
    
    formatted_results = []
    
    for result in results:
        payload = result.payload or {}

        formatted_results.append({
            "score": result.score,
            "document_id": payload.get("document_id"),
            "chunk_index": payload.get("chunk_index"),
            "text": payload.get("text")
        })

    return SearchResponse(query=request.query, results=formatted_results)
        
        