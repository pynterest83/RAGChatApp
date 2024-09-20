from fastapi import APIRouter, File, UploadFile, Depends
from services.retriever import vector_store  # Use the same vector_store
from utils.helpers import generate_group_id, save_file, process_documents
from services.auth_services import get_user_by_username
from models.doc_chat import DocChat
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.config import ALGORITHM, SECRET_KEY
from jose import JWTError, jwt


router = APIRouter()

@router.post("/")
async def upload_file(
    access_token: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    group_id = generate_group_id()
    save_file(file)
    all_splits = process_documents(file.filename, group_id)

    # Use the centralized vector_store to store embeddings
    vector_store.add_documents(all_splits)

    # Get the user_id from the access_token
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_name = payload.get("sub")
    current_user = get_user_by_username(db, user_name)

    # Add the document to the database
    new_doc = DocChat(group_id=group_id, doc_name=file.filename, user_id=current_user.id)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {"file_name": file.filename, "group_id": group_id}