from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.models import Filter, FieldCondition, MatchValue


class VectorService:

    COLLECTION_NAME = "document_chunks"

    def __init__(self):
        self.client = QdrantClient(
            host="localhost",
            port=6333
        )

    def create_collection(self):
        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )
        
    def upsert_vector(
        self,
        point_id: int,
        vector: list[float],
        payload: dict
    ):
        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id = point_id,
                    vector = vector,
                    payload = payload
                )
            ]
        )
        
    def upsert_vectors(
        self,
        vectors: list[dict]
    ):
        points = []

        for item in vectors:
            points.append(
                PointStruct(
                    id=item["point_id"],
                    vector=item["vector"],
                    payload=item["payload"]
                )
            )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points
        )
    
    def search_vectors(self, query_vector: list[float], limit: int):
        results = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query= query_vector,
            limit= limit,
            with_payload=True
        )
        
        return results.points
    
    def count_vectors(self):
        result = self.client.count(
            collection_name=self.COLLECTION_NAME
        )

        return result.count
    
    def delete_by_document_id(self, document_id: int):

        self.client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id)
                    )
                ]
            )
        )