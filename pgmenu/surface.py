import pygame
from pygame import Color

import pgmenu
from pgmenu.vars import cache
from pgmenu.widget import Widget
from pgmenu.constants import THEME
from pgmenu.theme import resolve
from pgmenu.animation import *

from typing import Callable


# Surface as a widget
class Surface(Widget):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 surface: pygame.Surface | AnimateSurface,
                 coords: list | tuple | AnimateTuple = THEME,
                 **kwargs):

        self.type = pgmenu.SURFACE

        super().__init__(**kwargs)

        self.master = master
        self.surface = surface
        self.coords = resolve(coords, pgmenu.Theme.surface_coords)

        self.size = self.surface.get_size()

        # Shadow attribute to resize surface
        self._surface = surface

        pgmenu.widget.add(self)

    def get_master(self):
        return self.master

    def __setattr__(self, key, value):

        super().__setattr__(key, value)

        if key == "surface":
            self._surface = value

    def draw(self):
        super().draw()

        self.master.blit(self.surface, self.coords)

    def resize(self, w, h):
        self.size = w, h

        original_surface = self._surface

        self.surface = cached_smoothscale(self._surface, self.size)

        self._surface = original_surface

    def update(self, event):
        super().update(event)

        self.size = self.surface.get_size()


def cached_smoothscale(surface: pygame.Surface | AnimateSurface,
                       size: tuple[int, int] | AnimateTuple):
    """Resizes surface with pygame.transform.smoothscale and caches result"""
    cache_id = (surface, size)

    cache_surface = pgmenu.cache.lru_get(cache["surface"], cache_id)

    if cache_surface is None:
        cache_surface = pygame.transform.smoothscale(surface, size)

        pgmenu.cache.lru_set(cache["surface"], cache_id, cache_surface)

    return cache_surface.copy()


def cached_surface(size: list[int, int] | tuple[int, int],
                   flags: int = 0,
                   depth: int | None = None,
                   masks: Color | list[int, int] | tuple[int, int] | str | int | None = None) -> pygame.Surface:
    """Creates a pygame Surface and caches the result"""

    cache_id = (size, flags, depth, masks)

    surface = pgmenu.cache.lru_get(cache["surface"], cache_id)

    if surface is None:
        args = [size]

        if flags or depth is not None or masks is not None:
            args.append(flags)
        if depth is not None or masks is not None:
            args.append(depth)
        if masks is not None:
            args.append(masks)

        surface = pygame.Surface(*args)

        pgmenu.cache.lru_set(cache["surface"], cache_id, surface)

    return surface.copy()