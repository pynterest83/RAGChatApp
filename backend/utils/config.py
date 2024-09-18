from dotenv import load_dotenv
import os

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
DATABASE_URL = "postgresql://postgres:password@localhost:5432/ragchat_database"
SECRET_KEY = "123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30