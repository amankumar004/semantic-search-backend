from app.services.vector_service import VectorService
from app.services.embedding_service import EmbeddingService

class SearchService:
    def __init__(self):
        self.vector_service = VectorService()
        self.embedding_service = EmbeddingService()
        
    def search(self, query: str, document_id: int, user_id: int, limit: int = 5):
        # convert query into embedding
        query_embedding = self.embedding_service.get_embedding(query)

        # search qdrant for similar vectors
        results = self.vector_service.search_vectors(
            query_vector=query_embedding,
            limit=limit,
            document_id=document_id,
            user_id=user_id
        )

        return results