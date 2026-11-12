import pygame
import pgmenu

from pgmenu.base import Widget, ToggleWidget
from pgmenu.core.animation import Animate, AnimateTuple, AnimateSurface, AnimateType
from pgmenu.core.theme import resolve, resolve_kwarg
from pgmenu.vars.constants import THEME


__all__ = ["Checkbox"]


class Checkbox(ToggleWidget):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 coords: list | tuple | AnimateTuple = THEME,
                 size: int | list | tuple | Animate | AnimateTuple = THEME,
                 fill: tuple[int, int, int] | AnimateTuple | pygame.Surface | AnimateSurface = THEME,
                 text: str | None = THEME,
                 text_color: tuple[int, int, int] | AnimateTuple = THEME,
                 check_fill: tuple[int, int, int] | AnimateTuple = THEME,
                 margin: int | Animate = THEME,
                 width: int | Animate = THEME,
                 border_radius: int | Animate = THEME,
                 checked: bool = THEME,
                 **kwargs):

        self.set_type(pgmenu.CHECKBOX)

        self._set_indicator("check_")
        self._set_on_attr("checked")

        super().__init__(**kwargs)

        self.master = master
        self.coords = resolve(coords, "coords", self.type)
        self.size = self._format_size(size)
        self.fill = resolve(fill, "fill", self.type)

        self.text = resolve(text, "text", self.type)
        self.text_color = resolve(text_color, "text_color", self.type)
        self.check_fill = resolve(check_fill, "check_fill", self.type)
        self.margin = resolve(margin, "margin", self.type)

        self.width = resolve(width, "width", self.type)
        self.border_radius = resolve(border_radius, "border_radius", self.type, round(min(self.size) / 3.3))

        self.checked = resolve(checked, "checked", self.type)

        # Kwargs attributes
        self.text_side = resolve_kwarg(kwargs, "text_side", self.type)
        self.text_margin = resolve_kwarg(kwargs, "text_margin", self.type)
        self.text_side_margin = resolve_kwarg(kwargs, "text_side_margin", self.type, self.margin.base_value)
        # Checkmark (rect) kwargs attributes
        self._init_rect(kwargs, "check_")
        self.check_border_radius = resolve_kwarg(kwargs, "check_border_radius", self.type, self.border_radius.base_value - self.margin.base_value)

        self.check_base_transparency = resolve_kwarg(kwargs, "check_base_transparency", self.type)
        # Setting base custom animation
        if not isinstance(kwargs.get("check_transparency"), AnimateType):
            self.check_transparency = pgmenu.animation.Animate(self.check_base_transparency, self.check_transparency, self.animation_duration, self.animation_curve, self.animation_precision)
        
        pgmenu.widgets.add(self)

    def check(self):
        self.checked = True
        self.on_select()
        # FIXME -> animation_on_select or _on_deselect might not have self.check_transparency for done check
        pgmenu.animation.run_callable(self.animation_on_select, done=lambda: self.check_transparency.done)

    def uncheck(self):
        self.checked = False
        self.on_deselect()
        # FIXME -> animation_on_select or _on_deselect might not have self.check_transparency for done check
        pgmenu.animation.run_callable(self.animation_on_deselect, done=lambda: self.check_transparency.done)

    def toggle(self):
        self.check() if not self.checked else self.uncheck()
