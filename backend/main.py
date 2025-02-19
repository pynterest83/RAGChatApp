from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, rag, auth
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="RAG-SERVER",
    version="1.0",
    description="RAG-SERVER API",
)

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(rag.router, prefix="/rag", tags=["rag"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])  # New auth routes

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)