import pygame
import pgmenu
from pgmenu.widget import Widget, RectMixin, TextMixin
from pgmenu.constants import THEME
from pgmenu.theme import resolve, resolve_kwarg
from pgmenu.animation import *


# TODO -> Switch Checkbox to a Button child?
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
        self.text_side_margin = resolve_kwarg(kwargs, "text_side_margin", pgmenu.Theme.checkbox_text_side_margin, self.margin)
        # Checkmark (rect) kwargs attributes
        self._init_rect(kwargs, "check_")
        self.check_border_radius = resolve_kwarg(kwargs, "check_border_radius", pgmenu.Theme.checkbox_check_border_radius, self.border_radius - self.margin)

        pgmenu.widget.add(self)

    def _format_size(self, size):
        size = resolve(size, pgmenu.Theme.checkbox_size)

        if isinstance(size, (int, float)):
            size = size, size

        elif isinstance(size, Animate):
            size = size.value, size.value

        return size

    def get_master(self):
        return self.master

    def get_coords(self):
        return self.coords

    def get_size(self):
        return self.size

    def get_fill(self):
        return self.fill

    def get_text(self):
        return self.text

    def get_text_color(self):
        return self.text_color

    def get_check_fill(self):
        return self.check_fill

    def get_margin(self):
        return self.margin

    def get_width(self):
        return self.width

    def get_border_radius(self):
        return self.border_radius

    def get_checked(self):
        return self.checked

    def is_checked(self):
        return self.checked

    def get_text_side(self):
        return self.text_side

    def get_text_margin(self):
        return self.text_margin

    def check(self):
        self.checked = True

    def uncheck(self):
        self.checked = False

    def toggle(self):
        self.checked = False if self.checked else True

    def draw(self):
        super().draw()

        coords = pgmenu.position.center_coords(self.size.int_tuple, (*self.coords.int_tuple, *self.size.base_tuple))

        full_rect = (0, 0, *self.size.int_tuple)

        self.surface = pgmenu.draw.aarect(None, self.fill, full_rect, self.width, self.border_radius,
                                              self.border_top_left_radius, self.border_top_right_radius,
                                              self.border_bottom_left_radius, self.border_bottom_right_radius,
                                              self.antialiasing, self.transparency, self.aa_strength,
                                              inner_fill=self.inner_fill, inner_transparency=self.inner_transparency,
                                              inner_aa_strength=self.inner_aa_strength, inner_antialiasing=self.inner_antialiasing)

        if self.checked:
            check_rect = (self.margin.int, self.margin.int, self.size.int_tuple[0] - self.margin.int*2, self.size.int_tuple[1] - self.margin.int*2)
            pgmenu.draw.aarect(self.surface, self.check_fill, check_rect, self.check_width, self.check_border_radius,
                               self.check_border_top_left_radius, self.check_border_top_right_radius,
                               self.check_border_bottom_left_radius, self.check_border_bottom_right_radius,
                               self.check_antialiasing, self.check_transparency, self.check_aa_strength,
                               inner_fill=self.check_inner_fill, inner_transparency=self.check_inner_transparency,
                               inner_aa_strength=self.check_inner_aa_strength, inner_antialiasing=self.check_inner_antialiasing)

        # TODO -> Add text: find a way to get the right size without fitting it to a restrictive rect
        # TODO -> Create self.surface -> Should it incorporate text or not -> self.rect linked to self.surface
        #           -> If text part of it, then should the hover grow animation also apply?
        #           -> What about cursor?
        # if self.text is not None and self.text != "":
        # text_surface, text_rect = pgmenu.text.fit_render_animated(self.size, self.text, self.text_color, round(self.text_margin), self.text_font,
        #                                                           self.text_background, self.text_antialias, self.text_italic, self.text_bold,
        #                                                           self.text_strikethrough, self.text_underline, self.text_transparency)

        self.master.blit(self.surface, coords)

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