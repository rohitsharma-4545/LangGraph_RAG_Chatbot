from fastapi import FastAPI
from app.api.routes import chat, admin
from app.auth.jwt_handler import create_token
from app.db.chroma_client import get_collection

app = FastAPI(title="Enterprise RAG Chatbot")

app.include_router(chat.router, prefix="/chat")
app.include_router(admin.router, prefix="/admin")

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/token")
def get_token(user_id: str, role: str = "user"):
    return {"token": create_token(user_id, role)}

@app.get("/debug/count")
def count_docs():
    collection = get_collection()
    return {"count": collection.count()}