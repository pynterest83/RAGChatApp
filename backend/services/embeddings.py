from langchain_cohere import CohereEmbeddings
import os
from utils.config import COHERE_API_KEY

embeddings = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=COHERE_API_KEY)