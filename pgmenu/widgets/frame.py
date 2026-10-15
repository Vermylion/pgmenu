import math
import pygame
import pgmenu

from pgmenu.base import Widget, RectMixin
from pgmenu.core.animation import Animate, AnimateTuple, AnimateSurface
from pgmenu.core.theme import resolve, resolve_kwarg
from pgmenu.vars.constants import THEME


__all__ = ["Frame"]


class Frame(Widget, RectMixin):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 coords: list | tuple | AnimateTuple = THEME,
                 size: list | tuple | AnimateTuple = THEME,
                 fill: tuple[int, int, int] | pygame.Surface | AnimateSurface = THEME,
                 width: int | Animate = THEME,
                 border_radius: int | Animate = THEME,
                 **kwargs):

        self.set_type(pgmenu.FRAME)

        super().__init__(**kwargs)

        self.master = master
        self.coords = resolve(coords, pgmenu.Theme.frame_coords)
        self.size = resolve(size, pgmenu.Theme.frame_size)

        self.fill = resolve(fill, pgmenu.Theme.frame_fill)
        self.width = resolve(width, pgmenu.Theme.frame_width)

        self.border_radius = resolve(border_radius, pgmenu.Theme.frame_border_radius, round(min(self.size) / 7))

        self.content_size = resolve_kwarg(kwargs, "content_size", pgmenu.Theme.frame_content_size, self.size)
        self.scroll_offset = resolve_kwarg(kwargs, "scroll_offset", pgmenu.Theme.frame_scroll_offset)

        x, y = self.scroll_offset
        self.scroll_offset = pgmenu.animation.AnimateTuple([x, x], [y, y], duration=self.animation_duration, curve=self.animation_curve, precision=self.animation_precision)
        # Mouse wheel scroll step
        self.scroll_step = resolve_kwarg(kwargs, "scroll_step", pgmenu.Theme.frame_scroll_step)
        # Min Max duration of scroll animation
        self.min_scroll_duration = resolve_kwarg(kwargs, "min_scroll_duration", pgmenu.Theme.frame_min_scroll_duration)
        self.max_scroll_duration = resolve_kwarg(kwargs, "max_scroll_duration", pgmenu.Theme.frame_max_scroll_duration)
        # Internal attribute for clearing up loose animations quicker
        self._animate_scroll = None

        self.widgets = []
        self._widgets_to_blit = {}

        pgmenu.widgets.add(self)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        if key == "content_size" and not pgmenu.vars.videoresized:
            setattr(self, f"base_{key}", value)

    def add(self, *widgets):
        self.widgets += widgets

    def remove(self,
               *widgets):
        for widget in widgets:
            if widget in self.widgets:
                self.widgets.remove(widget)

    def blit(self, surface, coords):
        self._widgets_to_blit[surface] = coords

    def scroll_x_by(self, dx: int, animate: bool = THEME):
        animate = resolve(animate, pgmenu.Theme.frame_animate_scroll)

        self.scroll_by(dx, 0, animate)

    def scroll_y_by(self, dy: int, animate: bool = THEME):
        animate = resolve(animate, pgmenu.Theme.frame_animate_scroll)

        self.scroll_by(0, dy, animate)

    def scroll_by(self, dx: int, dy: int, animate: bool = THEME):
        animate = resolve(animate, pgmenu.Theme.frame_animate_scroll)

        self.scroll_to(self.scroll_offset.final_value[0] + dx, self.scroll_offset.final_value[1] + dy, animate)

    def scroll_x_to(self, x: int, animate: bool = THEME):
        animate = resolve(animate, pgmenu.Theme.frame_animate_scroll)

        self.scroll_to(x, self.scroll_offset.final_value[1], animate)

    def scroll_y_to(self, y: int, animate: bool = THEME):
        animate = resolve(animate, pgmenu.Theme.frame_animate_scroll)

        self.scroll_to(self.scroll_offset.final_value[0], y, animate)

    def scroll_to(self, x: int, y: int, animate: bool = THEME):
        animate = resolve(animate, pgmenu.Theme.frame_animate_scroll)

        # Clamp scroll offset x,y
        x, y = max(x, 0), max(y, 0)
        x, y = min(x, self.content_size[0] - self.size[0]),  min(y, self.content_size[1] - self.size[1])

        # Wether new pos should trigger animation or not
        base_x, base_y = self.scroll_offset.float_tuple if animate else (x, y)

        # Total quadratic distance the frame can travel # TODO -> Test it feels natural with x and y scrolling
        content_travel = math.sqrt((self.content_size[0] - self.size[0]) ** 2 + (self.content_size[1] - self.size[1]) ** 2)
        # Duration set from 0 to 1: percentage of distance asked to travel
        duration = math.sqrt((base_x - x) ** 2 + (base_y - y) ** 2) / content_travel
        # Clamp scroll animation duration
        duration = max(duration, self.min_scroll_duration)
        duration = min(duration, self.max_scroll_duration)

        self.scroll_offset = pgmenu.animation.AnimateTuple([base_x, x], [base_y, y], duration=duration, curve=self.animation_curve, precision=self.animation_precision)
        # Reset previous animation
        for item in self.scroll_offset.items:
            item.done = False

        # Clear up old animation
        pgmenu.animation.stop_animation(self._animate_scroll)

        self._animate_scroll = pgmenu.animation.run_animation(self.scroll_offset, pgmenu.FORWARD)


    def set_content_size(self, w: int, h: int):
        self.content_size = max(w, self.size[0]), max(h, self.size[1])

    def draw(self):
        super().draw()

        self.surface = pgmenu.draw.aarect(None, self.fill, (0, 0, *self.size.int_tuple), self.width, self.border_radius,
                                        self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius,
                                        self.antialiasing, self.transparency, self.aa_strength, inner_fill=self.inner_fill,
                                        inner_transparency=self.inner_transparency, inner_aa_strength=self.inner_aa_strength, inner_antialiasing=self.inner_antialiasing)

        self.draw_widgets()

        self.blit_to_master()

    # FIXME -> Performance issue: all widgets, in clntent_size or not, get drawn to the surface
    def draw_widgets(self):
        for surface, coords in self._widgets_to_blit.items():
            # w, h = surface.get_size()
            # if (self.scroll_offset[0] < coords[0] + w < self.scroll_offset[0] + self.size[0]) and (self.scroll_offset[1] < coords[1] + w < self.scroll_offset[1] + self.size[1]):
            self.surface.blit(surface, coords)

        self._widgets_to_blit.clear()

    def update(self, event):
        super().update(event)

        if self.state == pgmenu.HOVERED or self.state == pgmenu.ACTIVE:
            if event.type == pygame.MOUSEWHEEL:
                scroll_travel_x = max(min(event.precise_x * self.scroll_step, self.scroll_step), -1 * self.scroll_step)
                scroll_travel_y = max(min(event.precise_y * -1 * self.scroll_step, self.scroll_step), -1 * self.scroll_step)

                # Left Shift inverts x,y movement between themselves -> x becomes y and y becomes x
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    scroll_travel_x, scroll_travel_y = scroll_travel_y, scroll_travel_x

                self.scroll_by(scroll_travel_x, scroll_travel_y, animate=True)

    def resize(self, w: int, h: int):
        self._resize_border_radii(w, h)

        self.size = w, h

        factor = min(w / self.base_size[0], h / self.base_size[1])

        # TODO -> Check that this is indeed correct content_size resizing
        self.content_size = round(self.base_content_size[0] * factor), round(self.base_content_size[1] * factor)