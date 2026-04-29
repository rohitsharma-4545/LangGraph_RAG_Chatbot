from app.services.vector_store import hybrid_search
from app.db.chat_history import get_chat_history
from app.services.llm_service import stream_response

def rag_answer_stream(query: str, user_id: str):
    docs = hybrid_search(query)
    context = "\n\n".join(docs)

    history = get_chat_history(user_id)

    history_text = ""
    for q, r in reversed(history):
        history_text += f"User: {q}\nAssistant: {r}\n"

    prompt = f"""
You are an internal company assistant.

Conversation History:
{history_text}

Context:
{context}

Question:
{query}

Rules:
- Answer ONLY from context
- If not found, say "I don't know"
"""

    return stream_response(prompt)