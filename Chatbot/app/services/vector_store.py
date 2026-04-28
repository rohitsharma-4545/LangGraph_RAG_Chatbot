from app.db.chroma_client import get_collection
from app.services.embedding_service import embed_texts
from app.services.embedding_service import embed_query
import uuid
from app.services.bm25_service import build_bm25, search_bm25

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

def hybrid_search(query: str, department="all", k: int = 4):
    collection = get_collection()
    
    query_embedding = embed_query(query)

    if collection.count() == 0:
     return []

    res = collection.query(
    query_embeddings=[query_embedding],
    n_results=k
    )

    results = res.get("documents", [[]])[0] if res else []

    results = [
    r for r in results
    if department == "all"
    ]

    bm25_results = search_bm25(query, k)

    combined = []

    seen = set()

    for doc in results + bm25_results:
        if doc not in seen:
            combined.append(doc)
            seen.add(doc)

    return combined[:k]

def clear_collection():
    collection = get_collection()

    try:
        ids = collection.get()["ids"]
        if ids:
            collection.delete(ids=ids)
    except Exception as e:
        print("Error clearing collection:", e)