from pathlib import Path
import uuid

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.enums import DocumentStatus
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentRead

# Configuration
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_MIME_TYPE = "application/pdf"


class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def upload_document(self, file: UploadFile) -> DocumentRead:
        # Check that a file was provided
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file uploaded.",
            )

        # Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file extension. Only PDF files are allowed.",
            )

        # Validate MIME type
        if file.content_type != ALLOWED_MIME_TYPE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Content is not a valid PDF.",
            )

        # Read bytes before saving
        content = file.file.read()

        # Reject empty uploads
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file is empty.",
            )

        # Validate size
        file_size = len(content)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds the maximum limit of 5 MB.",
            )

        # Preserve original extension
        suffix = Path(file.filename).suffix
        stored_filename = f"{uuid.uuid4().hex}{suffix}"
        original_filename = file.filename

        # Save to disk
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)

        file_path = uploads_dir / stored_filename
        with file_path.open("wb") as buffer:
            buffer.write(content)

        # Release file handle
        file.file.close()

        repository = DocumentRepository(self.db)

        document = Document(
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            file_size=file_size,
            content_type=file.content_type or ALLOWED_MIME_TYPE,
            status=DocumentStatus.UPLOADED.value,
        )

        created_document = repository.create_document(document=document)

        return DocumentRead.model_validate(created_document)
    
    
    def get_document(self, document_id: int) -> DocumentRead:
        repository = DocumentRepository(self.db)
        document = repository.get_document_by_id(document_id=document_id)
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found.",
            )
            
        return DocumentRead.model_validate(document)
    
    def list_documents(self) -> list[DocumentRead]:
        repository = DocumentRepository(self.db)
        documents = repository.list_documents()
        return [DocumentRead.model_validate(doc) for doc in documents]
    
    def delete_document(self, document_id: int):
        repository = DocumentRepository(self.db)
        document = repository.get_document_by_id(document_id=document_id)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found.",
            )

        # Delete the file from disk
        file_path = Path(str(document.file_path))
        if file_path.exists():
            file_path.unlink()  # Delete the file
        
        # Delete from DB
        repository.delete_document(document_id=document_id)