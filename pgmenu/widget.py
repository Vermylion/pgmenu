import pygame
import pgmenu

from pgmenu.animation import *
from pgmenu.constants import THEME


# TODO -> Class RectWidget: inside_radii are probably not getting updated when inside_border_radius is

# TODO -> Can't assign border_radii in theme because of the current system


# Adds widget to the system and update loop
def add(widget):
    pgmenu.vars.widgets.append(widget)
    # Add to draw order
    pgmenu.vars.widgets_draw_order.append(widget)


class Widget:

    def __init__(self,
                 **kwargs):
        # Formatting for responsive resize
        self.responsive_size = kwargs['responsive_size'] if 'responsive_size' in kwargs else pgmenu.Theme.responsive_size
        self.responsive_size_w = kwargs['responsive_size_w'] if 'responsive_size_w' in kwargs else pgmenu.Theme.responsive_size_w
        self.responsive_size_h = kwargs['responsive_size_h'] if 'responsive_size_h' in kwargs else pgmenu.Theme.responsive_size_h
        self.responsive_coords = kwargs['responsive_coords'] if 'responsive_coords' in kwargs else pgmenu.Theme.responsive_coords
        self.responsive_coords_x = kwargs['responsive_coords_x'] if 'responsive_coords_x' in kwargs else pgmenu.Theme.responsive_coords_x
        self.responsive_coords_y = kwargs['responsive_coords_y'] if 'responsive_coords_y' in kwargs else pgmenu.Theme.responsive_coords_y
        # Base widget should be able to be enabled and disabled, but could be removed later
        self.state = kwargs['state'] if 'state' in kwargs else pgmenu.Theme.state
        # If widget is part of draw priority
        self.has_draw_priority = True
        # Save widget's drawn state
        self._drawn = False

    # Redundant function here, but could be used in the future
    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    def modify(self,
               **kwargs):
        for args in kwargs:
            setattr(self, args, kwargs[args])

    def draw(self):
        self._drawn = True

    def update(self, event):
        ...

    def m_animation_on_standby(self):
        ...

    def m_animation_on_hover(self):
        ...

    def m_animation_on_press(self):
        ...

    def m_animation_on_release(self):
        ...

    def m_animation_on_key_press(self, key):
        ...

    def m_animation_on_key_release(self, key):
        ...

    def m_on_standby(self):
        ...

    def m_on_hover(self):
        ...

    def m_on_press(self):
        ...

    def m_on_release(self):
        ...

    def m_on_key_press(self, key):
        ...

    def m_on_key_release(self, key):
        ...

    def move_draw_order(self, index):
        pgmenu.vars.widgets_draw_order.remove(self)
        pgmenu.vars.widgets_draw_order.insert(index, self)


class RectWidget(Widget):

    def __init__(self,
                 border_radius,
                 **kwargs):

        super().__init__(**kwargs)

        # kwargs aarect arguments
        # Has to be at top since it englobes all defined and not defined border attributes
        # Removed border_radius and inside_border_radius since they impact others, preventing low-level interactions
        self._border_radii = ["border_top_left_radius", "border_top_right_radius", "border_bottom_left_radius", "border_bottom_right_radius",
                              "inside_border_top_left_radius", "inside_border_top_right_radius", "inside_border_bottom_left_radius",
                              "inside_border_bottom_right_radius"]

        self.border_radius = border_radius if border_radius != THEME else pgmenu.Theme.border_radius # round(min(self.size.tuple) / 3)  # if border_radius is not None else pgmenu.vars.Theme.border_radius
        self.border_top_left_radius = kwargs['border_top_left_radius'] if 'border_top_left_radius' in kwargs else self.border_radius.int # pgmenu.Theme.border_top_left_radius
        self.border_top_right_radius = kwargs['border_top_right_radius'] if 'border_top_right_radius' in kwargs else self.border_radius.int # pgmenu.Theme.border_top_right_radius
        self.border_bottom_left_radius = kwargs['border_bottom_left_radius'] if 'border_bottom_left_radius' in kwargs else self.border_radius.int # pgmenu.Theme.border_bottom_left_radius
        self.border_bottom_right_radius = kwargs['border_bottom_right_radius'] if 'border_bottom_right_radius' in kwargs else self.border_radius.int # pgmenu.Theme.border_bottom_right_radius
        self.antialiasing = kwargs['antialiasing'] if 'antialiasing' in kwargs else pgmenu.Theme.antialiasing
        self.transparency = kwargs['transparency'] if 'transparency' in kwargs else pgmenu.Theme.transparency
        self.aa_strength = kwargs['aa_strength'] if 'aa_strength' in kwargs else pgmenu.Theme.aa_strength
        # Additional parameters for modifying inside rect
        # inside_fill is not used in button but could be used in other widgets
        self.inside_fill = kwargs['inside_fill'] if 'inside_fill' in kwargs else self.fill.value # pgmenu.Theme.inside_fill
        self.inside_transparency = kwargs['inside_transparency'] if 'inside_transparency' in kwargs else self.transparency.int # pgmenu.Theme.inside_transparency
        self.inside_border_radius = kwargs['inside_border_radius'] if 'inside_border_radius' in kwargs else self.border_radius.int # pgmenu.Theme.inside_border_radius
        self.inside_border_top_left_radius = kwargs['inside_border_top_left_radius'] if 'inside_border_top_left_radius' in kwargs else self.inside_border_radius.int # pgmenu.Theme.inside_border_top_left_radius
        self.inside_border_top_right_radius = kwargs['inside_border_top_right_radius'] if 'inside_border_top_right_radius' in kwargs else self.inside_border_radius.int # pgmenu.Theme.inside_border_top_right_radius
        self.inside_border_bottom_left_radius = kwargs['inside_border_bottom_left_radius'] if 'inside_border_bottom_left_radius' in kwargs else self.inside_border_radius.int # pgmenu.Theme.inside_border_bottom_left_radius
        self.inside_border_bottom_right_radius = kwargs['inside_border_bottom_right_radius'] if 'inside_border_bottom_right_radius' in kwargs else self.inside_border_radius.int # pgmenu.Theme.inside_border_bottom_right_radius
        self.inside_aa_strength = kwargs['inside_aa_strength'] if 'inside_aa_strength' in kwargs else pgmenu.Theme.inside_aa_strength # self.aa_strength.int
        self.inside_antialiasing = kwargs['inside_antialiasing'] if 'inside_antialiasing' in kwargs else self.antialiasing # pgmenu.Theme.inside_antialiasing
        # Additional parameters
        self.debug = kwargs['debug'] if 'debug' in kwargs else pgmenu.Theme.debug
        self.force_only_overlay = kwargs['force_only_overlay'] if 'force_only_overlay' in kwargs else pgmenu.Theme.force_only_overlay
        # kwargs text arguments
        self.text_background = kwargs['text_background'] if 'text_background' in kwargs else pgmenu.Theme.text_background
        self.text_antialias = kwargs['text_antialias'] if 'text_antialias' in kwargs else pgmenu.Theme.text_antialias
        self.text_italic = kwargs['text_italic'] if 'text_italic' in kwargs else pgmenu.Theme.text_italic
        self.text_bold = kwargs['text_bold'] if 'text_bold' in kwargs else pgmenu.Theme.text_bold
        self.text_strikethrough = kwargs['text_strikethrough'] if 'text_strikethrough' in kwargs else pgmenu.Theme.text_strikethrough
        self.text_underline = kwargs['text_underline'] if 'text_underline' in kwargs else pgmenu.Theme.text_underline
        self.text_transparency = kwargs['text_transparency'] if 'text_transparency' in kwargs else self.transparency.int # pgmenu.Theme.widget_text_transparency
        # kwargs animation arguments
        self.no_animation = kwargs['no_animation'] if 'no_animation' in kwargs else pgmenu.Theme.no_animation
        # kwargs update event animation arguments
        self.animation_on_standby = kwargs['animation_on_standby'] if 'animation_on_standby' in kwargs else self.m_animation_on_standby # pgmenu.Theme.animation_on_standby
        self.animation_on_hover = kwargs['animation_on_hover'] if 'animation_on_hover' in kwargs else self.m_animation_on_hover # pgmenu.Theme.animation_on_hover
        self.animation_on_press = kwargs['animation_on_press'] if 'animation_on_press' in kwargs else self.m_animation_on_press # pgmenu.Theme.animation_on_press
        self.animation_on_release = kwargs['animation_on_release'] if 'animation_on_release' in kwargs else self.m_animation_on_release # pgmenu.Theme.animation_on_release
        self.animation_on_key_press = kwargs['animation_on_key_press'] if 'animation_on_key_press' in kwargs else self.m_animation_on_key_press # pgmenu.Theme.animation_on_key_press
        self.animation_on_key_release = kwargs['animation_on_key_release'] if 'animation_on_key_release' in kwargs else self.m_animation_on_key_release # pgmenu.Theme.animation_on_key_release
        # kwargs update event arguments
        self.on_key_press = kwargs['on_key_press'] if 'on_key_press' in kwargs else self.m_on_key_press # pgmenu.Theme.on_key_press
        self.on_key_release = kwargs['on_key_release'] if 'on_key_release' in kwargs else self.m_on_key_release # pgmenu.Theme.on_key_release
        # kwargs core arguments
        # self.state = kwargs['state'] if 'state' in kwargs else pgmenu.Theme.state
        # Core widget arguments
        self.rect = pygame.Rect(0, 0, 0, 0)

        # Link together border_radii
        self.border_radii = AnimateMultiple(self.border_radius, self.border_top_left_radius, self.border_top_right_radius,
                                            self.border_bottom_left_radius, self.border_bottom_right_radius, self.inside_border_radius,
                                            self.inside_border_top_left_radius, self.inside_border_top_right_radius,
                                            self.inside_border_bottom_left_radius, self.inside_border_bottom_right_radius)

        # Link together transparencies
        self.transparencies = AnimateMultiple(self.transparency, self.inside_transparency, self.text_transparency)

    def __setattr__(self, key, value):
        # Return if called with same value
        if hasattr(self, key) and getattr(self, key) == value:
            return False

        # Save current key's value to use for comparison later
        if hasattr(self, key):
            old_value = getattr(self, key)

        # Call the original __setattr__ method to set the attribute
        super().__setattr__(key, value)

        # Animation Arguments
        if not isinstance(getattr(self, key), Animate | AnimateTuple | AnimateColor | AnimateFill) and getattr(self, key) is not None:
            if key == "border_radius":
                self.border_radius = Animate(self.border_radius, self.border_radius * self.animation_scale, self.animation_duration, self.animation_curve)

                # FIXME -> For some reason, old_value breaks with this loop
                # for border_radius in self._border_radii:
                #     if hasattr(self, border_radius) and getattr(self, border_radius).base_num == old_value.base_num: setattr(self, border_radius, Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve))

                if hasattr(self, "border_top_left_radius") and self.border_top_left_radius.base_num == old_value.base_num: self.border_top_left_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "border_top_right_radius") and self.border_top_right_radius.base_num == old_value.base_num: self.border_top_right_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "border_bottom_left_radius") and self.border_bottom_left_radius.base_num == old_value.base_num: self.border_bottom_left_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "border_bottom_right_radius") and self.border_bottom_right_radius.base_num == old_value.base_num: self.border_bottom_right_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)

                if hasattr(self, "inside_border_radius") and self.inside_border_radius.base_num == old_value.base_num: self.inside_border_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_top_left_radius") and self.inside_border_top_left_radius.base_num == old_value.base_num: self.inside_border_top_left_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_top_right_radius") and self.inside_border_top_right_radius.base_num == old_value.base_num: self.inside_border_top_right_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_bottom_left_radius") and self.inside_border_bottom_left_radius.base_num == old_value.base_num: self.inside_border_bottom_left_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_bottom_right_radius") and self.inside_border_bottom_right_radius.base_num == old_value.base_num: self.inside_border_bottom_right_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)

            if key == "inside_border_radius":
                self.inside_border_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)

                if hasattr(self, "inside_border_top_left_radius") and self.inside_border_top_left_radius.base_num == old_value.base_num: self.inside_border_top_left_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_top_right_radius") and self.inside_border_top_right_radius.base_num == old_value.base_num: self.inside_border_top_right_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_bottom_left_radius") and self.inside_border_bottom_left_radius.base_num == old_value.base_num: self.inside_border_bottom_left_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_bottom_right_radius") and self.inside_border_bottom_right_radius.base_num == old_value.base_num: self.inside_border_bottom_right_radius = Animate(self.border_radius.base_num, self.border_radius.base_num * self.animation_scale, self.animation_duration, self.animation_curve)

            if key == "border_top_left_radius": self.border_top_left_radius = Animate(self.border_top_left_radius, self.border_top_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "border_top_right_radius": self.border_top_right_radius = Animate(self.border_top_right_radius, self.border_top_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "border_bottom_left_radius": self.border_bottom_left_radius = Animate(self.border_bottom_left_radius, self.border_bottom_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "border_bottom_right_radius": self.border_bottom_right_radius = Animate(self.border_bottom_right_radius, self.border_bottom_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)

            if key == "inside_border_top_left_radius": self.inside_border_top_left_radius = Animate(self.inside_border_top_left_radius, self.inside_border_top_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_border_top_right_radius": self.inside_border_top_right_radius = Animate(self.inside_border_top_right_radius, self.inside_border_top_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_border_bottom_left_radius": self.inside_border_bottom_left_radius = Animate(self.inside_border_bottom_left_radius, self.inside_border_bottom_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_border_bottom_right_radius": self.inside_border_bottom_right_radius = Animate(self.inside_border_bottom_right_radius, self.inside_border_bottom_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)

            if key == "transparency":
                self.transparency = Animate(self.transparency, self.transparency * self.animation_scale, self.animation_duration, self.animation_curve)

                if hasattr(self, "inside_transparency") and self.inside_transparency.base_num == old_value.base_num: self.inside_transparency = Animate(self.transparency.base_num, self.transparency.base_num * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "text_transparency") and self.text_transparency.base_num == old_value.base_num: self.text_transparency = Animate(self.transparency.base_num, self.transparency.base_num * self.animation_scale, self.animation_duration, self.animation_curve)

            if key == "inside_transparency": self.inside_transparency = Animate(self.inside_transparency, self.inside_transparency * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "text_transparency": self.text_transparency = Animate(self.text_transparency, self.text_transparency * self.animation_scale, self.animation_duration, self.animation_curve)

            if key == "aa_strength": self.aa_strength = Animate(self.aa_strength, self.aa_strength * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_aa_strength": self.inside_aa_strength = Animate(self.inside_aa_strength, self.inside_aa_strength * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_fill": self._format_fill(key)

        elif key is not None:
            if hasattr(self, "border_radii") and (key == "border_radius" or key == "border_top_left_radius" or key == "border_top_right_radius" or key == "border_bottom_left_radius" or key == "border_bottom_right_radius" or key == "inside_border_radius" or key == "inside_border_top_left_radius" or key == "inside_border_top_right_radius" or key == "inside_border_bottom_left_radius" or key == "inside_border_bottom_right_radius"):
                self.border_radii.modify(getattr(self, key))

            if hasattr(self, "transparencies") and (key == "transparency" or key == "inside_transparency" or key == "text_transparency"):
                self.transparencies.modify(getattr(self, key))

    def _format_fill(self, fill_name):
        fill = getattr(self, fill_name)

        if isinstance(fill, pygame.Surface) or fill is None:
            # Don't have secondary fill argument yet
            final_fill = getattr(self, fill_name)
        else:
            final_fill = (min(255, fill[0] * self.animation_scale),
                          min(255, fill[1] * self.animation_scale),
                          min(255, fill[2] * self.animation_scale))

        fill = AnimateFill(fill, final_fill, self.animation_duration, self.animation_curve)
        setattr(self, fill_name, fill)

        return fill
