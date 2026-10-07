import pygame
from pygame import Color

import pgmenu
from collections import OrderedDict

__all__ = ["Cache", "lru_get", "lru_set", "clear_cache", "cached_smoothscale", "cached_surface"]


# Class to handle AnimateType objects and handle them as frozen objects in cache
class Cache(OrderedDict):

    def _normalize(self, key):
        if not isinstance(key, tuple):
            return key  # optional: depends on your usage

        animate_type = pgmenu.core.animation.AnimateType
        return tuple(k.value if isinstance(k, animate_type) else k for k in key)

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

    if len(cache) > pgmenu.system.MAX_CACHE_SIZE:
        cache.popitem(last=False)  # remove least recently used


def clear_cache():
    for cache_dict in pgmenu.vars.cache.values():
        cache_dict.clear()


def cached_smoothscale(surface: pygame.Surface,
                       size: tuple[int, int]):
    """Resizes surface with pygame.transform.smoothscale and caches result"""
    cache_id = (surface, size)

    cache_surface = pgmenu.cache.lru_get(pgmenu.vars.cache["surface"], cache_id)

    if cache_surface is None:
        cache_surface = pygame.transform.smoothscale(surface, size)

        pgmenu.cache.lru_set(pgmenu.vars.cache["surface"], cache_id, cache_surface)

    return cache_surface.copy()


def cached_surface(size: list[int, int] | tuple[int, int],
                   flags: int = 0,
                   depth: int | None = None,
                   masks: Color | list[int, int] | tuple[int, int] | str | int | None = None) -> pygame.Surface:
    """Creates a pygame Surface and caches the result"""

    cache_id = (size, flags, depth, masks)

    surface = pgmenu.cache.lru_get(pgmenu.vars.cache["surface"], cache_id)

    if surface is None:
        args = [size]

        if flags or depth is not None or masks is not None:
            args.append(flags)
        if depth is not None or masks is not None:
            args.append(depth)
        if masks is not None:
            args.append(masks)

        surface = pygame.Surface(*args)

        pgmenu.cache.lru_set(pgmenu.vars.cache["surface"], cache_id, surface)

    return surface.copy()
