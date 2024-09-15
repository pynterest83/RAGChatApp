from uuid import uuid4
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
import torch
from transformers import BitsAndBytesConfig
from transformers import AutoTokenizer , AutoModelForCausalLM ,pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory

import warnings
warnings.filterwarnings("ignore")

TF_ENABLE_ONEDNN_OPTS=0

Loader = PyPDFLoader
FILE_PATH = "D:/Code/RAGChatApp/test/2404.05961v2.pdf"
loader = Loader(FILE_PATH)
documents = loader.load()   # Load the document

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)
print("Number of documents: ", len(docs))

vector_store.add_documents(docs)