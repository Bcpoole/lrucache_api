import json

import pytest

from lrucache_api.cache_service import LRUCache, app

app.testing = True


class TestLRUCache(object):
    @pytest.fixture()
    def cache(self):
        cache = LRUCache(2)
        cache.put(1, 100)
        cache.put(2, 20)
        return cache

    def test__init__(self):
        with pytest.raises(TypeError):
            LRUCache('bad_input')
        with pytest.raises(ValueError):
            LRUCache(0)
        assert LRUCache(1)

    def test_get(self, cache):
        assert cache.get(3) is None
        assert cache.get(2) == 20

    def test_put(self, cache):
        with pytest.raises(TypeError):
            cache.put(1, 'bad_input')
        with pytest.raises(ValueError):
            cache.put(1, -1)

        assert cache.get(3) is None
        cache.put(3, 35)
        assert cache.get(3) is 35
        assert cache.get(1) is None


class TestCacheService(object):
    def test_cache_get(self):
        with app.test_client() as client:
            get_request = '/api/v1/get/3'
            res = client.get(get_request)
            assert res.status_code == 404

            client.put('/api/v1/put/3', query_string={'value': 35})

            res = client.get(get_request)
            assert res.status_code == 200 and json.loads(res.data) == {'key': '3', 'value': 35}

    def test_cache_put(self):
        with app.test_client() as client:
            res = client.put('/api/v1/put/2', query_string={'value': 200})
            assert res.data == b''
            # check update
            res = client.put('/api/v1/put/2', query_string={'value': 250})
            assert res.data == b''

            assert client.put('/api/v1/put/3').status_code == 400
            assert client.put('/api/v1/put/3', query_string={'value': '35~'}).status_code == 400
