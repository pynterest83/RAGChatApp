from fastapi import APIRouter, File, UploadFile
from services.retriever import vector_store  # Use the same vector_store
from utils.helpers import generate_group_id, save_file, process_documents

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    group_id = generate_group_id()
    save_file(file)
    all_splits = process_documents(file.filename, group_id)

    # Use the centralized vector_store to store embeddings
    vector_store.add_documents(all_splits)

    return {"file_name": file.filename, "group_id": group_id}