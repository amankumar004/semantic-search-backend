from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

def test_count_vectors():
    service = VectorService()

    count = service.count_vectors()

    print("Vector count:", count)

    assert count >= 0
    
def test_delete_by_document_id():

    service = VectorService()

    service.delete_by_document_id(
        document_id=1
    )

    remaining = service.client.count(
        collection_name=service.COLLECTION_NAME
    )

    print("Remaining vectors:", remaining.count)

    assert remaining.count >= 0