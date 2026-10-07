import pygame
import pgmenu

from pgmenu.base import Widget, RectMixin
from pgmenu.core.animation import Animate, AnimateTuple, AnimateSurface
from pgmenu.core.theme import resolve
from pgmenu.vars.constants import THEME


__all__ = ["Frame"]


class Frame(Widget, RectMixin):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 coords: list | tuple | AnimateTuple = THEME,
                 size: list | tuple | AnimateTuple = THEME,
                 fill: tuple[int, int, int] | pygame.Surface | AnimateSurface = THEME,
                 width: int | Animate = THEME,
                 border_radius: int | Animate = THEME,
                 **kwargs):

        self.set_type(pgmenu.FRAME)

        super().__init__(**kwargs)

        self.master = master
        self.coords = resolve(coords, pgmenu.Theme.frame_coords)
        self.size = resolve(size, pgmenu.Theme.frame_size)

        self.fill = resolve(fill, pgmenu.Theme.frame_fill)
        self.width = resolve(width, pgmenu.Theme.frame_width)

        self.border_radius = resolve(border_radius, pgmenu.Theme.frame_border_radius, round(min(self.size) / 7))

        self.widgets = []
        self._widgets_to_blit = {}

        pgmenu.widgets.add(self)

    def add(self, *widgets):
        self.widgets += widgets

    def remove(self,
               *widgets):
        for widget in widgets:
            if widget in self.widgets:
                self.widgets.remove(widget)

    def blit(self, surface, coords):
        self._widgets_to_blit[surface] = coords

    def draw(self):
        super().draw()

        self.surface = pgmenu.draw.aarect(None, self.fill, (0, 0, *self.size.int_tuple), self.width, self.border_radius,
                                        self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius,
                                        self.antialiasing, self.transparency, self.aa_strength, inner_fill=self.inner_fill,
                                        inner_transparency=self.inner_transparency, inner_aa_strength=self.inner_aa_strength, inner_antialiasing=self.inner_antialiasing)

        self.draw_widgets()

        self.master.blit(self.surface, self.coords)

    def draw_widgets(self):
        for surface, coords in self._widgets_to_blit.items():
            self.surface.blit(surface, coords)

        self._widgets_to_blit.clear()

    def resize(self, w, h):
        self._resize_border_radii(w, h)

        self.size = w, h