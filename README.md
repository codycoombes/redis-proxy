# redis-proxy
## About
Redis proxy is an LRU caching layer to a single Redis backed service instance powered by Flask.

### Features
* Users can interface to the Redis proxy through HTTP, with the
Redis “GET” command mapped to the HTTP “GET” method.
* Key values retrieved from "GET" requests are cached to Redis proxy using LRU algorithm.

## Architecture overview
### Flask web server
* Handles GET requests for value of specified keys at the `GET /:key` endpoint.
* Concurrent requests are handled through multithreading.
* Configurable through `.flaskev`:
  * `FLASK_RUN_HOST=0.0.0.0`
  * `FLASK_RUN_PORT=5000`
  * `FLASK_DEBUG=True`
  * `FLASK_ENV=development`
### Cached GET
* A GET request, directed at the proxy, returns the value of the specified key from the proxy’s local cache if the local cache
  contains a value for that key. If the local cache does not contain a value for the specified key, it fetches the value from the
  backing Redis instance, using the Redis GET command, and stores it in the local cache, associated with the specified key.
* Once the cache fills to capacity, the least recently used (LRU) key is evicted each time a new key needs to be added to the cache.
* Configurable through the environment variables `CAPACITY` and `GLOBAL_EXPIRY`.
### Redis
* Each instance of the proxy service is associated with a single Redis service instance. 
* The address of the backing Redis is configured at proxy startup
  through environment variables `REDIS_HOST` and `REDIS_PORT`.
### Black-box testing
* proxy-test is used for automated end-to-end testing and treats the proxy as a black-box to which an HTTP client connects and
makes requests. This is configurable through the environment variables but requires a specific configuration to pass tests. 

## How to use
This project requires `make`, `docker`, and `docker-compose`. 

To build and run the proxy, redis, and test containers: 
```
$ make test
```

Output for tests will look like:
```
proxy-test_1  | ......
proxy-test_1  | ----------------------------------------------------------------------
proxy-test_1  | Ran 6 tests in 5.218s
proxy-test_1  | 
proxy-test_1  | OK
redis-proxy_proxy-test_1 exited with code 0
```

Press CRTL C to exit and stop all containers 

To build only the proxy and redis containers: 
```
$ make build
$ make run
# To stop the containers
$ make stop
```

## Concurrency
Flask supports concurrent requests through multithreading by default. \
lru-expiring-cache (https://pypi.org/project/lru-expiring-cache/) is thread-safe by setting `concurrent=True` when
creating a new instance.

## Complexity
lru-expiring-cache has O(n) get and O(1) set \
I went with this library because it was thread-safe but if I had more time I would have gone with a cache library that had O(1) retrieval like cachetools (https://cachetools.readthedocs.io/en/latest/) and manually synchronize access to the methods or implement my own LRU cache using a dictionary (hashmap). 

## Time spent
Total time: 5.5 hr
* Research and understand redis -> 1 hr
* Decide on framework -> 0.25 hr
* Look into Python LRU cache libraries -> 0.5 hr
* Setup Flask project -> 0.5 hr
* Write LRU cache class -> 0.25 hr
* Write http get logic -> 0.5 hr
* Write tests for proxy-test -> 1 hr
* Setup docker files -> 0.5 hr
* Learn make and setup make file -> 0.5 hr
* Write up documentation in readme -> 0.5 hr

## Bonus
Due to time constraint, the maximum number of clients that can be concurrently served by the proxy is not currently configurable nor verified by test cases.
