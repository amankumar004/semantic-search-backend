from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_documents(self) -> list[Document]:
        return self.db.query(Document).all()

    def get_document_by_id(self, document_id: int) -> Document | None:
        return self.db.query(Document).filter(Document.id == document_id).first()

    def create_document(self, document: Document) -> Document:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def delete_document(self, document_id: int):
        document = self.get_document_by_id(document_id=document_id)
        if document:
            self.db.delete(document)
            self.db.commit()
            