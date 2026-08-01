import pygame
import pgmenu
from pgmenu.widget import Widget, RectMixin, TextMixin
from pgmenu.constants import THEME
from pgmenu.theme import resolve
from pgmenu.animation import *


class Button(Widget, RectMixin, TextMixin):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 coords: list | tuple | AnimateTuple = THEME,
                 size: list | tuple | AnimateTuple = THEME,
                 fill: tuple[int, int, int] | AnimateTuple | pygame.Surface | AnimateSurface = THEME,
                 text: str = THEME,
                 text_color: tuple[int, int, int] | AnimateTuple = THEME,
                 icon: pygame.Surface | AnimateSurface = THEME,
                 margin: int | Animate = THEME,
                 width: int | Animate = THEME,
                 border_radius: int | Animate = THEME,
                 **kwargs):
        """
        :param master:
        :param coords:
        :param size:
        :param fill:
        :param text:
        :param text_color:
        :param icon: Has to be a Surface
        :param margin:
        :param width:
        :param border_radius:
        """

        self.type = pgmenu.BUTTON

        super().__init__(**kwargs)

        self.master = master
        self.coords = resolve(coords, pgmenu.Theme.button_coords)
        self.size = resolve(size, pgmenu.Theme.button_size)
        self.fill = resolve(fill, pgmenu.Theme.button_fill)

        self.text = resolve(text, pgmenu.Theme.button_text)
        self.text_color = resolve(text_color, pgmenu.Theme.button_text_color)
        self.icon = resolve(icon, pgmenu.Theme.button_icon)
        self.margin = resolve(margin, pgmenu.Theme.button_margin)

        self.width = resolve(width, pgmenu.Theme.button_width)
        self.border_radius = resolve(border_radius, pgmenu.Theme.button_border_radius, round(min(self.size) / 3))

        pgmenu.widget.add(self)

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

    def get_icon(self):
        return self.icon

    def get_margin(self):
        return self.margin

    def get_width(self):
        return self.width

    def get_border_radius(self):
        return self.border_radius

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

        text_surface, text_rect = pgmenu.text.fit_render_animated(self.size, self.text, self.text_color, round(self.margin), self.text_font,  # In case margin is animated, it has to be passed as a whole number into fit_text
                                                                  self.text_background, self.text_antialias, self.text_italic, self.text_bold,
                                                                  self.text_strikethrough, self.text_underline, self.text_transparency)

        if self.icon is not None:
            # Use render once to get exact text proportions for the icon/text split;
            # fit_text below reuses the render cache internally
            text_2d_size = pgmenu.text.render(self.text).get_size()
            icon_rect, text_rect = pgmenu.rect.fit_rects(self.size.int_tuple, self.icon.get_size(), text_2d_size, margin=self.margin)
            icon_surface = pgmenu.surface.resize(self.icon, icon_rect[2:])

            icon_rect, text_rect = pgmenu.rect.center_rects((0, 0, *self.surface.get_size()), icon_rect, text_rect)

            self.surface.blit(icon_surface, icon_rect[:2])

        self.surface.blit(text_surface, text_rect[:2])
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
                    self.on_release()
                    self.animation_on_release()

            elif pygame.mouse.get_pressed()[0]:
                self.on_hold()
                self.animation_on_hold()

    def resize(self, w, h):
        self._resize_border_radii(w, h)

        self.size = w, h

    def m_animation_on_standby(self):
        if not self.disable_animation:
            self.size.update(pgmenu.BACKWARD)
            self.fill.update(pgmenu.BACKWARD)
            self._animation_update_border_radii(pgmenu.BACKWARD)

    def m_animation_on_hover(self):
        if not self.disable_animation:
            self.size.update(pgmenu.FORWARD)
            self.fill.update(pgmenu.FORWARD)
            self._animation_update_border_radii(pgmenu.FORWARD)

    def m_animation_on_hold(self):
        if not self.disable_animation:
            self.size.update(pgmenu.BACKWARD, 0.15)
            self._animation_update_border_radii(pgmenu.BACKWARD, 0.15)

    def m_on_release(self):
        print('Button pressed')

    def request_cursor(self):
        pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_HAND