from fastapi import APIRouter, Depends, HTTPException, Query
from models.questions import Question
from models.chat_response import ChatResponse
from services.chain import build_rag_chain
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

    print(f"Question: {question.root}")
    
    # Retrieve and run the chain
    retriever = get_retriever(group_id)
    result = build_rag_chain(retriever, question.root)

    print(result)

    return {'response': result}