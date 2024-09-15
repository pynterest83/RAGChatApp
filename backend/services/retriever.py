from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from .embeddings import embeddings
from qdrant_client.http.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")

colletion_name = "client_documents"

if not client.collection_exists(collection_name=colletion_name):
    client.create_collection(
        collection_name=colletion_name,
        vectors_config={
            "image": VectorParams(size=512, distance=Distance.DOT),
            "text": VectorParams(size=384, distance=Distance.COSINE),
        },
    )
else:
    print(f"Collection client_documents already exists.")


vector_store = QdrantVectorStore(
    client=client,
    collection_name=colletion_name,
    embedding=embeddings,
)

def get_retriever(group_id: str):
    return client.as_retriever(
        search_kwargs={'filter': {'group_id': group_id}}
    )