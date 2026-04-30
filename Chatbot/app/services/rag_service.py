from app.services.vector_store import hybrid_search_with_scores, rewrite_query_llm
from app.db.chat_history import get_chat_history
from app.services.llm_service import stream_response
from app.services.reranker import rerank

THRESHOLD = 0.45
MAX_ATTEMPTS = 3

final_docs = []

def rag_answer_stream(query: str, user_id: str):
    for attempt in range(MAX_ATTEMPTS):
        print(attempt, " rewriting")
        if attempt > 0:
            q = rewrite_query_llm(query)
        else:
            q = query

        results = hybrid_search_with_scores(q)

        docs = [doc for doc, _ in results]

        reranked_docs = rerank(q, docs)

        final_docs = reranked_docs

    if len(final_docs) < 2:
        return iter(["I don't know\n"])

    context = "\n\n".join(final_docs)

    history = get_chat_history(user_id)

    history_text = ""
    for q, r in reversed(history):
        history_text += f"User: {q}\nAssistant: {r}\n"

    prompt = f"""
You are a strict company assistant.

Use ONLY the given context.

If answer is not clearly present, say:
"I don't know based on the provided document."

Conversation History:
{history_text}

Context:
{context}

Question:
{query}

"""

    return stream_response(prompt)