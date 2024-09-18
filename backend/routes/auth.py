# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.auth_services import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session
from models.users import User
from utils.db import get_db
from datetime import timedelta
from utils.config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_pw, register_at=datetime.utcnow().date())
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
