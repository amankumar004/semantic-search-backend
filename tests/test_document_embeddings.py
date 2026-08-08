from app.services.embedding_service import EmbeddingService
from app.services.text_splitter import TextSplitter


def test_chunks_to_embeddings():

    text = """
    FastAPI is a Python web framework.
    It is used to build APIs.
    Python is commonly used for backend development.
    """

    splitter = TextSplitter(
        chunk_size=100,
        overlap=10
    )

    chunks = splitter.split_text(text)

    embedding_service = EmbeddingService()

    embeddings = embedding_service.get_embeddings(chunks)

    assert len(embeddings) == len(chunks)

    for embedding in embeddings:
        assert len(embedding) == 384