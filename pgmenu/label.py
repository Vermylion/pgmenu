import pygame
import pgmenu
from pgmenu.widget import Widget
from pgmenu.constants import THEME
from pgmenu.theme import resolve
from pgmenu.animation import *


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
                 center_x: bool = THEME,
                 center_y: bool = THEME,
                 **kwargs):

        # self.type has to be defined before super().__init__()
        self.type = pgmenu.LABEL

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
        self.center_x = resolve(center_x, pgmenu.Theme.label_center_x)
        self.center_y = resolve(center_y, pgmenu.Theme.label_center_y)

        # Add widget to widget list
        pgmenu.widget.add(self)

    def get_master(self):
        return self.master

    def get_text(self):
        return self.text

    def get_color(self):
        return self.color

    def get_font(self):
        return self.font

    def get_background(self):
        return self.background

    def get_antialias(self):
        return self.antialias

    def get_italic(self):
        return self.italic

    def get_bold(self):
        return self.bold

    def get_strikethrough(self):
        return self.strikethrough

    def get_underline(self):
        return self.underline

    def get_transparency(self):
        return self.transparency

    def get_center_x(self):
        return self.center_x

    def get_center_y(self):
        return self.center_y

    def draw(self):
        super().draw()

        self.surface = pgmenu.text.render(self.text, self.color, self.size, self.font, self.background, self.antialias, self.italic, self.bold, self.strikethrough, self.underline, self.transparency)

        if self.center_x or self.center_y:
            coords = pgmenu.position.center_coords(self.surface_size, (*self.coords, 0, 0), self.center_x, self.center_y)

        else:
            coords = self.coords

        self.master.blit(self.surface, coords)

    def resize(self, w, h):
        self.size = h