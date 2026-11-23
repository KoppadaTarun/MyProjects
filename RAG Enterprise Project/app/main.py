from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title = settings.APP_NAME,
    debug = settings.DEBUG,
    version = "1.0.0",
    description="An Enterprise RAG Knowledge Assistant"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Enterprise RAG Assistant!",
        "status": "Running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy!"
    }