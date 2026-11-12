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
        self.coords = resolve(coords, "coords", self.type)
        self.text = resolve(text, "text", self.type)
        self.color = resolve(color, "color", self.type)
        self.font = resolve(font, "font", self.type)
        self.background = resolve(background, "background", self.type)
        self.size = resolve(size, "size", self.type)
        self.antialias = resolve(antialias, "antialias", self.type)
        self.italic = resolve(italic, "italic", self.type)
        self.bold = resolve(bold, "bold", self.type)
        self.strikethrough = resolve(strikethrough, "strikethrough", self.type)
        self.underline = resolve(underline, "underline", self.type)
        self.transparency = resolve(transparency, "transparency", self.type)

        # Add widget to widget list
        pgmenu.widgets.add(self)

    def draw(self):
        super().draw()

        self.surface = pgmenu.text.render(self.text, self.color, self.size, self.font, self.background, self.antialias, self.italic, self.bold, self.strikethrough, self.underline, self.transparency)

        self.blit_to_master()

    def resize(self, w: int, h: int):
        self.size = h