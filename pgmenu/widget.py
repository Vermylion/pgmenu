import pygame
import pgmenu

from pgmenu.animation import Animate, AnimateColor, AnimateTuple, AnimateMultiple


class Widget:

    def __init__(self,
                 border_radius,
                 **kwargs):
        # kwargs aarect arguments
        self.border_radius = border_radius if border_radius is not None else round(min(self.size.tuple) / 3)  # if border_radius is not None else pgmenu.vars.Theme.border_radius TODO -> Change with theme
        self.border_top_left_radius = kwargs['border_top_left_radius'] if 'border_top_left_radius' in kwargs else self.border_radius.int
        self.border_top_right_radius = kwargs['border_top_right_radius'] if 'border_top_right_radius' in kwargs else self.border_radius.int
        self.border_bottom_left_radius = kwargs['border_bottom_left_radius'] if 'border_bottom_left_radius' in kwargs else self.border_radius.int
        self.border_bottom_right_radius = kwargs['border_bottom_right_radius'] if 'border_bottom_right_radius' in kwargs else self.border_radius.int
        self.antialiasing = kwargs['antialiasing'] if 'antialiasing' in kwargs else True
        self.transparency = kwargs['transparency'] if 'transparency' in kwargs else 255
        self.aa_strength = kwargs['aas_strength'] if 'aa_strength' in kwargs else 1
        # Additional parameters for modifying inside rect
        self.inside_fill = kwargs['inside_fill'] if 'inside_fill' in kwargs else self.fill.color
        self.inside_transparency = kwargs['inside_transparency'] if 'inside_transparency' in kwargs else self.transparency
        self.inside_border_radius = kwargs['inside_border_radius'] if 'inside_border_radius' in kwargs else self.border_radius.int
        self.inside_border_top_left_radius = kwargs['inside_border_top_left_radius'] if 'inside_border_top_left_radius' in kwargs else self.inside_border_radius
        self.inside_border_top_right_radius = kwargs['inside_border_top_right_radius'] if 'inside_border_top_right_radius' in kwargs else self.inside_border_radius
        self.inside_border_bottom_left_radius = kwargs['inside_border_bottom_left_radius'] if 'inside_border_bottom_left_radius' in kwargs else self.inside_border_radius
        self.inside_border_bottom_right_radius = kwargs['inside_border_bottom_right_radius'] if 'inside_border_bottom_right_radius' in kwargs else self.inside_border_radius
        self.inside_aa_strength = kwargs['inside_aa_strength'] if 'inside_aa_strength' in kwargs else self.aa_strength
        self.inside_antialiasing = kwargs['inside_antialiasing'] if 'inside_antialiasing' in kwargs else self.antialiasing
        # Additional parameters
        self.debug = kwargs['debug'] if 'debug' in kwargs else True
        self.force_only_overlay = kwargs['force_only_overlay'] if 'force_only_overlay' in kwargs else False
        # kwargs text arguments
        self.text_background = kwargs['text_background'] if 'text_background' in kwargs else None
        self.text_antialias = kwargs['text_antialias'] if 'text_antialias' in kwargs else True
        self.text_italic = kwargs['text_italic'] if 'text_italic' in kwargs else False
        self.text_bold = kwargs['text_bold'] if 'text_bold' in kwargs else False
        self.text_strikethrough = kwargs['text_strikethrough'] if 'text_strikethrough' in kwargs else False
        self.text_underline = kwargs['text_underline'] if 'text_underline' in kwargs else False
        # kwargs animation arguments
        self.no_animation = kwargs['no_animation'] if 'no_animation' in kwargs else False
        # kwargs update event animation arguments
        self.animation_on_standby = kwargs['animation_on_standby'] if 'animation_on_standby' in kwargs else self.m_animation_on_standby
        self.animation_on_hover = kwargs['animation_on_hover'] if 'animation_on_hover' in kwargs else self.m_animation_on_hover
        self.animation_on_press = kwargs['animation_on_press'] if 'animation_on_press' in kwargs else self.m_animation_on_press
        self.animation_on_release = kwargs['animation_on_release'] if 'animation_on_release' in kwargs else self.m_animation_on_release
        self.animation_on_key_press = kwargs['animation_on_key_press'] if 'animation_on_key_press' in kwargs else self.m_animation_on_key_press
        self.animation_on_key_release = kwargs['animation_on_key_release'] if 'animation_on_key_release' in kwargs else self.m_animation_on_key_release
        # kwargs update event arguments
        self.on_key_press = kwargs['on_key_press'] if 'on_key_press' in kwargs else self.m_on_key_press
        self.on_key_release = kwargs['on_key_release'] if 'on_key_release' in kwargs else self.m_on_key_release
        # kwargs core arguments
        self.state = kwargs['state'] if 'state' in kwargs else pgmenu.NORMAL
        # Core widget arguments
        self.rect = pygame.Rect
        # Random number to calibrate text_size correctly in calculate_text
        self.text_size = 10

        # Link together border_radii
        self.border_radii = AnimateMultiple(self.border_radius, self.border_top_left_radius, self.border_top_right_radius,
                                            self.border_bottom_left_radius, self.border_bottom_right_radius, self.inside_border_radius,
                                            self.inside_border_top_left_radius, self.inside_border_top_right_radius,
                                            self.inside_border_bottom_left_radius, self.inside_border_bottom_right_radius)

    def __setattr__(self, key, value):
        # Return if called with same value
        if hasattr(self, key) and getattr(self, key) == value:
            return False

        # Save current key's value to use for comparison later
        if hasattr(self, key): old_value = getattr(self, key)

        # Call the original __setattr__ method to set the attribute
        super().__setattr__(key, value)

        if key == "border_top_left_radius": print(value)

        # Animation Arguments
        if not isinstance(getattr(self, key), Animate) and not isinstance(getattr(self, key), AnimateTuple) and not isinstance(getattr(self, key), AnimateColor) and getattr(self, key) is not None:
            if key == "border_radius":
                self.border_radius = Animate(self.border_radius, self.border_radius * self.animation_scale, self.animation_duration, self.animation_curve)

                if hasattr(self, "border_top_left_radius") and self.border_top_left_radius == old_value: self.border_top_left_radius = Animate(self.border_top_left_radius, self.border_top_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "border_top_right_radius") and self.border_top_right_radius == old_value: self.border_top_right_radius = Animate(self.border_top_right_radius, self.border_top_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "border_bottom_left_radius") and self.border_bottom_left_radius == old_value: self.border_bottom_left_radius = Animate(self.border_bottom_left_radius, self.border_bottom_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "border_bottom_right_radius") and self.border_bottom_right_radius == old_value: self.border_bottom_right_radius = Animate(self.border_bottom_right_radius, self.border_bottom_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)

                if hasattr(self, "inside_border_radius") and self.inside_border_radius == old_value: self.inside_border_radius = Animate(self.inside_border_radius, self.inside_border_radius * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_top_left_radius") and self.inside_border_top_left_radius == old_value: self.inside_border_top_left_radius = Animate(self.inside_border_top_left_radius, self.inside_border_top_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_top_right_radius") and self.inside_border_top_right_radius == old_value: self.inside_border_top_right_radius = Animate(self.inside_border_top_right_radius, self.inside_border_top_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_bottom_left_radius") and self.inside_border_bottom_left_radius == old_value: self.inside_border_bottom_left_radius = Animate(self.inside_border_bottom_left_radius, self.inside_border_bottom_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
                if hasattr(self, "inside_border_bottom_right_radius") and self.inside_border_bottom_right_radius == old_value: self.border_bottom_right_radius = Animate(self.inside_border_bottom_right_radius, self.inside_border_bottom_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)

            if key == "border_top_left_radius": self.border_top_left_radius = Animate(self.border_top_left_radius, self.border_top_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "border_top_right_radius": self.border_top_right_radius = Animate(self.border_top_right_radius, self.border_top_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "border_bottom_left_radius": self.border_bottom_left_radius = Animate(self.border_bottom_left_radius, self.border_bottom_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "border_bottom_right_radius": self.border_bottom_right_radius = Animate(self.border_bottom_right_radius, self.border_bottom_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)

            if key == "inside_border_radius": self.inside_border_radius = Animate(self.inside_border_radius, self.inside_border_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_border_top_left_radius": self.inside_border_top_left_radius = Animate(self.inside_border_top_left_radius, self.inside_border_top_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_border_top_right_radius": self.inside_border_top_right_radius = Animate(self.inside_border_top_right_radius, self.inside_border_top_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_border_bottom_left_radius": self.inside_border_bottom_left_radius = Animate(self.inside_border_bottom_left_radius, self.inside_border_bottom_left_radius * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_border_bottom_right_radius": self.border_bottom_right_radius = Animate(self.inside_border_bottom_right_radius, self.inside_border_bottom_right_radius * self.animation_scale, self.animation_duration, self.animation_curve)

            if hasattr(self, "border_radii") and (key == "border_radius" or key == "border_top_left_radius" or key == "border_top_right_radius" or key == "border_bottom_left_radius" or key == "border_bottom_right_radius" or key == "inside_border_radius" or key == "inside_border_top_left_radius" or key == "inside_border_top_right_radius" or key == "inside_border_bottom_left_radius" or key == "inside_border_bottom_right_radius"):
                self.border_radii.modify(getattr(self, key))

            if key == "transparency": self.transparency = Animate(self.transparency, self.transparency * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "aa_strength": self.aa_strength = Animate(self.aa_strength, self.aa_strength * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_fill": self.inside_fill = AnimateColor(self.inside_fill, (min(255, self.inside_fill[0] * self.animation_scale), min(255, self.inside_fill[1] * self.animation_scale), min(255, self.inside_fill[2] * self.animation_scale)), self.animation_duration, self.animation_curve)
            if key == "inside_transparency": self.inside_transparency = Animate(self.inside_transparency, self.inside_transparency * self.animation_scale, self.animation_duration, self.animation_curve)
            if key == "inside_aa_strength": self.inside_aa_strength = Animate(self.inside_aa_strength, self.inside_aa_strength * self.animation_scale, self.animation_duration, self.animation_curve)

    def modify(self,
               **kwargs):
        for args in kwargs:
            setattr(self, args, kwargs[args])

    def draw(self):
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
