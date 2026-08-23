from app.core.celery_app import celery_app
from app.database import SessionLocal
from app.services.document_service import DocumentService


@celery_app.task
def process_document_task(document_id: int, user_id: int):
    db = SessionLocal()

    try:
        document_service = DocumentService(db=db)

        return document_service.process_document(
            document_id=document_id,
            user_id=user_id,
        )

    finally:
        db.close()


def enqueue_document_processing(document_id: int, user_id: int):
    return process_document_task.delay(  # type: ignore[attr-defined]
        document_id=document_id,
        user_id=user_id,
    )