from rank_bm25 import BM25Okapi

# in-memory store (for now)
bm25 = None
documents = []

def build_bm25(texts: list[str]):
    global bm25, documents

    documents = texts
    tokenized = [doc.split(" ") for doc in texts]

    bm25 = BM25Okapi(tokenized)


def search_bm25(query: str, k: int = 4):
    if bm25 is None:
        return []

    tokenized_query = query.split(" ")
    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked[:k]]