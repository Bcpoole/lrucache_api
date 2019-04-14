import collections

from flask import Flask, Response, abort, jsonify, request

app = Flask(__name__)
app.run(host='0.0.0.0', port=80)


class LRUCache:
    def __init__(self, capacity):
        """
        Cache that evicts members based on when last used.

        :param capacity: Capacity of the LRU cache
        """
        # self._cache = dict()
        self._cache = collections.OrderedDict()

        if type(capacity) is not int:
            raise TypeError(f"Invalid capacity type {type(capacity)}, must be an integer!")
        elif capacity < 1:
            raise ValueError(f"Cache capacity {capacity} too small, must be at least 1!")

        self.capacity = capacity

    def get(self, key):
        """
        Get key's value from cache and bump usage key in cache.

        :param key: key in cache
        :return: Cache key's value. If key not in cache returns None.
        """
        if key in self._cache:
            value = self._cache[key]
            self._cache.move_to_end(key, last=False)
            return value
        else:
            return None

    def put(self, key, value):
        """
        Set key in cache to value and bump usage. If cache at capacity and adding a new key, evict LRU key.

        :param key: key in cache
        :param value: positive int value for key
        """
        if type(value) is not int:
            raise TypeError(f"Invalid value type {type(value)}, must be an integer!")
        elif value < 0:
            raise ValueError(f"value {value} must positive!")
        if key not in self._cache and len(self._cache) == self.capacity:  # evict LRU key
            self._cache.popitem()
        self._cache[key] = value
        self._cache.move_to_end(key, last=False)


cache = LRUCache(2)


@app.route("/api/v1/get/<key>", methods=['GET'])
def cache_get(key):
    """
    GET request for key in cache.

    :param key: key in cache
    :return: JSON of key, value if exists in cache, else 404.
    """
    value = cache.get(key)
    if value is None:
        abort(404)
    else:
        return jsonify({'key': key, 'value': value})


@app.route("/api/v1/put/<key>", methods=['PUT'])
def cache_put(key):
    """
    PUT request for adding/updating key in cache. Supply -d value={POSITIVE_INT}

    :param key: key in cache
    :return: 200 status if successful and empty response, else
    """
    try:
        value = int(request.args.get('value'))
        cache.put(key, value)
        return Response(status=200)
    except TypeError:
        abort(400, "Arg `value` must be supplied!")
    except ValueError:
        abort(400, "Arg `value` must be a positive integer!")
