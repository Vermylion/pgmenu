import pgmenu


class Menu:

    def __init__(self,
                 *widgets):

        self.widgets = list(widgets)

        super().__init__()

    def get_widgets(self):
        return self.widgets

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


def show(menu):
    pgmenu.vars.current_menu_showed = menu


def draw():
    if isinstance(pgmenu.vars.current_menu_showed, Menu):
        pgmenu.vars.current_menu_showed.draw()
