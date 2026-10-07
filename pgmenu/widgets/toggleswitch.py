import pygame
import pgmenu

from pgmenu.base import Widget, ToggleWidget
from pgmenu.core.animation import Animate, AnimateTuple, AnimateSurface, AnimateType
from pgmenu.core.theme import resolve, resolve_kwarg
from pgmenu.vars.constants import THEME


__all__ = ["ToggleSwitch"]


class ToggleSwitch(ToggleWidget):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 coords: list | tuple | AnimateTuple = THEME,
                 size: int | list | tuple | Animate | AnimateTuple = THEME,
                 fill: tuple[int, int, int] | AnimateTuple | pygame.Surface | AnimateSurface = THEME,
                 text: str | None = THEME,
                 text_color: tuple[int, int, int] | AnimateTuple = THEME,
                 thumb_fill: tuple[int, int, int] | AnimateTuple = THEME,
                 margin: int | Animate = THEME,
                 width: int | Animate = THEME,
                 border_radius: int | Animate = THEME,
                 on: bool = THEME,
                 **kwargs):

        self.set_type(pgmenu.TOGGLESWITCH)

        self._set_indicator("thumb_")
        self._set_on_attr("on")

        super().__init__(**kwargs)

        self.master = master
        self.coords = resolve(coords, pgmenu.Theme.toggleswitch_coords)
        self.size = self._format_size(size)

        self.fill = resolve(fill, pgmenu.Theme.toggleswitch_fill)
        self.final_fill = resolve_kwarg(kwargs, "final_fill", pgmenu.Theme.toggleswitch_final_fill)
        # Setting base custom animation
        if not isinstance(fill, AnimateType):
            self.fill = pgmenu.animation.AnimateTuple((self.fill[0], self.final_fill[0]), (self.fill[1], self.final_fill[1]), (self.fill[2], self.final_fill[2]), duration=self.animation_duration, curve=self.animation_curve, precision=self.animation_precision)

        self.text = resolve(text, pgmenu.Theme.toggleswitch_text)
        self.text_color = resolve(text_color, pgmenu.Theme.toggleswitch_text_color)

        self.thumb_fill = resolve(thumb_fill, pgmenu.Theme.toggleswitch_thumb_fill)
        self.thumb_final_fill = resolve_kwarg(kwargs, "thumb_final_fill", pgmenu.Theme.toggleswitch_thumb_final_fill)
        # Setting base custom animation
        if not isinstance(thumb_fill, AnimateType):
            self.thumb_fill = pgmenu.animation.AnimateTuple((self.thumb_fill[0], self.thumb_final_fill[0]), (self.thumb_fill[1], self.thumb_final_fill[1]), (self.thumb_fill[2], self.thumb_final_fill[2]), duration=self.animation_duration, curve=self.animation_curve, precision=self.animation_precision)

        self.final_margin = resolve_kwarg(kwargs, "final_margin", pgmenu.Theme.toggleswitch_final_margin)
        self.margin = resolve(margin, pgmenu.Theme.toggleswitch_margin)
        # Setting base custom animation
        if not isinstance(margin, AnimateType):
            self.margin = pgmenu.animation.Animate(self.margin, self.final_margin, self.animation_duration, self.animation_curve, self.animation_precision)

        self.width = resolve(width, pgmenu.Theme.toggleswitch_width)
        self.border_radius = resolve(border_radius, pgmenu.Theme.toggleswitch_border_radius, round(min(self.size) / 3.3))

        self.on = resolve(on, pgmenu.Theme.toggleswitch_on)

        # Kwargs attributes
        self.text_side = resolve_kwarg(kwargs, "text_side", pgmenu.Theme.toggleswitch_text_side)
        self.text_margin = resolve_kwarg(kwargs, "text_margin", pgmenu.Theme.toggleswitch_text_margin)
        self.text_side_margin = resolve_kwarg(kwargs, "text_side_margin", pgmenu.Theme.toggleswitch_text_side_margin, self.margin.base_value)
        # Checkmark (rect) kwargs attributes
        self._init_rect(kwargs, "thumb_")
        self.thumb_border_radius = resolve_kwarg(kwargs, "thumb_border_radius", pgmenu.Theme.toggleswitch_thumb_border_radius, self.border_radius.base_value - self.margin.base_value)

        self.toggle_direction = resolve_kwarg(kwargs, "toggle_direction", pgmenu.Theme.toggleswitch_toggle_direction)

        self.transition = resolve_kwarg(kwargs, "transition", pgmenu.Theme.toggleswitch_transition)
        # Setting base custom animation
        if not isinstance(kwargs.get("transition"), AnimateType):
            self.transition = pgmenu.animation.Animate(self.transition, 1, self.animation_duration, self.animation_curve, None)

        # Internal attributes used for responsive resize

        pgmenu.widgets.add(self)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        if key == "final_margin" and not pgmenu.vars.videoresized:
            setattr(self, f"base_{key}", value)

        if key == "margin" and hasattr(self, "final_margin"):
            if not isinstance(value, AnimateType):
                self.margin = pgmenu.animation.Animate(value, self.final_margin, self.animation_duration, self.animation_curve, self.animation_precision)

    def turn_on(self):
        self.on = True
        self.on_select()
        # FIXME -> animation_on_select or _on_deselect might not have self.thumb_transparency for done check
        pgmenu.animation.run_callable(self.animation_on_select, done=lambda: self.thumb_fill.done)

    def turn_off(self):
        self.on = False
        self.on_deselect()
        # FIXME -> animation_on_select or _on_deselect might not have self.thumb_transparency for done check
        pgmenu.animation.run_callable(self.animation_on_deselect, done=lambda: self.thumb_fill.done)

    def toggle(self):
        self.turn_on() if not self.on else self.turn_off()

    def draw(self):
        Widget.draw(self)

        # The largest extent the toggleswitch will ever reach across its animation, regardless of whether hover grows or shrinks it.
        # This is the stable "slot" size the toggleswitch is centered within, so growth/shrink never shifts the text.
        max_w = max(self.size.base_tuple[0], self.size.final_tuple[0])
        max_h = max(self.size.base_tuple[1], self.size.final_tuple[1])

        full_rect = (0, 0, *self.size.int_tuple)

        toggleswitch_surface = pgmenu.draw.aarect(None, self.fill, full_rect, self.width, self.border_radius,
                                                self.border_top_left_radius, self.border_top_right_radius,
                                                self.border_bottom_left_radius, self.border_bottom_right_radius,
                                                self.antialiasing, self.transparency, self.aa_strength,
                                                inner_fill=self.inner_fill, inner_transparency=self.inner_transparency,
                                                inner_aa_strength=self.inner_aa_strength, inner_antialiasing=self.inner_antialiasing)

        # Code for smooth toggle transition
        x_on = self.size.int_tuple[0] - min(self.size.int_tuple)
        y_on = self.size.int_tuple[1] - min(self.size.int_tuple)

        transition = self.transition if self.toggle_direction == pgmenu.RIGHT else 1 - self.transition

        thumb_x = self.margin.int + x_on * transition
        thumb_y = self.margin.int + y_on * transition

        thumb_rect = (thumb_x, thumb_y, min(self.size.int_tuple) - self.margin.int * 2, min(self.size.int_tuple) - self.margin.int * 2)
        pgmenu.draw.aarect(toggleswitch_surface, self.thumb_fill, thumb_rect, self.thumb_width, self.thumb_border_radius,
                         self.thumb_border_top_left_radius, self.thumb_border_top_right_radius,
                         self.thumb_border_bottom_left_radius, self.thumb_border_bottom_right_radius,
                         self.thumb_antialiasing, self.thumb_transparency, self.thumb_aa_strength,
                         inner_fill=self.thumb_inner_fill, inner_transparency=self.thumb_inner_transparency,
                         inner_aa_strength=self.thumb_inner_aa_strength, inner_antialiasing=self.thumb_inner_antialiasing)

        has_text = self.text is not None and self.text != ""
        if has_text:
            text_surface = pgmenu.text.fit_height_render(self.size.base_tuple[1], self.text, self.text_color, round(self.text_margin), self.text_font,
                                                       self.text_background, self.text_antialias, self.text_italic, self.text_bold,
                                                       self.text_strikethrough, self.text_underline, self.text_transparency)
            text_surf_size = text_surface.get_size()
            side_margin = self.text_side_margin
        else:
            text_surface = None
            text_surf_size = (0, 0)
            side_margin = 0

        # Combined surface sized off the MAX toggleswitch extent, plus text
        # (if any), so it's constant across the hover animation either way.
        surface_size = (max_w + side_margin + text_surf_size[0], max_h)
        self.surface = pgmenu.cache.cached_surface(surface_size, pygame.SRCALPHA)

        if has_text and self.text_side == pgmenu.LEFT:
            text_x = 0
            toggleswitch_x = text_surf_size[0] + side_margin
        else:  # pgmenu.RIGHT (default), or no text at all
            toggleswitch_x = 0
            text_x = max_w + side_margin

        toggleswitch_pos = pgmenu.position.center_coords(toggleswitch_surface.get_size(), (toggleswitch_x, 0, max_w, max_h))
        self.surface.blit(toggleswitch_surface, toggleswitch_pos)

        if has_text:
            text_pos = pgmenu.position.center_coords(text_surf_size, (text_x, 0, text_x + text_surf_size[0], max_h), center_x=False)
            self.surface.blit(text_surface, text_pos)

        self.master.blit(self.surface, self.coords.int_tuple)

    def resize(self, w, h):
        self._resize_border_radii(w, h)
        self._resize_rect("thumb_", w, h)

        factor = min(w / self.base_size[0], h / self.base_size[1])

        self.final_margin = round(self.base_final_margin * factor)
        self.margin = round(self.base_margin * factor)

        self.size = w, h