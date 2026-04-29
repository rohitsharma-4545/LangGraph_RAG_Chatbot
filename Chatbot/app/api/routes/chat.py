from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.rag_service import rag_answer_stream
from app.db.chat_history import save_chat
from app.auth.dependencies import get_current_user

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/ask-stream")
def ask_question_stream(req: QueryRequest, user=Depends(get_current_user)):
    user_id = user["user_id"]
    
    def event_generator():
        full_response = ""

        try:
            for chunk in rag_answer_stream(req.query, user_id):
                full_response += chunk
                yield f"data: {chunk.replace('\n', ' ')}\n\n"

        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"

        yield "data: [DONE]\n\n"

        save_chat(user_id, req.query, full_response)

    return StreamingResponse(event_generator(), media_type="text/event-stream")