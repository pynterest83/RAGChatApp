import secrets
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def generate_group_id():
    return secrets.token_urlsafe(8)

def save_file(file):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

def process_documents(filename, group_id):
    loader = PyPDFLoader(filename)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    all_splits = text_splitter.split_documents(data)

    # Add group_id to the document's metadata
    for doc in all_splits:
        doc.metadata['group_id'] = group_id

    os.remove(filename)

    return all_splits