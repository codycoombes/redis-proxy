from lru import LruCache


class Cache:
    def __init__(self, size, expiry):
        self.size = size
        self.expiry = expiry
        self.cache = LruCache(maxsize=self.size, expires=self.expiry, concurrent=True)

    def get_value(self, key):
        return self.cache.get(key)

    def contains_key(self, key):
        return self.cache.__contains__(key)

    def add(self, key, value):
        self.cache.add(key, value)

    def clear_cache(self):
        self.cache.clear()

