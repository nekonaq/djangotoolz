from django.core.cache import caches


class RedisStore(object):
    cache_name_default = 'default'

    @property
    def cache_key_template(self):
        raise NotImplementedError(
            "property must be defined: {}.cache_key_template".format(self.__class__.__name__)
        )

    def __init__(self, cache_name=None):
        self.cache_name = cache_name or self.cache_name_default

    @property
    def client(self):
        return caches[self.cache_name]

    @property
    def redis_client(self):
        return caches[self.cache_name].client.get_client()

    def make_key(self, key, template=None, kwargs={}):
        return (template or self.cache_key_template).format(key, **kwargs)

    def make_redis_key(self, key, template=None, kwargs={}):
        return self.client.make_key(self.make_key(key, template=template, kwargs=kwargs))

    def value_as_python(self, value):
        return value

    def get(self, key):
        return self.value_as_python(self.client.get(self.make_key(key)))

    def set(self, key, value, timeout=None):
        self.client.set(self.make_key(key), value, timeout=timeout)

    def delete(self, key, **kwargs):
        self.client.delete(self.make_key(key))

    def raw_value_as_python(self, value):
        return value

    def raw_get(self, key):
        return self.raw_value_as_python(self.redis_client.get(self.make_redis_key(key)))

    def raw_set(self, key, value):
        return self.redis_client.set(self.make_redis_key(key), value)

    def raw_delete(self, key):
        return self.redis_client.delete(self.make_redis_key(key))

    def raw_encode(self, value):
        return self.client.client.encode(value)

    def raw_decode(self, value):
        return self.client.client.decode(value)


'''
#-------------------------------------------------------
>>> from djangoexpack.utils.redis import RedisStore
>>> rc = RedisStore()
>>> rc.get('foomix')

>>> rc.set('foomix', 'destrix')
>>> rc.get('foomix')
'destrix'

>>> rc.set('foomix', 23)
>>> rc.get('foomix')
23

>>> rc.set('foomix', dict(a=23, b='nak'))
>>> rc.get('foomix')
{'a': 23, 'b': 'nak'}

>>> rc.make_key('foomix')
'redis.foomix'

#-------------------------------------------------------
>>> rc.make_redis_key('foomix')
':1:redis.foomix'

>>> rc.raw_get('foomix')
b'\x80\x04\x95\x15\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x01a\x94K\x17\x8c\x01b\x94\x8c\x03nak\x94u.'

>>> rc.raw_decode(rc.raw_get('foomix'))
{'a': 23, 'b': 'nak'}

>>> rc.raw_set('foomix', 'valllue')
b'valllue'

>>> rc.raw_delete('foomix')
1
>>> rc.raw_get('foomix')

>>> rc.raw_set('foomix', dict())
Traceback (most recent call last):
...
redis.exceptions.DataError: Invalid input of type: 'dict'. Convert to a byte, string or number first.

#-------------------------------------------------------
>>> rr = rc.redis_client
>>> rr
Redis<ConnectionPool<Connection<host=localhost,port=6379,db=0>>>

>>> rr.get('foomix')

>>> rr.set('foomix', 'destrix')
True
>>> rr.get('foomix')
b'destrix'

>>> rr.set('foomix', 23)
True
>>> rr.get('foomix')
b'23'

>>> rr.set('foomix', dict(a=23, b='nak'))
Traceback (most recent call last):
...
redis.exceptions.DataError: Invalid input of type: 'dict'. Convert to a byte, string or number first.

'''
