from fastapi import APIRouter, File, UploadFile
from services.embeddings import embeddings
from langchain_qdrant import QdrantVectorStore
from utils.helpers import generate_group_id, save_file, process_documents

router = APIRouter()
colletion_name = "client_documents"

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    group_id = generate_group_id()
    save_file(file)
    all_splits = process_documents(file.filename, group_id)

    client = QdrantVectorStore.from_documents(
        all_splits,
        embeddings,
        url="http://localhost:6333",
        collection_name=colletion_name,
        prefer_grpc=True,
    )

    return {"file_name": file.filename, "group_id": group_id}