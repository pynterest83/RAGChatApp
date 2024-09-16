from fastapi import APIRouter, Depends, HTTPException
from models.questions import Question
from models.chat_response import ChatResponse
from services.chain import get_chain
from services.retriever import get_retriever

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def rag_endpoint(question: Question, group_id:str):
    if not group_id:
        raise HTTPException(status_code=403, detail="Please upload a document first.")
    
    retriever = get_retriever(group_id)
    chain = get_chain(retriever)
    result = chain.invoke(question.__root__)

    return {'response': result['result']}