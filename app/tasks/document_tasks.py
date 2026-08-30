from app.database import SessionLocal
from app.models.enums import DocumentStatus
from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService


def process_document_background(document_id: int, user_id: int):

    db = SessionLocal()
    repository = DocumentRepository(db)

    try:

        document = repository.get_document_by_id_for_user(
            document_id=document_id,
            user_id=user_id,
        )

        if not document:
            return

        repository.update_status(
            document_id=document_id,
            status=DocumentStatus.PROCESSING.value,
        )

        document_service = DocumentService(db=db)

        document_service.process_document(
            document_id=document_id,
            user_id=user_id,
        )

        repository.update_status(
            document_id=document_id,
            status=DocumentStatus.COMPLETED.value,
        )

    except Exception:
        repository.update_status(
            document_id=document_id,
            status=DocumentStatus.FAILED.value,
        )
        raise

    finally:
        db.close()
