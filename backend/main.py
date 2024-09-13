from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from uuid import uuid4
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationalRetrievalChain
import torch
from transformers import BitsAndBytesConfig
from transformers import AutoTokenizer , AutoModelForCausalLM ,pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain_community . chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain import hub

import warnings
warnings.filterwarnings("ignore")

TF_ENABLE_ONEDNN_OPTS=0

embeddings = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key="p2Jch3wcKWOD5I2QpMaamiSCkVcgjDEzSsyLyHf4")

client = QdrantClient(url="http://localhost:6333")

if not client.collection_exists(collection_name="client_documents"):
    client.create_collection(
        collection_name="client_documents",
        vectors_config={
            "image": VectorParams(size=512, distance=Distance.DOT),
            "text": VectorParams(size=384, distance=Distance.COSINE),
        },
    )
else:
    print(f"Collection client_documents already exists.")


vector_store = QdrantVectorStore(
    client=client,
    collection_name="client_documents",
    embedding=embeddings,
)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 6})

Loader = PyPDFLoader
FILE_PATH = "D:/Code/RAGChatApp/test/2404.05961v2.pdf"
loader = Loader(FILE_PATH)
documents = loader.load()   # Load the document

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)
print("Number of documents: ", len(docs))

vector_store.add_documents(docs)

llm = ChatCohere(model="command-r-plus", cohere_api_key="p2Jch3wcKWOD5I2QpMaamiSCkVcgjDEzSsyLyHf4")

prompt = hub.pull("rlm/rag-prompt", api_key="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")

# Function to format documents into a single string
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Construct the RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# User question
USER_QUESTION = "What is the main idea of the document?"

# Invoke the chain and get the output
output = rag_chain.invoke(USER_QUESTION)

print(output)