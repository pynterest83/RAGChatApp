import secrets
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def generate_group_id():
    return secrets.token_urlsafe(8)

def save_file(file):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

def process_documents(file_name, group_id):
    loader = PyPDFLoader(file_name)   # Load the document
    documents = loader.load()   # Load the document

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    all_splits = text_splitter.split_documents(documents)
    for doc in all_splits:
        doc.group_id = group_id
    return all_splits