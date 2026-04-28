import chromadb
from app.config import settings

def get_collection():
    client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
    
    return client.get_or_create_collection(
        name="company_docs"
    )