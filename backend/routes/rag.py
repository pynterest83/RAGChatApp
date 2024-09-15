from fastapi import APIRouter, Depends, HTTPException
from backend.models.questions import Question
from backend.models.chat_response import ChatResponse
from backend.services.chain import get_chain
from backend.services.retriever import get_retriever

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def rag_endpoint(question: Question, group_id:str):
    if not group_id:
        raise HTTPException(status_code=403, detail="Please upload a document first.")
    
    retriever = get_retriever(group_id)
    chain = get_chain(retriever)
    result = chain.invoke(question.__root__)

    return {'response': result['result']}