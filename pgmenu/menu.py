import pygame
import pgmenu
from pgmenu.widget import Widget


class Menu(Widget):

    def __init__(self,
                 *widgets,
                 **kwargs):

        self.widgets = list(widgets)

        super().__init__(**kwargs)

    def modify(self,
               **kwargs):
        for args in kwargs:
            setattr(self, args, kwargs[args])

            for widget in self.widgets:
                setattr(widget, args, kwargs[args])

    def add(self,
            *widgets):
        self.widgets += widgets

    def remove(self,
               *widgets):
        for widget in widgets:
            if widget in self.widgets:
                self.widgets.remove(widget)

    def draw(self):
        pgmenu.lib._draw(*self.widgets)


# Automatically disables previous menu and activates current one
def show(menu):
    pgmenu.vars.current_menu_showed = menu


def draw():
    if isinstance(pgmenu.vars.current_menu_showed, Menu):
        pgmenu.vars.current_menu_showed.draw()
