import pygame
import pgmenu
from pgmenu.widget import Widget, RectMixin, TextMixin
from pgmenu.constants import THEME
from pgmenu.theme import resolve, resolve_kwarg
from pgmenu.animation import *


class Checkbox(Widget, RectMixin, TextMixin):

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

        self.type = pgmenu.CHECKBOX

        super().__init__(**kwargs)

        self.master = master
        self.coords = resolve(coords, pgmenu.Theme.checkbox_coords)
        self.size = self._format_size(size)
        self.fill = resolve(fill, pgmenu.Theme.checkbox_fill)

        self.text = resolve(text, pgmenu.Theme.checkbox_text)
        self.text_color = resolve(text_color, pgmenu.Theme.checkbox_text_color)
        self.check_fill = resolve(check_fill, pgmenu.Theme.checkbox_check_fill)
        self.margin = resolve(margin, pgmenu.Theme.checkbox_margin)

        self.width = resolve(width, pgmenu.Theme.checkbox_width)
        self.border_radius = resolve(border_radius, pgmenu.Theme.checkbox_border_radius, round(min(self.size) / 3.3))

        self.checked = resolve(checked, pgmenu.Theme.checkbox_checked)

        # Kwargs attributes
        self.text_side = resolve_kwarg(kwargs, "text_side", pgmenu.Theme.checkbox_text_side)
        self.text_margin = resolve_kwarg(kwargs, "text_margin", pgmenu.Theme.checkbox_text_margin)
        self.text_side_margin = resolve_kwarg(kwargs, "text_side_margin", pgmenu.Theme.checkbox_text_side_margin, self.margin.base_value)
        # Checkmark (rect) kwargs attributes
        self._init_rect(kwargs, "check_")
        self.check_border_radius = resolve_kwarg(kwargs, "check_border_radius", pgmenu.Theme.checkbox_check_border_radius, self.border_radius.base_value - self.margin.base_value)

        pgmenu.widget.add(self)

    def _format_size(self, size):
        size = resolve(size, pgmenu.Theme.checkbox_size)

        if isinstance(size, (int, float)):
            size = size, size

        elif isinstance(size, Animate):
            size = size.value, size.value

        return size

    def check(self):
        self.checked = True

    def uncheck(self):
        self.checked = False

    def toggle(self):
        self.checked = False if self.checked else True

    def draw(self):
        super().draw()

        # The largest extent the checkbox will ever reach across its animation, regardless of whether hover grows or shrinks it.
        # This is the stable "slot" size the checkbox is centered within, so growth/shrink never shifts the text.
        max_w = max(self.size.base_tuple[0], self.size.final_tuple[0])
        max_h = max(self.size.base_tuple[1], self.size.final_tuple[1])

        full_rect = (0, 0, *self.size.int_tuple)

        checkbox_surface = pgmenu.draw.aarect(None, self.fill, full_rect, self.width, self.border_radius,
                                              self.border_top_left_radius, self.border_top_right_radius,
                                              self.border_bottom_left_radius, self.border_bottom_right_radius,
                                              self.antialiasing, self.transparency, self.aa_strength,
                                              inner_fill=self.inner_fill, inner_transparency=self.inner_transparency,
                                              inner_aa_strength=self.inner_aa_strength, inner_antialiasing=self.inner_antialiasing)

        if self.checked:
            check_rect = (self.margin.int, self.margin.int, self.size.int_tuple[0] - self.margin.int*2, self.size.int_tuple[1] - self.margin.int*2)
            pgmenu.draw.aarect(checkbox_surface, self.check_fill, check_rect, self.check_width, self.check_border_radius,
                               self.check_border_top_left_radius, self.check_border_top_right_radius,
                               self.check_border_bottom_left_radius, self.check_border_bottom_right_radius,
                               self.check_antialiasing, self.check_transparency, self.check_aa_strength,
                               inner_fill=self.check_inner_fill, inner_transparency=self.check_inner_transparency,
                               inner_aa_strength=self.check_inner_aa_strength, inner_antialiasing=self.check_inner_antialiasing)

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

        # Combined surface sized off the MAX checkbox extent, plus text
        # (if any), so it's constant across the hover animation either way.
        surface_size = (max_w + side_margin + text_surf_size[0], max_h)
        self.surface = pgmenu.surface.cached_surface(surface_size, pygame.SRCALPHA)

        if has_text and self.text_side == pgmenu.LEFT:
            text_x = 0
            checkbox_x = text_surf_size[0] + side_margin
        else:  # pgmenu.RIGHT (default), or no text at all
            checkbox_x = 0
            text_x = max_w + side_margin

        checkbox_pos = pgmenu.position.center_coords(checkbox_surface.get_size(), (checkbox_x, 0, max_w, max_h))
        self.surface.blit(checkbox_surface, checkbox_pos)

        if has_text:
            text_pos = pgmenu.position.center_coords(text_surf_size, (text_x, 0, text_x + text_surf_size[0], max_h), center_x=False)
            self.surface.blit(text_surface, text_pos)

        self.master.blit(self.surface, self.coords.int_tuple)

    def update(self, event):
        super().update(event)

        # Detect mouse collisions
        if self.state == pgmenu.HOVERED or self.state == pgmenu.ACTIVE:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.state = pgmenu.ACTIVE
                    self.on_press()
                    self.animation_on_press()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.state = pgmenu.NORMAL
                    self.toggle()

                    self.on_release()
                    self.animation_on_release()

            elif pygame.mouse.get_pressed()[0]:
                self.on_hold()
                self.animation_on_hold()

    def resize(self, w, h):
        self._resize_border_radii(w, h)
        self._resize_rect("check_", w, h)
        
        # Change margin size dynamically
        factor = min(w / self.base_size[0], h / self.base_size[1])
        self.margin = int(self.margin * factor)

        self.size = w, h

    def m_animation_on_standby(self):
        if not self.disable_animation:
            self.size.update(pgmenu.BACKWARD)
            self.fill.update(pgmenu.BACKWARD)
            self.margin.update(pgmenu.BACKWARD)
            self._animation_update_border_radii(pgmenu.BACKWARD)
            self._animation_update_rect("check_", pgmenu.BACKWARD)

    def m_animation_on_hover(self):
        if not self.disable_animation:
            self.size.update(pgmenu.FORWARD)
            self.fill.update(pgmenu.FORWARD)
            self.margin.update(pgmenu.FORWARD)
            self._animation_update_border_radii(pgmenu.FORWARD)
            self._animation_update_rect("check_", pgmenu.FORWARD)

    def m_animation_on_hold(self):
        if not self.disable_animation:
            self.size.update(pgmenu.BACKWARD, 0.15)
            self.margin.update(pgmenu.BACKWARD, 0.15)
            self._animation_update_border_radii(pgmenu.BACKWARD, 0.15)
            self._animation_update_rect("check_", pgmenu.BACKWARD, 0.15)

    def request_cursor(self):
        pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_HAND