import redis

r = redis.Redis(host="localhost", port=6379, db=3)

# example: 5K tokens per day per user
DAILY_LIMIT = 5000


def is_token_exceeded(user_id: str, tokens_used: int):
    key = f"tokens:{user_id}"

    current = r.get(key)
    current = int(current) if current else 0

    if current + tokens_used > DAILY_LIMIT:
        return True

    r.incrby(key, tokens_used)
    r.expire(key, 86400)  # 1 day

    return False