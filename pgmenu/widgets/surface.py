import pygame
import pgmenu

from pgmenu.base import Widget
from pgmenu.core.animation import AnimateTuple, AnimateSurface
from pgmenu.core.theme import resolve
from pgmenu.vars.constants import THEME


__all__ = ["Surface"]


# Surface as a widget
class Surface(Widget):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 surface: pygame.Surface | AnimateSurface,
                 coords: list | tuple | AnimateTuple = THEME,
                 **kwargs):

        self.set_type(pgmenu.SURFACE)

        super().__init__(**kwargs)

        self.master = master
        self.surface = surface
        self.coords = resolve(coords, pgmenu.Theme.surface_coords)

        self.size = self.surface.get_size()

        # Shadow attribute to resize surface
        self._surface = surface

        pgmenu.widgets.add(self)

    def __setattr__(self, key, value):

        super().__setattr__(key, value)

        if key == "surface":
            self._surface = value

    def draw(self):
        super().draw()

        self.blit_to_master()

    def resize(self, w: int, h: int):
        self.size = w, h

        original_surface = self._surface

        self.surface = pgmenu.cache.cached_smoothscale(self._surface, self.size)

        self._surface = original_surface

    def update(self, event):
        super().update(event)

        self.size = self.surface.get_size()
