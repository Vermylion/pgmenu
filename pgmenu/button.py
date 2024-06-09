import pgmenu
from pgmenu.animation import *
from pgmenu.widget import RectWidget
from pgmenu.constants import THEME

from typing import Callable

import pygame


# TODO -> Add icon

# TODO -> Handle fill and inside_fill switching when width or inside_fill

# TODO -> Color animation: other argument for secondary color?

# TODO -> Update fills to use AnimateFill

# TODO -> Can modify base values for widgets, through theme or constants or vars? Ex -> border_radius

# TODO -> Be able to set max text size / set text size?

# TODO -> Be able to change text or icon centering?

class Button(RectWidget):

    # Argument of value None represents the user has not modified it
    def __init__(self,
                 surface: pygame.Surface,
                 coords: tuple[int, int] | Animate = THEME,
                 size: tuple[int, int] | Animate = THEME,
                 fill: tuple[int, int, int] | pygame.Surface | AnimateFill = THEME,
                 icon: pygame.Surface | AnimateFill = THEME,
                 text: str = THEME,
                 text_font: str = THEME,
                 text_color: tuple[int, int, int] | AnimateColor = THEME,
                 margin: int | Animate = THEME,
                 width: int | Animate = THEME,
                 outline_fill: tuple[int, int, int] | pygame.Surface | AnimateFill = THEME,
                 border_radius: int | Animate = THEME,  # ! Need to be able to modify in theme
                 animation_scale: float | Animate = THEME,
                 animation_duration: float | Animate = THEME,
                 animation_curve: Callable = THEME,
                 on_standby: Callable = None,
                 on_hover: Callable = None,
                 on_press: Callable = None,
                 on_release: Callable = None,
                 **kwargs):

        # Animation
        self.animation_scale = animation_scale if animation_scale != THEME else pgmenu.Theme.animation_scale
        self.animation_duration = animation_duration if animation_duration != THEME else pgmenu.Theme.animation_duration
        self.animation_curve = animation_curve if animation_curve != THEME else pgmenu.Theme.animation_curve

        self.surface = surface if surface != THEME else pgmenu.Theme.surface
        self.coords = coords if coords != THEME else pgmenu.Theme.coords
        self.size = size if size != THEME else pgmenu.Theme.size
        self.fill = fill if fill != THEME else pgmenu.Theme.fill
        self.icon = icon if icon != THEME else pgmenu.Theme.icon
        self.text = text if text != THEME else pgmenu.Theme.button_text
        self.text_font = text_font if text_font != THEME else pgmenu.Theme.text_font
        self.text_color = text_color if text_color != THEME else pgmenu.Theme.text_color
        self.margin = margin if margin != THEME else pgmenu.Theme.margin # round(min(self.size.inttuple) * 0.1)
        self.width = width if width != THEME else pgmenu.Theme.width
        self.outline_fill = outline_fill if outline_fill != THEME else pgmenu.Theme.outline_fill
        # self.border_radius -> Border radius is taken care of in widget
        self.on_standby = on_standby if on_standby is not None else self.m_on_standby # pgmenu.Theme.on_standby
        self.on_hover = on_hover if on_hover is not None else self.m_on_hover # pgmenu.Theme.on_hover
        self.on_press = on_press if on_press is not None else self.m_on_press # pgmenu.Theme.on_press
        self.on_release = on_release if on_release is not None else self.m_on_release # pgmenu.Theme.on_release

        # A defined widget type for easier widget comprehension in code
        self.type = pgmenu.BUTTON

        # Declare other widget arguments
        super().__init__(border_radius, **kwargs)

        # Set up arguments
        # Add widget to widget list
        pgmenu.vars.widgets.append(self)

    def __setattr__(self, key, value):
        # Return if called with same value
        if hasattr(self, key) and getattr(self, key) == value:
            return False

        # Save current key's value to use for comparison later
        if hasattr(self, key): old_value = getattr(self, key)

        # Call the original __setattr__ method to set the attribute
        super().__setattr__(key, value)

        # Base Arguments
        # Animation Arguments
        if not isinstance(getattr(self, key), Animate | AnimateTuple | AnimateColor | AnimateFill) and getattr(self, key) is not None:
            if key == "coords": self.coords = AnimateTuple((self.coords[0], self.coords[0] * self.animation_scale), (self.coords[1], self.coords[1] * self.animation_scale), duration=self.animation_duration, curve=self.animation_curve)
            if key == "size": self.size = AnimateTuple((self.size[0], self.size[0] * self.animation_scale), (self.size[1], self.size[1] * self.animation_scale), duration=self.animation_duration, curve=self.animation_curve)
            if key == "fill": self.fill = AnimateColor(self.fill, (min(255, self.fill[0] * self.animation_scale), min(255, self.fill[1] * self.animation_scale), min(255, self.fill[2] * self.animation_scale)), self.animation_duration, self.animation_curve)
            if key == "text_color": self.text_color = AnimateColor(self.text_color, (min(255, self.text_color[0] * self.animation_scale), min(255, self.text_color[1] * self.animation_scale), min(255, self.text_color[2] * self.animation_scale)), self.animation_duration, self.animation_curve)
            if key == "margin": self.margin = Animate(self.margin, self.margin * self.animation_scale, self.animation_duration, self.animation_curve)  # Is it necessary?
            if key == "width": self.width = Animate(self.width, self.width * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "outline_fill": self.outline_fill = AnimateColor(self.outline_fill, (min(255, self.outline_fill[0] * self.animation_scale), min(255, self.outline_fill[1] * self.animation_scale), min(255, self.outline_fill[2] * self.animation_scale)), self.animation_duration, self.animation_curve)

    def draw(self):
        coords = pgmenu.position.center_coords(self.size.inttuple, (*self.coords.inttuple, *self.size.basetuple))

        # Hopefully not definitive, but need to update rect
        self.rect = pygame.Rect(*coords, *self.size.inttuple)

        button_surface = pgmenu.draw.aarect(None, self.fill.color, (*coords, *self.size.inttuple), self.width.int, self.border_radius.int,
                                            self.border_top_left_radius.int, self.border_top_right_radius.int, self.border_bottom_left_radius.int,
                                            self.border_bottom_right_radius.int, self.antialiasing, self.transparency.int, self.aa_strength.int,
                                            inside_fill=self.inside_fill.color, inside_transparency=self.inside_transparency.int, inside_border_radius=self.inside_border_radius.int,
                                            inside_border_top_left_radius=self.inside_border_top_left_radius.int, inside_border_top_right_radius=self.inside_border_top_right_radius.int,
                                            inside_border_bottom_left_radius=self.inside_border_bottom_left_radius.int, inside_border_bottom_right_radius=self.inside_border_bottom_right_radius.int,
                                            inside_aa_strength=self.inside_aa_strength.int, inside_antialiasing=self.inside_antialiasing,
                                            debug=self.debug, force_only_overlay=self.force_only_overlay)

        # Icon
        if self.icon is not None:
            icon_surface = pgmenu.surface.resize(self.icon, (min(self.size.inttuple) - self.margin,)*2)

        # Get text and calculate new text_size
        text_surface = pgmenu.text.fit_text(self.text, self.text_font, self.text_color.color, self.size.inttuple,
                                            self.margin.int, self.text_background, self.text_antialias, self.text_italic, self.text_bold, self.text_strikethrough,
                                            self.text_underline, self.text_transparency.int)

        text_coords = pgmenu.position.center_coords(text_surface.get_size(), (0, 0, *self.size.inttuple))

        self.surface.blit(button_surface, coords)

        self.surface.blit(text_surface, (text_coords[0] + coords[0], text_coords[1] + coords[1]))

    def update(self, event):
        # Detect mouse collisions
        if self.state == pgmenu.HOVERED or self.state == pgmenu.ACTIVE:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.state = pgmenu.ACTIVE
                    self.on_press()
                    self.animation_on_press()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.on_release()
                    self.animation_on_release()

    def m_animation_on_standby(self):
        if not self.no_animation:
            self.size.backward()
            self.size.update()

            self.border_radii.backward()
            self.border_radii.update()

            self.fill.backward()
            self.fill.update()

    def m_animation_on_hover(self):
        if not self.no_animation:
            self.size.forward()
            self.size.update()

            self.border_radii.forward()
            self.border_radii.update()

            self.fill.forward()
            self.fill.update()

    def m_on_release(self):
        print('Button pressed')

    def request_cursor(self):
        pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_HAND
