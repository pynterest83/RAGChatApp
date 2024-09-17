from fastapi import APIRouter, Depends, HTTPException, Query
from models.questions import Question
from models.chat_response import ChatResponse
from services.chain import get_chain
from services.retriever import get_retriever

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def rag_endpoint(
    question: Question, 
    group_id: str = Query(..., description="The group_id for the document")
):
    # Ensure group_id is provided
    if not group_id:
        raise HTTPException(status_code=403, detail="Please upload a document first.")
    
    # Retrieve and run the chain
    retriever = get_retriever(group_id)
    chain = get_chain(retriever)
    result = chain.invoke(question.root)

    return {'response': result['result']}