import os
import redis
import requests
import unittest
import time


class MyTestCase(unittest.TestCase):

    POOL = redis.ConnectionPool(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0)
    conn = redis.Redis(connection_pool=POOL)

    def test_redis_connection(self):
        self.conn.set("key1", "value1")
        self.assertEqual("value1", self.conn.get("key1").decode('UTF-8'))

    def test_get_from_redis(self):
        self.conn.set("key2", "value2")
        r = requests.get('http://proxy:5000/key2')
        self.assertEqual(r.text, self.conn.get("key2").decode('UTF-8'))

    def test_get_from_cache(self):
        # Manually set new value for key in redis
        self.conn.set("key3", "old-value")
        # Call get request to load key value into cache
        requests.get('http://proxy:5000/key3')
        # Update value for key in redis
        self.conn.set("key3", "new-value")
        # Check that value is from cache instead of redis
        r = requests.get('http://proxy:5000/key3')
        self.assertEqual(r.text, "old-value")

    def test_unknown_key_return_404(self):
        r = requests.get('http://proxy:5000/key4')
        self.assertEqual(r.status_code, 404)

    def test_expired_cache_read_from_redis(self):
        self.conn.set("key5", "old-value")
        # Call get request to load key value into cache
        requests.get('http://proxy:5000/key5')
        # Wait until cache expires
        time.sleep(int(os.getenv('GLOBAL_EXPIRY')))
        # Check that value is from redis since cache expired
        self.conn.set("key5", "new-value")
        r = requests.get('http://proxy:5000/key5')
        self.assertEqual(r.text, "new-value")

    def test_lru_eviction_cache(self):
        # Insert test data into redis
        self.conn.set("key6", "value6")
        self.conn.set("key7", "value7")
        self.conn.set("key8", "value8")
        self.conn.set("key9", "value9")
        self.conn.set("key10", "value10")

        # Load test data into cache to fill capacity
        requests.get('http://proxy:5000/key6')
        requests.get('http://proxy:5000/key7')
        requests.get('http://proxy:5000/key8')
        requests.get('http://proxy:5000/key9')

        # New request replace LRU key-value pair from cache
        requests.get('http://proxy:5000/key10')

        # Update evicted key-value pair and check that new request reads from redis
        self.conn.set("key6", "new-value6")
        r = requests.get('http://proxy:5000/key6')
        self.assertEqual(r.text, "new-value6")


if __name__ == '__main__':
    unittest.main()