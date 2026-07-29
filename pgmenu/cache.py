import pgmenu
import pygame
from collections import OrderedDict


# Class to handle AnimateType objects and handle them as frozen objects in cache
class Cache(OrderedDict):

    def _normalize(self, key):
        if not isinstance(key, tuple):
            return key  # optional: depends on your usage

        return tuple(k.value if isinstance(k, pgmenu.animation.AnimateType) else k for k in key)

    def __setitem__(self, key, value):
        return super().__setitem__(self._normalize(key), value)

    def __getitem__(self, key):
        return super().__getitem__(self._normalize(key))

    def __contains__(self, key):
        return super().__contains__(self._normalize(key))

    def get(self, key, default=None):
        return super().get(self._normalize(key), default)

    def move_to_end(self, key, last = True):
        return super().move_to_end(self._normalize(key), last)


def lru_get(cache, key):
    if key in cache:
        cache.move_to_end(key)  # mark as recently used
        return cache[key]

    return None


def lru_set(cache, key, value):
    if key in cache:
        cache.move_to_end(key)
    cache[key] = value

    if len(cache) > pgmenu.system.max_cache_size:
        cache.popitem(last=False)  # remove least recently used


def clear_cache():
    for cache_var in pgmenu.vars.cache:
        getattr(pgmenu.vars, cache_var).clear()