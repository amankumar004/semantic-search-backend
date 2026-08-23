from app.core.celery_app import celery_app
from app.database import SessionLocal
from app.models.enums import DocumentStatus
from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService


@celery_app.task(
    bind=True,
    max_retries=3,
)
def process_document_task(self, document_id: int, user_id: int):

    db = SessionLocal()
    repository = DocumentRepository(db)
    

    try:

        document = repository.get_document_by_id_for_user(
            document_id=document_id,
            user_id=user_id,
        )

        if not document:
            raise ValueError(
                f"Document {document_id} not found for user {user_id}"
            )

        repository.update_status(
            document_id=document_id,
            status=DocumentStatus.PROCESSING.value,
        )

        document_service = DocumentService(db=db)

        result = document_service.process_document(
            document_id=document_id,
            user_id=user_id,
        )

        repository.update_status(
            document_id=document_id,
            status=DocumentStatus.COMPLETED.value,
        )

        return result

    except Exception as exc:

        if self.request.retries < self.max_retries:
            raise self.retry(
                exc=exc,
                countdown=5 * (2 ** self.request.retries),
            )

        repository.update_status(
            document_id=document_id,
            status=DocumentStatus.FAILED.value,
        )

        raise

    finally:
        db.close()



def enqueue_document_processing(
    document_id: int,
    user_id: int,
):
    return process_document_task.delay(  # type: ignore[attr-defined]
        document_id=document_id,
        user_id=user_id,
    )