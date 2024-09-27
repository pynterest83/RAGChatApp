# DocuGPT Web Application

This project is a full-stack web application for document-based interactions using GPT. The app consists of a frontend (React) and a backend (FastAPI), with backend services connected to PostgreSQL and Qdrant for storage and vector search capabilities. The backend is Dockerized and can be deployed alongside the database containers.

# How to use
1. Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo/backend
2. Configure environment variables
LANGCHAIN_API = "YOUR OWN API"
COHERE_API = "YOUR OWN API"
3. Run the backend using Docker
docker-compose up --build
4. Run the frontend
Use the provided deployed frontend link to run
