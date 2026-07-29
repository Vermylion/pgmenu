import pygame
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

        self.surface = resize(self._surface, self.size)

        self._surface = original_surface

    def update(self, event):
        super().update(event)

        self.size = self.surface.get_size()


# FIXME -> Is this really necessary?
def resize(surface: pygame.Surface | AnimateSurface,
           size: tuple[int, int] | AnimateTuple):
    """resizes surface with pygame.transform.smoothscale and caches result"""
    cache_id = (surface, size)

    if pgmenu.cache.lru_get(cache["surface"], cache_id) is None:
        surface = pygame.transform.smoothscale(surface, size)

        pgmenu.cache.lru_set(cache["surface"], cache_id, surface)

    return pgmenu.cache.lru_get(cache["surface"], cache_id)
