import pygame
import pgmenu
from pgmenu.core import cache

from pgmenu.base.widget import Widget
from pgmenu.base.mixins import RectMixin, TextMixin, ActionableMixin


__all__ = ["ToggleWidget"]


class ToggleWidget(Widget, RectMixin, TextMixin, ActionableMixin):
    """
    Shared base for indicator+label widgets (Checkbox, Radiobutton, ...).
    Subclasses set, before super().__init__():
        self._set_indicator("prefix_")
        self._set_on_attr("name")
    """

    @property
    def is_on(self):
        return getattr(self, self._on_attr)

    @is_on.setter
    def is_on(self, value):
        setattr(self, self._on_attr, value)

    def _set_on_attr(self, name):
        self._on_attr = name

    def _set_indicator(self, prefix):
        self._indicator_prefix = prefix

    def _indicator(self, name):
        return getattr(self, f"{self._indicator_prefix}{name}")

    def toggle(self):
        self.is_on = not self.is_on

    def draw(self):
        super().draw()

        max_w = max(self.size.base_tuple[0], self.size.final_tuple[0])
        max_h = max(self.size.base_tuple[1], self.size.final_tuple[1])
        full_rect = (0, 0, *self.size.int_tuple)

        toggle_surface = pgmenu.draw.aarect(None, self.fill, full_rect, self.width, self.border_radius,
                                          self.border_top_left_radius, self.border_top_right_radius,
                                          self.border_bottom_left_radius, self.border_bottom_right_radius,
                                          self.antialiasing, self.transparency, self.aa_strength,
                                          inner_fill=self.inner_fill, inner_transparency=self.inner_transparency,
                                          inner_aa_strength=self.inner_aa_strength, inner_antialiasing=self.inner_antialiasing)

        inner_rect = (self.margin.int, self.margin.int,
                     self.size.int_tuple[0] - self.margin.int * 2, self.size.int_tuple[1] - self.margin.int * 2)
        pgmenu.draw.aarect(toggle_surface, self._indicator("fill"), inner_rect, self._indicator("width"),
                         self._indicator("border_radius"),
                         self._indicator("border_top_left_radius"), self._indicator("border_top_right_radius"),
                         self._indicator("border_bottom_left_radius"), self._indicator("border_bottom_right_radius"),
                         self._indicator("antialiasing"), self._indicator("transparency"), self._indicator("aa_strength"),
                         inner_fill=self._indicator("inner_fill"), inner_transparency=self._indicator("inner_transparency"),
                         inner_aa_strength=self._indicator("inner_aa_strength"), inner_antialiasing=self._indicator("inner_antialiasing"))

        has_text = self.text is not None and self.text != ""
        if has_text:
            text_surface = pgmenu.text.fit_height_render(self.size.base_tuple[1], self.text, self.text_color, round(self.text_margin), self.text_font,
                                                       self.text_background, self.text_antialias, self.text_italic, self.text_bold,
                                                       self.text_strikethrough, self.text_underline, self.text_transparency)
            text_surf_size = text_surface.get_size()
            side_margin = self.text_side_margin
        else:
            text_surface, text_surf_size, side_margin = None, (0, 0), 0

        surface_size = (max_w + side_margin + text_surf_size[0], max_h)
        self.surface = cache.cached_surface(surface_size, pygame.SRCALPHA)

        if has_text and self.text_side == pgmenu.LEFT:
            text_x, toggle_x = 0, text_surf_size[0] + side_margin
        else:
            toggle_x, text_x = 0, max_w + side_margin

        toggle_pos = pgmenu.position.center_coords(toggle_surface.get_size(), (toggle_x, 0, max_w, max_h))
        self.surface.blit(toggle_surface, toggle_pos)

        if has_text:
            text_pos = pgmenu.position.center_coords(text_surf_size, (text_x, 0, text_x + text_surf_size[0], max_h), center_x=False)
            self.surface.blit(text_surface, text_pos)

        self.blit_to_master()

    # TODO: IMPORTANT -> Revamp update system with states and/or update mixin handling
    def update(self, event):
        super().update(event)

        # Detect mouse collisions
        if self.state == pgmenu.HOVERED or self.state == pgmenu.ACTIVE:

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.toggle()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.toggle()

        self._mixin_hook("_mixin_update", event)

    def resize(self, w: int, h: int):
        self._resize_border_radii(w, h)
        self._resize_rect(self._indicator_prefix, w, h)

        factor = min(w / self.base_size[0], h / self.base_size[1])
        self.margin = int(self.base_margin * factor)

        self.size = w, h
