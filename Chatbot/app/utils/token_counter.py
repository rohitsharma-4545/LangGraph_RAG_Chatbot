def estimate_tokens(text: str):
    # rough estimate: 1 token ≈ 4 chars
    return len(text) // 4