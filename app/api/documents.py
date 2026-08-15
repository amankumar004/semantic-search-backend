from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.document import DocumentChunksResponse, DocumentRead
from app.services.document_service import DocumentService
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search_service import SearchService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> DocumentRead:
    service = DocumentService(db)
    return service.upload_document(file=file)


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(document_id: int, db: Session = Depends(get_db)) -> DocumentRead:
    service = DocumentService(db)
    return service.get_document(document_id=document_id)

@router.get("/", response_model=list[DocumentRead])
def list_documents(db: Session = Depends(get_db)) -> list[DocumentRead]:
    service = DocumentService(db)
    return service.list_documents()

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    service.delete_document(document_id=document_id)
    
@router.get("/{document_id}/chunks", response_model=DocumentChunksResponse)
def get_document_chunks(document_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_document_chunks(document_id=document_id)

@router.post("/{document_id}/process", status_code=status.HTTP_200_OK)
def process_document(document_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.process_document(document_id=document_id)

@router.post("/search", response_model=SearchResponse)
def search_documents(request: SearchRequest):
    search_service = SearchService()
    results = search_service.search(
        query=request.query,
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
        
        