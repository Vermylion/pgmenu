import pygame
import pgmenu
from pgmenu import widget
from pgmenu.widget import Widget, ToggleWidget
from pgmenu.constants import THEME
from pgmenu.theme import resolve, resolve_kwarg
from pgmenu.animation import *


class Radiobutton(ToggleWidget):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 coords: list | tuple | AnimateTuple = THEME,
                 size: int | list | tuple | Animate | AnimateTuple = THEME,
                 fill: tuple[int, int, int] | AnimateTuple | pygame.Surface | AnimateSurface = THEME,
                 text: str | None = THEME,
                 text_color: tuple[int, int, int] | AnimateTuple = THEME,
                 dot_fill: tuple[int, int, int] | AnimateTuple = THEME,
                 margin: int | Animate = THEME,
                 width: int | Animate = THEME,
                 border_radius: int | Animate = THEME,
                 selected: bool = THEME,
                 **kwargs):

        self.set_type(pgmenu.RADIOBUTTON)

        self._set_indicator("dot_")
        self._set_on_attr("selected")

        super().__init__(**kwargs)

        self.master = master
        self.coords = resolve(coords, pgmenu.Theme.radiobutton_coords)
        self.size = self._format_size(size)
        self.fill = resolve(fill, pgmenu.Theme.radiobutton_fill)

        self.text = resolve(text, pgmenu.Theme.radiobutton_text)
        self.text_color = resolve(text_color, pgmenu.Theme.radiobutton_text_color)
        self.dot_fill = resolve(dot_fill, pgmenu.Theme.radiobutton_dot_fill)
        self.margin = resolve(margin, pgmenu.Theme.radiobutton_margin)

        self.width = resolve(width, pgmenu.Theme.radiobutton_width)
        self.border_radius = resolve(border_radius, pgmenu.Theme.radiobutton_border_radius, round(min(self.size) / 3.3))

        self.selected = resolve(selected, pgmenu.Theme.radiobutton_selected)
        self.group = None

        # Kwargs attributes
        self.text_side = resolve_kwarg(kwargs, "text_side", pgmenu.Theme.radiobutton_text_side)
        self.text_margin = resolve_kwarg(kwargs, "text_margin", pgmenu.Theme.radiobutton_text_margin)
        self.text_side_margin = resolve_kwarg(kwargs, "text_side_margin", pgmenu.Theme.radiobutton_text_side_margin, self.margin.base_value)
        # Dot (Inner indicator) (rect) kwargs attributes
        self._init_rect(kwargs, "dot_")
        self.dot_border_radius = resolve_kwarg(kwargs, "dot_border_radius", pgmenu.Theme.radiobutton_dot_border_radius, self.border_radius.base_value - self.margin.base_value)

        self.dot_base_transparency = resolve_kwarg(kwargs, "dot_base_transparency", pgmenu.Theme.radiobutton_dot_base_transparency)
        # Setting base custom animation
        if not isinstance(kwargs.get("dot_transparency"), AnimateType):
            self.dot_transparency = pgmenu.animation.Animate(self.dot_base_transparency, self.dot_transparency, self.animation_duration, self.animation_curve, self.animation_precision)

        pgmenu.widget.add(self)
        
    def select(self):
        self.selected = True
        self.on_select()
        # FIXME -> animation_on_select or _on_deselect might not have self.dot_transparency for done check
        pgmenu.animation.run_callable(self.animation_on_select, done=lambda: self.dot_transparency.done)

        if self.group:
            self.group.select(self)
        
    def deselect(self):
        self.selected = False
        self.on_deselect()
        # FIXME -> animation_on_select or _on_deselect might not have self.dot_transparency for done check
        pgmenu.animation.run_callable(self.animation_on_deselect, done=lambda: self.dot_transparency.done)

        if self.group:
            self.group.deselect(self)

    def toggle(self):
        self.select() if not self.selected else self.deselect()

    def set_group(self, group):
        self.group = group

    def remove_group(self):
        self.group = None


class RadioGroup:

    def __init__(self, *widgets: Radiobutton,):
        self.widgets = []
        self.add(*widgets)

        self.selected_widget = None

    def add(self, *widgets: Radiobutton,):
        for widget in widgets:
            if isinstance(widget, Radiobutton):
                self.widgets.append(widget)
                widget.set_group(self)

    def remove(self, *widgets: Radiobutton,):
        for widget in widgets:
            if widget in self.widgets:
                self.widgets.remove(widget)

    def select(self, widget: Radiobutton):
        if not widget in self.widgets:
            return

        if self.selected_widget is None:
            self.selected_widget = widget

        else:
            self.selected_widget.deselect()

        self.selected_widget = widget

    def deselect(self, widget: Radiobutton):
        if widget == self.selected_widget:
            self.selected_widget = None

    def get_selected(self):
        return self.selected_widget