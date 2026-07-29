import pygame
import pgmenu

from pgmenu.animation import *
from pgmenu.constants import THEME
from pgmenu.theme import resolve, resolve_kwarg, resolve_widget


# TODO -> Class RectWidget: inner_radii are probably not getting updated when inner_border_radius is

# TODO -> Can't assign border_radii in theme because of the current system


# Adds widget to the system and update loop
def add(widget):
    # Sets Frame objects at the end of the draw order so other surfaces have time to blit on to them
    def frame_handling():
        for i in range(len(pgmenu.vars.widgets_draw_order)):
            if pgmenu.vars.widgets_draw_order[i].type == pgmenu.FRAME:
                pgmenu.vars.widgets_draw_order.insert(i, widget)
                return

        pgmenu.vars.widgets_draw_order.append(widget)

    if widget.type == pgmenu.FRAME:
        frame_handling()
    else:
        pgmenu.vars.widgets_draw_order.append(widget)

    pgmenu.vars.widgets.append(widget)


# TODO -> Add .place() method referencing position.py in here? Or .grid()?
class Widget:

    def __init__(self,
                 **kwargs):
        # self.type should be defined before calling super().__init__(), if not, defaults to WIDGET
        self.type = getattr(self, "type") if hasattr(self, "type") else pgmenu.WIDGET
        # Set animation attributes to theme according to widget type
        self.animation_scale = resolve_widget(kwargs, 'animation_scale', self.type, pgmenu.Theme.widget_animation_scale)
        self.animation_duration = resolve_widget(kwargs, 'animation_duration', self.type, pgmenu.Theme.widget_animation_duration)
        self.animation_curve = resolve_widget(kwargs, 'animation_curve', self.type, pgmenu.Theme.widget_animation_curve)
        # Disable animation
        self.disable_animation = resolve_widget(kwargs, 'disable_animation', self.type, pgmenu.Theme.widget_disable_animation)
        # No need to define attr in DEFAULT theme, as an absence of theme attr goes to default in resolve_widget
        self.animation_on_standby = resolve_widget(kwargs, 'animation_on_standby', self.type, self.m_animation_on_standby)
        self.animation_on_hover = resolve_widget(kwargs, 'animation_on_hover', self.type, self.m_animation_on_hover)
        self.animation_on_press = resolve_widget(kwargs, 'animation_on_press', self.type, self.m_animation_on_press)
        self.animation_on_hold = resolve_widget(kwargs, 'animation_on_hold', self.type, self.m_animation_on_hold)
        self.animation_on_release = resolve_widget(kwargs, 'animation_on_release', self.type, self.m_animation_on_release)
        self.animation_on_key_press = resolve_widget(kwargs, 'animation_on_key_press', self.type, self.m_animation_on_key_press)
        self.animation_on_key_hold = resolve_widget(kwargs, 'animation_on_key_hold', self.type, self.m_animation_on_key_hold)
        self.animation_on_key_release = resolve_widget(kwargs, 'animation_on_key_release', self.type, self.m_animation_on_key_release)
        # Set action attributes to theme according to widget type
        # No need to define attr in DEFAULT theme, as an absence of theme attr goes to default in resolve_widget
        self.on_standby = resolve_widget(kwargs, 'on_standby', self.type, self.m_on_standby)
        self.on_hover = resolve_widget(kwargs, 'on_hover', self.type, self.m_on_hover)
        self.on_press = resolve_widget(kwargs, 'on_press', self.type, self.m_on_press)
        self.on_hold = resolve_widget(kwargs, 'on_hold', self.type, self.m_on_hold)
        self.on_release = resolve_widget(kwargs, 'on_release', self.type, self.m_on_release)
        self.on_key_press = resolve_widget(kwargs, 'on_key_press', self.type, self.m_on_key_press)
        self.on_key_hold = resolve_widget(kwargs, 'on_key_hold', self.type, self.m_on_key_hold)
        self.on_key_release = resolve_widget(kwargs, 'on_key_release', self.type, self.m_on_key_release)
        self.on_resize = resolve_widget(kwargs, 'on_resize', self.type, self.m_on_resize)
        # Formatting for responsive resize
        # Responsive resize values have to be the same for all widgets
        self.responsive_size = kwargs.get('responsive_size', pgmenu.Theme.widget_responsive_size)
        self.responsive_size_w = kwargs.get('responsive_size_w', pgmenu.Theme.widget_responsive_size_w)
        self.responsive_size_h = kwargs.get('responsive_size_h', pgmenu.Theme.widget_responsive_size_h)
        self.responsive_coords = kwargs.get('responsive_coords', pgmenu.Theme.widget_responsive_coords)
        self.responsive_coords_x = kwargs.get('responsive_coords_x', pgmenu.Theme.widget_responsive_coords_x)
        self.responsive_coords_y = kwargs.get('responsive_coords_y', pgmenu.Theme.widget_responsive_coords_y)
        # Base widget should be able to be enabled and disabled, but could be removed later
        self.state = kwargs.get('state', pgmenu.Theme.widget_state)
        # Detection rect for update; no detection zone by default
        self.rect = pygame.Rect(0, 0, 0, 0)
        # Base attributes that have to be defined for a widget
        # master is included, but has to be defined by the widget
        self.size = (0, 0)
        self.coords = (0, 0)
        # The widget's size on screen, updated when drawn
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface_size = (0, 0)
        # Internal attributes used in responsive resize
        self.base_size = None
        self.base_coords = None
        # If widget is part of draw priority
        self.has_draw_priority = False
        # Save widget's drawn state
        self._drawn = False

    def get_type(self):
        return self.type

    def get_animation_scale(self):
        return self.animation_scale

    def get_animation_duration(self):
        return self.animation_duration

    def get_animation_curve(self):
        return self.animation_curve

    def get_disable_animation(self):
        return self.disable_animation

    def get_animation_on_standby(self):
        return self.animation_on_standby

    def get_animation_on_hover(self):
        return self.animation_on_hover

    def get_animation_on_press(self):
        return self.animation_on_press

    def get_animation_on_hold(self):
        return self.animation_on_hold

    def get_animation_on_release(self):
        return self.animation_on_release

    def get_animation_on_key_press(self):
        return self.animation_on_key_press

    def get_animation_on_key_hold(self):
        return self.animation_on_key_hold

    def get_animation_on_key_release(self):
        return self.animation_on_key_release

    def get_on_standby(self):
        return self.on_standby

    def get_on_hover(self):
        return self.on_hover

    def get_on_press(self):
        return self.on_press

    def get_on_hold(self):
        return self.on_hold

    def get_on_release(self):
        return self.on_release

    def get_on_key_press(self):
        return self.on_key_press

    def get_on_key_hold(self):
        return self.on_key_hold

    def get_on_key_release(self):
        return self.on_key_release

    def get_on_resize(self):
        return self.on_resize

    def get_responsive_size(self):
        return self.responsive_size

    def get_responsive_size_w(self):
        return self.responsive_size_w

    def get_responsive_size_h(self):
        return self.responsive_size_h

    def get_responsive_coords(self):
        return self.responsive_coords

    def get_responsive_coords_x(self):
        return self.responsive_coords_x

    def get_responsive_coords_y(self):
        return self.responsive_coords_y

    def get_state(self):
        return self.state

    def get_rect(self):
        return self.rect

    def get_size(self):
        return self.size

    def get_coords(self):
        return self.coords

    def get_surface_size(self):
        return self.surface_size

    def get_base_size(self):
        return self.base_size

    def get_base_coords(self):
        return self.base_coords

    def get_has_draw_priority(self):
        return self.has_draw_priority

    def __setattr__(self, key, value):
        # Prevent redefining animations if it's the same value
        if hasattr(self, key):
            attr = getattr(self, key)
            if isinstance(attr, pgmenu.animation.AnimateType):

                if attr.base_value == value:
                    return

        # Create animation
        if not isinstance(value, pgmenu.animation.AnimateType):
            # Don't run the animation run if the animation attributes aren't initialized yet
            if not hasattr(self, 'animation_scale') or not hasattr(self, 'animation_duration') or not hasattr(self, 'animation_curve'):
                pass

            # Only allow Surface widget's surface to get animations
            elif key == "surface" and hasattr(self, "type") and self.type != pgmenu.SURFACE:
                pass

            # Check if value is a supported type in animation (int, float, tuple, list, pygame.Surface)
            # bool is also an int (0 or 1) but we don't want it to be animated
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                value = Animate(value, value * self.animation_scale, self.animation_duration, self.animation_curve)

            elif isinstance(value, (tuple, list)) and all(isinstance(val, (int, float)) for val in value):
                pairs = [(base, base * self.animation_scale) for base in value]
                value = AnimateTuple(*pairs, duration=self.animation_duration, curve=self.animation_curve)

            # Only update surface if it's not a master surface
            elif isinstance(value, pygame.Surface) and key != "master":

                final_alpha = min(100 * self.animation_scale, 255)

                overlay = pygame.Surface(value.get_size(), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, final_alpha))

                final_surface = value.copy()
                final_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

                value = AnimateSurface(value, final_surface, 0, final_alpha, self.animation_duration, self.animation_curve)

        super().__setattr__(key, value)

        if key == "master":
            if value is not pygame.display.get_surface() and not isinstance(value, pgmenu.frame.Frame):
                raise ValueError("master attribute must be a display Surface or a Frame object.")

            if isinstance(value, pgmenu.frame.Frame):
                value.add(self)

            # Internal modified size in resize for all widgets -> Useful in resize logic, can't be updated during resize logic, only through user input
        if key in ("size", "coords") and not pgmenu.vars.videoresized:
            setattr(self, f"base_{key}", value)

    def _update_rect(self, size, coords):
        if isinstance(self.master, pgmenu.frame.Frame):
            size = min(self.master.size[0] - coords[0], size[0]), min(self.master.size[1] - coords[1], size[1])
            coords = self.master.coords[0] + coords[0], self.master.coords[1] + coords[1]

        self.rect = pygame.Rect(*coords, *size)

    def _make_2d(self, value):
        if isinstance(value, AnimateType):
            value = value.value

        if not isinstance(value, (tuple, list)):
            return value, value
        else:
            return value

    def _get_2d(self, key):
        if not hasattr(self, key):
            return None

        attr = getattr(self, key)

        return self._make_2d(attr)

    def get_2d_size(self):
        return self._get_2d("size")

    def get_2d_base_size(self):
        return self._get_2d("base_size")

    # Method allows to modify multiple attributes at a time
    def modify(self,
               **kwargs):
        for args in kwargs:
            self.__setattr__(args, kwargs[args])

    def draw(self):
        # Makes sure a widget not drawn doesn't update
        self._drawn = True

    def update(self, event):
        self.surface_size = self.surface.get_size()
        self._update_rect(self.surface_size, self.coords)

    def resize(self, w, h):
        ...

    def m_animation_on_standby(self):
        ...

    def m_animation_on_hover(self):
        ...

    def m_animation_on_press(self):
        ...

    def m_animation_on_hold(self):
        ...

    def m_animation_on_release(self):
        ...

    def m_animation_on_key_press(self, key):
        ...

    def m_animation_on_key_hold(self):
        ...

    def m_animation_on_key_release(self, key):
        ...

    def m_on_standby(self):
        ...

    def m_on_hover(self):
        ...

    def m_on_press(self):
        ...

    def m_on_hold(self):
        ...

    def m_on_release(self):
        ...

    def m_on_key_press(self, key):
        ...

    def m_on_key_hold(self, key):
        ...

    def m_on_key_release(self, key):
        ...

    def m_on_resize(self):
        ...

    def request_cursor(self):
        ...


class RectWidget(Widget):

    def __init__(self,
                 **kwargs):
        super().__init__(**kwargs)

        # Resize attributes
        self.base_border_radius = None
        self.base_border_top_left_radius = None
        self.base_border_top_right_radius = None
        self.base_border_bottom_left_radius = None
        self.base_border_bottom_right_radius = None

        # Defined afterward in normal widget class, this it to appease syntaxing
        self.border_radius = None

        self.border_top_left_radius = resolve_widget(kwargs, 'border_top_left_radius', self.type)
        self.border_top_right_radius = resolve_widget(kwargs, 'border_top_right_radius', self.type)
        self.border_bottom_left_radius = resolve_widget(kwargs, 'border_bottom_left_radius', self.type)
        self.border_bottom_right_radius = resolve_widget(kwargs, 'border_bottom_right_radius', self.type)

        self.antialiasing = resolve_widget(kwargs, 'antialiasing', self.type, pgmenu.Theme.rectwidget_antialiasing)
        self.transparency = resolve_widget(kwargs, 'transparency', self.type, pgmenu.Theme.rectwidget_transparency)
        self.aa_strength = resolve_widget(kwargs, 'aa_strength', self.type, pgmenu.Theme.rectwidget_aa_strength)

        self.inner_fill = resolve_widget(kwargs, 'inner_fill', self.type, pgmenu.UNSET)
        self.inner_transparency = resolve_widget(kwargs, 'inner_transparency', self.type, pgmenu.UNSET)
        self.inner_aa_strength = resolve_widget(kwargs, 'inner_aa_strength', self.type, pgmenu.UNSET)
        self.inner_antialiasing = resolve_widget(kwargs, 'inner_antialiasing', self.type, pgmenu.UNSET)

    def get_base_border_radius(self):
        return self.base_border_radius

    def get_base_border_top_left_radius(self):
        return self.base_border_top_left_radius

    def get_base_border_top_right_radius(self):
        return self.base_border_top_right_radius

    def get_base_border_bottom_left_radius(self):
        return self.base_border_bottom_left_radius

    def get_base_border_bottom_right_radius(self):
        return self.base_border_bottom_right_radius

    def get_border_radius(self):
        return self.border_radius

    def get_border_top_left_radius(self):
        return self.border_top_left_radius

    def get_border_top_right_radius(self):
        return self.border_top_right_radius

    def get_border_bottom_left_radius(self):
        return self.border_bottom_left_radius

    def get_border_bottom_right_radius(self):
        return self.border_bottom_right_radius

    def get_antialiasing(self):
        return self.antialiasing

    def get_transparency(self):
        return self.transparency

    def get_aa_strength(self):
        return self.aa_strength

    def get_inner_fill(self):
        return self.inner_fill

    def get_inner_transparency(self):
        return self.inner_transparency

    def get_inner_aa_strength(self):
        return self.inner_aa_strength

    def get_inner_antialiasing(self):
        return self.inner_antialiasing

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        if key in ("border_radius", "border_top_left_radius", "border_top_right_radius", "border_bottom_left_radius", "border_bottom_right_radius") and not pgmenu.vars.videoresized:
            setattr(self, f"base_{key}", value)

    def _resize_border_radii(self, w, h):
        factor = min(w / self.base_size[0], h / self.base_size[1])

        self.border_radius = round(self.base_border_radius * factor) if self.border_radius is not None else None
        self.border_top_left_radius = round(self.base_border_top_left_radius * factor) if self.border_top_left_radius is not None else None
        self.border_top_right_radius = round(self.base_border_top_right_radius * factor) if self.border_top_right_radius is not None else None
        self.border_bottom_left_radius = round(self.base_border_bottom_left_radius * factor) if self.border_bottom_left_radius is not None else None
        self.border_bottom_right_radius = round(self.base_border_bottom_right_radius * factor) if self.border_bottom_right_radius is not None else None

    def _animation_update_border_radii(self, direction=pgmenu.FORWARD, reach=1):
        self.border_radius.update(direction, reach) if self.border_radius is not None else None
        self.border_top_left_radius.update(direction, reach) if self.border_top_left_radius is not None else None
        self.border_top_right_radius.update(direction, reach) if self.border_top_right_radius is not None else None
        self.border_bottom_left_radius.update(direction, reach) if self.border_bottom_left_radius is not None else None
        self.border_bottom_right_radius.update(direction, reach) if self.border_bottom_right_radius is not None else None