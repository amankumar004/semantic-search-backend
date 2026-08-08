from app.services.embedding_service import EmbeddingService

def test_get_embedding():
    service = EmbeddingService()

    text = "FastAPI is a Python web framework."

    embedding = service.get_embedding(text)

    assert len(embedding) == 384
    assert isinstance(embedding, list)


def test_get_embeddings():
    service = EmbeddingService()

    texts = [
        "FastAPI is a Python web framework.",
        "Python is used for backend development.",
        "Qdrant is a vector database."
    ]

    embeddings = service.get_embeddings(texts)

    assert len(embeddings) == 3

    for embedding in embeddings:
        assert len(embedding) == 384