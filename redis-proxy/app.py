import redis
import os
from flask import Flask, abort
from cache import *


app = Flask(__name__)
lru_cache = Cache(int(os.getenv('CAPACITY')), int(os.getenv('GLOBAL_EXPIRY')))
POOL = redis.ConnectionPool(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0)


@app.get("/<key>")
def get(key):
    if lru_cache.contains_key(key):
        return lru_cache.get_value(key)
    else:
        try:
            conn = redis.Redis(connection_pool=POOL)
        except:
            abort(500)
        if not conn.__contains__(key):
            abort(404)
        else:
            value = conn.get(key)
            lru_cache.add(key, value)
            return value
