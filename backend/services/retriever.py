from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from .embeddings import embeddings
from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue

client = QdrantClient(url="http://localhost:6333")

colletion_name = "client_documents"

if not client.collection_exists(collection_name=colletion_name):
    client.create_collection(
        collection_name=colletion_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=colletion_name,
        embedding=embeddings,
    )
else:
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=colletion_name,
        embedding=embeddings,
    )

def get_retriever(group_id: str):
    filters = Filter(
        should=[
            Filter(
                must=[
                    FieldCondition(
                        key="group_id",
                        match=MatchValue(value=group_id)
                    )
                ]
            )
        ]
    )
    return vector_store.as_retriever(kwargs={"filters": filters})