import chromadb
from app.config import settings

chroma_client = chromadb.PersistentClient(
    path=settings.CHROMA_PERSIST_DIRECTORY
)