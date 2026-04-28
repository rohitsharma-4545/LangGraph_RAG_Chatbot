from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.api.routes import chat, admin
from app.auth.jwt_handler import create_token
from app.db.chroma_client import get_collection
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Enterprise RAG Chatbot")

app.include_router(chat.router, prefix="/chat")
app.include_router(admin.router, prefix="/admin")

@app.get("/")
def root():
    return {"status": "running"}

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

class AuthRequest(BaseModel):
    user_id: str
    role: str = "user"
    password: str | None = None


@app.post("/token")
def get_token(req: AuthRequest):
    if req.role == "admin":
        if not req.password or req.password != ADMIN_PASSWORD:
            raise HTTPException(status_code=401, detail="Invalid admin password")

    return {"token": create_token(req.user_id, req.role)}

@app.get("/debug/count")
def count_docs():
    collection = get_collection()
    return {"count": collection.count()}