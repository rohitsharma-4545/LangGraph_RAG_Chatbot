from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.rag_service import rag_answer_stream
from app.db.chat_history import save_chat
from app.auth.dependencies import get_current_user

from app.services.rate_limiter import is_rate_limited
from app.services.token_limiter import is_token_exceeded
from app.utils.token_counter import estimate_tokens

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/ask-stream")
def ask_question_stream(req: QueryRequest, user=Depends(get_current_user)):
    user_id = user["user_id"]

    # 🚫 RATE LIMIT CHECK
    if is_rate_limited(user_id):
        return StreamingResponse(
            iter(["data: Rate limit exceeded. Try later.\n\n"]),
            media_type="text/event-stream"
        )

    # 💰 TOKEN LIMIT CHECK (input side)
    input_tokens = estimate_tokens(req.query)

    if is_token_exceeded(user_id, input_tokens):
        return StreamingResponse(
            iter(["data: Token limit exceeded.\n\n"]),
            media_type="text/event-stream"
        )
    
    def event_generator():
        full_response = ""

        try:
            for chunk in rag_answer_stream(req.query, user_id):
                full_response += chunk
                yield f"data: {chunk.replace('\n', ' ')}\n\n"

        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"

        output_tokens = estimate_tokens(full_response)
        is_token_exceeded(user_id, output_tokens)

        yield "data: [DONE]\n\n"

        save_chat(user_id, req.query, full_response)

    return StreamingResponse(event_generator(), media_type="text/event-stream")