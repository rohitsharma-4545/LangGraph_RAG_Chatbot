import redis

r = redis.Redis(host="localhost", port=6379, db=1)

def get_cache(key):
    val = r.get(key)
    return val.decode() if val else None

def set_cache(key, value):
    r.setex(key, 3600, value)