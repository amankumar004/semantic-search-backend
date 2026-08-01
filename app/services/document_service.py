from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentRead


class DocumentService:
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

    def list_documents(self) -> list[DocumentRead]:
        documents = self.repository.list_documents()
        return [DocumentRead.from_orm(document) for document in documents]

    def get_document(self, document_id: int) -> DocumentRead | None:
        document = self.repository.get_document(document_id)
        if document is None:
            return None
        return DocumentRead.from_orm(document)

    def create_document(self, payload: DocumentCreate) -> DocumentRead:
        document = self.repository.create_document(
            title=payload.title,
            content=payload.content,
            file_path=payload.file_path,
        )
        return DocumentRead.from_orm(document)
