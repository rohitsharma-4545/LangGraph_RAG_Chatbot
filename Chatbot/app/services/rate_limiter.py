import time
import redis

r = redis.Redis(host="localhost", port=6379, db=2)

# max 5 requests per minute
RATE_LIMIT = 5
WINDOW = 60  # seconds


def is_rate_limited(user_id: str):
    key = f"rate:{user_id}"

    current = r.get(key)

    if current and int(current) >= RATE_LIMIT:
        return True

    pipe = r.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, WINDOW)
    pipe.execute()

    return False