from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingService:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.embedding_model
        self.model = SentenceTransformer(self.model_name)

    def get_embedding(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()