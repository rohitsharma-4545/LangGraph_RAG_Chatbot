from app.services.vector_store import hybrid_search_with_scores, rewrite_query_llm
from app.db.chat_history import get_chat_history
from app.services.llm_service import stream_response
from app.services.reranker import rerank

THRESHOLD = 0.45
MAX_ATTEMPTS = 3

def rag_answer_stream(query: str, user_id: str):
    final_docs = []

    for attempt in range(MAX_ATTEMPTS):
        print(f"[RAG] Attempt {attempt}")

        q = query if attempt == 0 else rewrite_query_llm(query)

        results = hybrid_search_with_scores(q)

        if not results:
            continue

        # filter by confidence
        filtered = [doc for doc, score in results if score >= THRESHOLD]

        # fallback if nothing passes threshold
        if not filtered:
            filtered = [doc for doc, _ in results]

        reranked_docs = rerank(q, filtered)

        final_docs = reranked_docs

        # ✅ early exit if good enough
        if len(final_docs) >= 2:
            break

    if not final_docs:
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