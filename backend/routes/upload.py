from fastapi import APIRouter, File, UploadFile, Depends
from services.retriever import vector_store  # Use the same vector_store
from utils.helpers import generate_group_id, save_file, process_documents
from services.auth_services import get_current_user
from models.doc_chat import DocChat
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.config import ALGORITHM, SECRET_KEY
from jose import JWTError, jwt
from models.users import User

router = APIRouter()

@router.post("/")
async def upload_file(
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    group_id = generate_group_id()
    save_file(file)
    all_splits = process_documents(file.filename, group_id)

    # Use the centralized vector_store to store embeddings
    vector_store.add_documents(all_splits)

    # Add the document to the database
    new_doc = DocChat(group_id=group_id, doc_name=file.filename, user_id=current_user.id)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {"file_name": file.filename, "group_id": group_id}

@router.get("/")
async def get_all_docs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    docs = db.query(DocChat).filter(DocChat.user_id == current_user.id).all()
    return docs