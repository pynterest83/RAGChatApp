from langchain_cohere import ChatCohere
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.pydantic_v1 import BaseModel
from langchain import hub
from utils.config import COHERE_API_KEY, LANGCHAIN_API_KEY
from typing import List

# Initialize the LLM model (Cohere) with the command-r-plus model
llm = ChatCohere(model="command-r-plus", cohere_api_key=COHERE_API_KEY)

# Pull the prompt template from a repository using a specific API key
prompt = hub.pull("rlm/rag-prompt", api_key=LANGCHAIN_API_KEY)

# Ensure the prompt is formatted correctly (make it a Runnable if necessary)
def prompt_runnable(inputs):
    context = inputs['context']
    question = inputs['question']
    return prompt.format(context=context, question=question)

# Function to format documents into a single string
def format_docs(docs: List[BaseModel]) -> str:
    """Formats the documents into a concatenated string for processing."""
    return "\n\n".join(doc.page_content for doc in docs)

# Function to construct and execute the RAG chain
def build_rag_chain(retriever, user_question: str):
    """Builds and invokes the RAG chain to answer the user question."""
    
    # Retrieve relevant documents
    retrieved_docs = retriever.invoke(user_question)

    # Format the retrieved documents
    formatted_context = format_docs(retrieved_docs)
    
    # Define the chain of operations
    rag_chain = (
        {
            "context": RunnableLambda(lambda x: formatted_context),  # Provide the formatted context
            "question": RunnablePassthrough()                         # Pass the user question unchanged
        }
        | RunnableLambda(prompt_runnable)                           # Format the prompt dynamically using a RunnableLambda
        | llm                                                        # Pass the prompt to the LLM for processing
        | StrOutputParser()                                          # Parse the final output as a string
    )
    
    # Invoke the chain with the user's question and return the output
    return rag_chain.invoke({"context": formatted_context, "question": user_question})