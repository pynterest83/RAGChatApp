from fastapi import APIRouter, Depends, HTTPException, Query
from models.questions import Question
from models.chat_response import ChatResponse
from services.chain import build_rag_chain
from services.retriever import get_retriever
from utils.db import get_db
from models.messages import Message
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def rag_endpoint(
    question: Question, 
    group_id: str = Query(..., description="The group_id for the document"),
    db: Session = Depends(get_db)
):
    # Ensure group_id is provided
    if not group_id:
        raise HTTPException(status_code=403, detail="Please upload a document first.")
    
    # Retrieve and run the chain
    retriever = get_retriever(group_id)
    result = build_rag_chain(retriever, question.root)

    # Save the response to the database
    user_id = 1
    bot_id = 0
    user_message = Message(group_id=group_id, message=question.root, sender_id=user_id)
    bot_message = Message(group_id=group_id, message=result, sender_id=bot_id)
    db.add(user_message)
    db.add(bot_message)
    db.commit()
    db.refresh(user_message)
    db.refresh(bot_message)

    return {'response': result}

@router.get("/")
async def load_rag(
    group_id: str = Query(..., description="The group_id for the document"),
    db: Session = Depends(get_db)
):
    # Ensure group_id is provided
    if not group_id:
        raise HTTPException(status_code=403, detail="Please provide a group_id.")

    # Retrieve the conversation for the group_id
    messages = db.query(Message).filter(Message.group_id == group_id).all()

    # If no messages found, return an empty list
    if not messages:
        return {"conversation": []}

    # Format the conversation for the frontend
    conversation = []
    for msg in messages:
        # If sender_id is 1, mark it as 'user', else 'bot'
        sender = "user" if msg.sender_id == 1 else "bot"
        conversation.append({
            "text": msg.message,
            "from": sender,
            "order": msg.message_id
        })
    
    # Sort the conversation by the 'order' (message_id)
    sorted_conversation = sorted(conversation, key=lambda x: x["order"], reverse=True)

    return {"conversation": sorted_conversation}