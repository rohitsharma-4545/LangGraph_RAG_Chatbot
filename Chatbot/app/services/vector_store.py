from app.db.chroma_client import get_collection
from app.services.embedding_service import embed_texts
from app.services.embedding_service import embed_query
import uuid
from app.services.bm25_service import build_bm25, search_bm25
from app.services.llm_service import generate_response

def add_documents(chunks):
    collection = get_collection()   

    texts = [doc.page_content for doc in chunks]

    build_bm25(texts)

    metadatas = [
        {"source": "company_doc", "department": "all"}
        for _ in texts
    ]

    embeddings = embed_texts(texts)

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=[str(uuid.uuid4()) for _ in texts]
    )

def hybrid_search_with_scores(query: str, department="all", k: int = 4):
    collection = get_collection()
    
    if collection.count() == 0:
        return []

    query_embedding = embed_query(query)

    res = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    docs = res.get("documents", [[]])[0]
    distances = res.get("distances", [[]])[0]

    # normalize vector scores
    scored_docs = [
        (doc, 1 - dist) for doc, dist in zip(docs, distances)
    ]

    bm25_docs = search_bm25(query, k)
    bm25_scored = [(doc, 0.5) for doc in bm25_docs]

    # weighted merge
    scores = {}

    for doc, s in scored_docs:
        scores[doc] = scores.get(doc, 0) + (0.5 * s)

    for doc, s in bm25_scored:
        scores[doc] = scores.get(doc, 0) + (0.3 * s)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return ranked[:k]

def clear_collection():
    collection = get_collection()

    try:
        ids = collection.get()["ids"]
        if ids:
            collection.delete(ids=ids)
    except Exception as e:
        print("Error clearing collection:", e)

def rewrite_query_llm(query: str):
    prompt = f"""
Rewrite the following query to improve retrieval quality.
Keep meaning same. Be concise.

Query: {query}
Rewritten:
"""
    return generate_response(prompt).strip()