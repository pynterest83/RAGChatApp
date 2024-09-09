#!/usr/bin/env python
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatCohere
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain_cohere import CohereEmbeddings
import os
from langchain_core.pydantic_v1 import BaseModel
from typing import List
import shutil
from fastapi import Query, Response, Cookie  # Import Query for optional query parameters
from qdrant_client.http import models
import secrets
# Load environment variables
COHERE_API_KEY = "p2Jch3wcKWOD5I2QpMaamiSCkVcgjDEzSsyLyHf4"
# Global variable to track if the document has been uploaded and processed
document_processed = False
# Initialize embeddings and Qdrant client outside of the route to reuse
embeddings = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=COHERE_API_KEY)
client = QdrantClient(url="http://localhost:6333")
collection_name = "my_documents"
qdrant_client = Qdrant(client, collection_name, embeddings)

