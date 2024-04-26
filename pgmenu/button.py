# Clean version

from typing import Callable
import math

import pygame

import pgmenu
from pgmenu.widget import Widget
from pgmenu.animation import Animate, AnimateTuple, AnimateColor, circ
from pgmenu.animation import *


# TODO -> Add icon

# TODO -> Handle fill and inside_fill switching when width or inside_fill

# TODO -> Remake theme, doesn't format correctly

# TODO -> Make theme dynamic!!

# TODO -> Color animation: other argument for secondary color?

# TODO -> Problem for fill with animation -> can be else than color, like surface, but I need to call fill.color


class Button(Widget):

    # Argument of value None represents the user has not modified it
    def __init__(self,
                 surface: pygame.Surface,
                 coords: tuple[int, int] = (10, 10),
                 size: tuple[int, int] = (100, 30),
                 fill: tuple[int, int, int] | pygame.Surface = None,
                 icon: pygame.Surface = None,
                 text: str = "Button",
                 text_font: str = None,
                 text_color: tuple[int, int, int] = None,
                 text_margin: int = None,
                 width: int = None,
                 outline_fill: tuple[int, int, int] | pygame.Surface = None,
                 border_radius: int = None,  # ! Need to be able to modify in theme
                 animation_scale: float = 1.2,
                 animation_duration: float = 0.1,
                 animation_curve: Callable = circ,
                 on_standby: Callable = None,
                 on_hover: Callable = None,
                 on_press: Callable = None,
                 on_release: Callable = None,
                 **kwargs):

        # Animation
        self.animation_scale = animation_scale
        self.animation_duration = animation_duration
        self.animation_curve = animation_curve

        self.surface = surface
        self.coords = coords
        self.size = size
        self.fill = fill if fill is not None else pgmenu.vars.Theme.fill
        self.icon = icon
        self.text = text
        self.text_font = text_font if text_font is not None else pgmenu.vars.Theme.text_font
        self.text_color = text_color if text_color is not None else pgmenu.vars.Theme.text_color
        self.text_margin = text_margin if text_margin is not None else round(min(self.size.tuple) * 0.1)
        self.width = width if width is not None else pgmenu.vars.Theme.width
        self.outline_fill = outline_fill if outline_fill is not None else pgmenu.vars.Theme.outline_fill
        # Border radius is taken care of in widget
        self.on_standby = on_standby if on_standby is not None else self.m_on_standby
        self.on_hover = on_hover if on_hover is not None else self.m_on_hover
        self.on_press = on_press if on_press is not None else self.m_on_press
        self.on_release = on_release if on_release is not None else self.m_on_release

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
        if not isinstance(getattr(self, key), Animate) and not isinstance(getattr(self, key), AnimateTuple) and not isinstance(getattr(self, key), AnimateColor) and getattr(self, key) is not None:
            if key == "coords": self.coords = AnimateTuple((self.coords[0], self.coords[0] * self.animation_scale), (self.coords[1], self.coords[1] * self.animation_scale), duration=self.animation_duration, curve=self.animation_curve)
            if key == "size": self.size = AnimateTuple((self.size[0], self.size[0] * self.animation_scale), (self.size[1], self.size[1] * self.animation_scale), duration=self.animation_duration, curve=self.animation_curve)
            if key == "fill": self.fill = AnimateColor(self.fill, (min(255, self.fill[0] * self.animation_scale), min(255, self.fill[1] * self.animation_scale), min(255, self.fill[2] * self.animation_scale)), self.animation_duration, self.animation_curve)
            if key == "text_color": self.text_color = AnimateColor(self.text_color, (min(255, self.text_color[0] * self.animation_scale), min(255, self.text_color[1] * self.animation_scale), min(255, self.text_color[2] * self.animation_scale)), self.animation_duration, self.animation_curve)
            if key == "text_margin": self.text_margin = Animate(self.text_margin, self.text_margin * self.animation_scale, self.animation_duration, self.animation_curve)  # Is it necessary?
            if key == "width": self.width = Animate(self.width, self.width * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "outline_fill": self.outline_fill = AnimateColor(self.outline_fill, (min(255, self.outline_fill[0] * self.animation_scale), min(255, self.outline_fill[1] * self.animation_scale), min(255, self.outline_fill[2] * self.animation_scale)), self.animation_duration, self.animation_curve)

        # Rect requires special checks since it requires two attributes
        # Check type to make format rect after coords and size have been attributed animations
        # TODO -> Maybe try to remove key == "rect", can lead to errors
        if key == "rect" or (key == "coords" and isinstance(self.coords, AnimateTuple) and hasattr(self, "size")) or (key == "size" and isinstance(self.size, AnimateTuple) and hasattr(self, "coords")):
            self.rect = pygame.Rect(*self.coords.tuple, *self.size.tuple)

    def draw(self):
        coord_x, coord_y = self.coords.inttuple
        size_x, size_y = self.size.inttuple
        base_size_x, base_size_y = self.size.basetuple

        coords = pgmenu.position.center_coords((size_x, size_y), (coord_x, coord_y, base_size_x, base_size_y))

        button_surface = pgmenu.draw.aarect(None, self.fill.color, (coord_x, coord_y, size_x, size_y), self.width.int, self.border_radius.int,
                                            self.border_top_left_radius.int, self.border_top_right_radius.int, self.border_bottom_left_radius.int,
                                            self.border_bottom_right_radius.int, self.antialiasing, self.transparency.int, self.aa_strength.int,
                                            inside_fill=self.inside_fill.color, inside_transparency=self.inside_transparency.int, inside_border_radius=self.inside_border_radius.int,
                                            inside_border_top_left_radius=self.inside_border_top_left_radius.int, inside_border_top_right_radius=self.inside_border_top_right_radius.int,
                                            inside_border_bottom_left_radius=self.inside_border_bottom_left_radius.int, inside_border_bottom_right_radius=self.inside_border_bottom_right_radius.int,
                                            inside_aa_strength=self.inside_aa_strength.int, inside_antialiasing=self.inside_antialiasing,
                                            debug=self.debug, force_only_overlay=self.force_only_overlay)

        # Get text and calculate new text_size
        text_surface = pgmenu.text.fit_text(self.text, self.text_font, self.text_color.color, (size_x, size_y),
                                            self.text_margin.int, self.text_background, self.text_antialias, self.text_italic, self.text_bold, self.text_strikethrough,
                                            self.text_underline)

        text_coords = pgmenu.position.center_coords(text_surface.get_size(), (0, 0, size_x, size_y))

        button_surface.blit(text_surface, text_coords)

        self.surface.blit(button_surface, coords)

        return button_surface

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

    def m_on_standby(self):
        ...

    def m_on_hover(self):
        ...

    def m_on_press(self):
        print('Button pressed')

    def request_cursor(self):
        pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_HAND
