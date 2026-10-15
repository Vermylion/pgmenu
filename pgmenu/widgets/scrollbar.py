import pygame
import pgmenu

from pgmenu.base import Widget, RectMixin, ActionableMixin
from pgmenu.core.animation import Animate, AnimateTuple, AnimateSurface, AnimateType
from pgmenu.core.theme import resolve, resolve_kwarg
from pgmenu.vars.constants import THEME


__all__ = ['Scrollbar']


# TODO -> Have scrollbar be automatically drawn on top of all the widgets?


class Scrollbar(Widget, RectMixin, ActionableMixin):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 placement: str = THEME,
                 thickness: int | Animate = THEME,
                 fill: tuple[int, int, int] | AnimateTuple | pygame.Surface | AnimateSurface = THEME,
                 thumb_fill: tuple[int, int, int] | AnimateTuple | pygame.Surface | AnimateSurface = THEME,
                 margin: int | Animate = THEME,
                 **kwargs):

        self.set_type(pgmenu.SCROLLBAR)

        super().__init__(**kwargs)

        # Only frames can scroll so anything else is an error
        self.master = master
        if not isinstance(self.master, pgmenu.widgets.Frame):
            raise TypeError("Scrollbar master must be a Frame object/widget")

        # Left/right means vertical bar, top/bottom means horizontal
        self.placement = resolve(placement, pgmenu.Theme.scrollbar_placement)
        self.orientation = pgmenu.VERTICAL if self.placement in (pgmenu.LEFT, pgmenu.RIGHT) else pgmenu.HORIZONTAL
        self.thickness = resolve(thickness, pgmenu.Theme.scrollbar_thickness)
        self.base_thickness = resolve_kwarg(kwargs, "base_thickness", pgmenu.Theme.scrollbar_base_thickness)
        # Setting base custom animation
        if not isinstance(thickness, AnimateType):
            self.thickness = pgmenu.animation.Animate(self.base_thickness, self.thickness, self.animation_duration, self.animation_curve, self.animation_precision)

        self.fill = resolve(fill, pgmenu.Theme.scrollbar_fill)
        self.thumb_fill = resolve(thumb_fill, pgmenu.Theme.scrollbar_thumb_fill)
        self.margin = resolve(margin, pgmenu.Theme.scrollbar_margin)

        self.border_radius = resolve_kwarg(kwargs, "border_radius", pgmenu.Theme.scrollbar_border_radius)

        # Thumb gets its own rect attributes, hence the prefix
        self._init_rect(kwargs, "thumb_")
        self.thumb_rect = (0, 0, 0, 0)
        # Default radius is half the thumb width so the ends are fully round
        self.thumb_border_radius = resolve_kwarg(kwargs, "thumb_border_radius", pgmenu.Theme.scrollbar_thumb_border_radius, (self.thickness.final_value / 2) - self.margin)
        self.thumb_min_length = resolve_kwarg(kwargs, "thumb_min_length", pgmenu.Theme.scrollbar_thumb_min_length)

        self.disable_track = resolve_kwarg(kwargs, "disable_track", pgmenu.Theme.scrollbar_disable_track)

        # Setting base custom animation
        self.base_transparency = resolve_kwarg(kwargs, "base_transparency", pgmenu.Theme.scrollbar_base_transparency)
        if not isinstance(kwargs.get("transparency", None), AnimateType):
            self.transparency = pgmenu.animation.Animate(self.base_transparency, self.transparency, self.animation_duration, self.animation_curve, self.animation_precision)


        pgmenu.widgets.add(self)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        # Keep the unscaled values around so resize() can scale from them
        if key in ("thickness", "base_thickness") and not pgmenu.vars.videoresized and not isinstance(value, AnimateType):
            setattr(self, f"resize_base_{key}", value)

        # Wrap plain ints in an Animate so thickness always has .int/.final_value
        if key == "thickness" and hasattr(self, "base_thickness") and not isinstance(value, AnimateType):
            self.thickness = pgmenu.animation.Animate(self.base_thickness, value, self.animation_duration, self.animation_curve, self.animation_precision)

        # FIXME -> Is this necessary with a call in update?
        if hasattr(self, "placement") and hasattr(self, "orientation") and hasattr(self, "thickness"):
            if key in ("placement", "orientation", "thickness"):
                self._update_base_attr()

    def _update_base_attr(self):
        t = self.thickness.int
        w, h = self.master.size
        r = self.master.border_radius

        # Track length leaves room for the master's rounded corners
        self.size = (t, h - r * 2) if self.orientation == pgmenu.VERTICAL else (w - r * 2, t)

        # Stick to the chosen edge, offset by the corner radius on the other axis
        self.coords = (w - t if self.placement == pgmenu.RIGHT else 0 if self.placement == pgmenu.LEFT else r,
                       h - t if self.placement == pgmenu.BOTTOM else 0 if self.placement == pgmenu.TOP else r)

    def draw(self):
        super().draw()

        # idx picks the axis we care about, y for vertical and x for horizontal
        is_vertical = self.orientation == pgmenu.VERTICAL
        idx = 1 if is_vertical else 0

        inner_len = self.size[idx] - 2 * self.margin
        c_size, m_size, s_offset = self.master.content_size[idx], self.master.size[idx], self.master.scroll_offset[idx]

        # Thumb length is the visible fraction of the content, never below the minimum
        thumb_len = max(int(inner_len * m_size / c_size), self.thumb_min_length) if c_size > 0 else self.thumb_min_length
        # Map scroll progress onto the free space the thumb can travel in
        offset = self.margin + (s_offset / (c_size - m_size)) * (inner_len - thumb_len) if c_size > m_size else self.margin

        self.thumb_rect = (self.margin, offset, self.size[0] - self.margin * 2, thumb_len) if is_vertical else (offset, self.margin, thumb_len, self.size[1] - self.margin * 2)

        scrollbar_surface = pgmenu.draw.aarect(None, self.fill, (0, 0, *self.size), self.width, self.border_radius,
                                                  self.border_top_left_radius, self.border_top_right_radius,
                                                  self.border_bottom_left_radius, self.border_bottom_right_radius,
                                                  self.antialiasing, self.transparency, self.aa_strength,
                                                  inner_fill=self.inner_fill, inner_transparency=self.inner_transparency,
                                                  inner_aa_strength=self.inner_aa_strength, inner_antialiasing=self.inner_antialiasing)

        thumb_surface = pgmenu.draw.aarect(None, self.thumb_fill, self.thumb_rect, self.thumb_width, self.thumb_border_radius,
                           self.thumb_border_top_left_radius, self.thumb_border_top_right_radius,
                           self.thumb_border_bottom_left_radius, self.thumb_border_bottom_right_radius,
                           self.thumb_antialiasing, self.thumb_transparency, self.thumb_aa_strength,
                           inner_fill=self.thumb_inner_fill, inner_transparency=self.thumb_inner_transparency,
                           inner_aa_strength=self.thumb_inner_aa_strength, inner_antialiasing=self.thumb_inner_antialiasing)

        # Track first, thumb on top
        self.surface = pgmenu.cache.cached_surface(self.size, pygame.SRCALPHA)
        self.surface.blit(scrollbar_surface, (0, 0))
        self.surface.blit(thumb_surface, self.thumb_rect[:2])

        self.blit_to_master()

    def update(self, event):
        super().update(event)

        self._update_base_attr()

        # Nothing to do unless the mouse is on us or we're mid-drag
        if self.state not in (pgmenu.HOVERED, pgmenu.ACTIVE):
            return

        is_vertical = self.orientation == pgmenu.VERTICAL
        idx = 1 if is_vertical else 0

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            # thumb_rect is relative to the scrollbar, so convert it to screen coords for the mouse check
            tx, ty, tw, th = self.thumb_rect
            cx, cy = self.coords[0] + self.master.coords[0], self.coords[1] + self.master.coords[1]
            abs_thumb_rect = pygame.Rect((cx, ty + cy, self.thickness.int, th) if is_vertical else (tx + cx, cy, tw, self.thickness.int))

            if abs_thumb_rect.collidepoint(pgmenu.vars.mouse_x, pgmenu.vars.mouse_y):
                    # Clear the stored mouse movement so the drag doesn't start with a jump
                    pygame.mouse.get_rel()
                    self.state = pgmenu.ACTIVE
            else:
                # Clicked on the track, scroll to that spot
                mouse_val = pgmenu.vars.mouse_y if is_vertical else pgmenu.vars.mouse_x
                ratio = (mouse_val - self.coords[idx] - self.master.coords[idx]) / self.size[idx]
                target_pos = ratio * (self.master.content_size[idx] - self.master.size[idx])

                (self.master.scroll_y_to if is_vertical else self.master.scroll_x_to)(target_pos, animate=True)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            self.state = pgmenu.NORMAL

        elif event.type == pgmenu.IDLE_EVENT and self.state == pgmenu.ACTIVE:
            # Thumb moves less than the content, so scale the mouse delta up by the content/track ratio
            ratio = (self.master.content_size[idx] - self.master.size[idx]) / (self.size[idx] - self.thumb_rect[idx + 2])
            delta = ratio * pygame.mouse.get_rel()[idx]
            delta_2d = (0, delta) if is_vertical else (delta, 0)

            # No animation while dragging, it would lag behind the mouse
            self.master.scroll_by(*delta_2d, animate=False)


    def resize(self, w: int, h: int):
        self._resize_border_radii(w, h)
        self._resize_rect("thumb_", w, h)

        # Scale everything by the smaller axis so nothing overflows
        factor = min(w / self.base_size[0], h / self.base_size[1])
        self.margin = round(self.base_margin * factor)

        self.base_thickness = round(self.resize_base_base_thickness * factor)
        self.thickness = round(self.resize_base_thickness * factor)