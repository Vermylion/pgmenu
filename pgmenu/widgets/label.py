import pygame
import pgmenu

from pgmenu.base import Widget
from pgmenu.core.animation import Animate, AnimateTuple
from pgmenu.core.theme import resolve
from pgmenu.vars.constants import THEME


__all__ = ["Label"]


# Need Widget for default functions
class Label(Widget):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 coords: list | tuple | AnimateTuple = THEME,
                 text: str = THEME,
                 color: list | tuple | AnimateTuple = THEME,
                 size: int | Animate = THEME,
                 font: str = THEME,
                 background: list | tuple | AnimateTuple = THEME,
                 antialias: bool = THEME,
                 italic: bool = THEME,
                 bold: bool = THEME,
                 strikethrough: bool = THEME,
                 underline: bool = THEME,
                 transparency: int | Animate = THEME,
                 **kwargs):

        # self.type has to be defined before super().__init__()
        self.set_type(pgmenu.LABEL)

        super().__init__(**kwargs)

        self.master = master
        self.coords = resolve(coords, pgmenu.Theme.label_coords)
        self.text = resolve(text, pgmenu.Theme.label_text)
        self.color = resolve(color, pgmenu.Theme.label_color)
        self.font = resolve(font, pgmenu.Theme.label_font)
        self.background = resolve(background, pgmenu.Theme.label_background)
        self.size = resolve(size, pgmenu.Theme.label_size)
        self.antialias = resolve(antialias, pgmenu.Theme.label_antialias)
        self.italic = resolve(italic, pgmenu.Theme.label_italic)
        self.bold = resolve(bold, pgmenu.Theme.label_bold)
        self.strikethrough = resolve(strikethrough, pgmenu.Theme.label_strikethrough)
        self.underline = resolve(underline, pgmenu.Theme.label_underline)
        self.transparency = resolve(transparency, pgmenu.Theme.label_transparency)

        # Add widget to widget list
        pgmenu.widgets.add(self)

    def draw(self):
        super().draw()

        self.surface = pgmenu.text.render(self.text, self.color, self.size, self.font, self.background, self.antialias, self.italic, self.bold, self.strikethrough, self.underline, self.transparency)

        self.blit_to_master()

    def resize(self, w: int, h: int):
        self.size = h