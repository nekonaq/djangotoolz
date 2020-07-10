import random
import django.core.cache
from .logic import xor32


class Xor32Generator(object):
    def __init__(self, key=None, cache=None):
        self.key = key or self.__module__
        self.cache = cache or django.core.cache.cache

    @property
    def seed(self):
        try:
            return int(self.cache.get(self.key))
        except TypeError:
            return random.randint(1, 0x7fffffff)

    @seed.setter
    def seed(self, value):
        self.cache.set(self.key, value)

    def init_seed(self, value):
        """seed の値が未設定なら value にする
        """
        with self.cache.lock(f'{self.key}:lock'):
            if not self.seed:
                self.seed = value

    def get_next(self):
        with self.cache.lock(f'{self.key}:lock'):
            last = self.seed

            new = xor32(last)
            self.cache.set(self.key, new)
            return new


xor32_generator = Xor32Generator()
xor32_next = xor32_generator.get_next


"""
>>> from djangoexpack.utils.xorshift import xor32_next

>>> xor32_next()

>>> [xor32_next() for num in range(1, 10)]

>>> from djangoexpack.utils.xorshift.xor32 import xor32_generator
>>> xor32_generator.seed

"""
