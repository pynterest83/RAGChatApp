from langchain_cohere import ChatCohere
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel
from langchain import hub
from utils.config import COHERE_API_KEY, LANGCHAIN_API_KEY
from typing import List

# Initialize the LLM model (Cohere) with the command-r-plus model
llm = ChatCohere(model="command-r-plus", cohere_api_key=COHERE_API_KEY)

# Pull the prompt template from a repository using a specific API key
prompt = hub.pull("rlm/rag-prompt", api_key=LANGCHAIN_API_KEY)
# Function to format documents into a single string
def format_docs(docs: List[BaseModel]) -> str:
    """Formats the documents into a concatenated string for processing."""
    return "\n\n".join(doc.page_content for doc in docs)

# Function to construct and execute the RAG chain
def build_rag_chain(retriever, user_question: str):
    """Builds and invokes the RAG chain to answer the user question."""
    
    # Define the chain of operations: retrieve, format, prompt, process with LLM, and parse the output
    rag_chain = (
        {
            "context": retriever | format_docs,  # Retrieve documents and format them
            "question": RunnablePassthrough()     # Pass the user question unchanged
        }
        | prompt                                 # Use the pre-defined prompt template
        | llm                                    # Pass the prompt to the LLM for processing
        | StrOutputParser()                      # Parse the final output as a string
    )
    
    # Invoke the chain with the user's question and return the output
    return rag_chain.invoke(user_question)