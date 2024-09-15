from fastapi import Depends
from langchain.chains import RetrievalQA, StuffDocumentsChain, LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatCohere
from .retriever import get_retriever
from .embeddings import embeddings
import os
from utils.config import COHERE_API_KEY

model_name = "command-r-plus"

def get_chain(retriever=Depends(get_retriever)):
    template = """Answer the question based only on the following context:
    {context}
    Question: {question}"""
    
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatCohere(model=model_name, cohere_api_key=COHERE_API_KEY)
    output_parser = StrOutputParser()

    # Create the LLMChain
    llm_chain = LLMChain(llm=model, prompt=prompt, output_parser=output_parser)

    # Create the StuffDocumentsChain
    stuff_documents_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="context")

    # Create the RetrievalQA chain
    return RetrievalQA(combine_documents_chain=stuff_documents_chain, retriever=retriever)