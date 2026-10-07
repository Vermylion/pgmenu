import pygame
import pgmenu

from pgmenu.core.animation import Animate, AnimateTuple, AnimateSurface, AnimateType
from pgmenu.core.theme import resolve, resolve_widget


__all__ = ["Widget"]


# TODO -> Add .place() method referencing position.py in here? Or .grid()?
class Widget:

    def __init__(self,
                 **kwargs):
        # Call to mixins if there are any
        self._mixin_hook("_mixin_init", **kwargs)

        # self.type should be defined before calling super().__init__(), if not, defaults to WIDGET
        self.set_type(pgmenu.WIDGET)
        # Set animation attributes to theme according to widget type
        self.animation_scale = resolve_widget(kwargs, 'animation_scale', self.type, pgmenu.Theme.widget_animation_scale)
        self.animation_duration = resolve_widget(kwargs, 'animation_duration', self.type, pgmenu.Theme.widget_animation_duration)
        self.animation_curve = resolve_widget(kwargs, 'animation_curve', self.type, pgmenu.Theme.widget_animation_curve)
        self.animation_precision = resolve_widget(kwargs, 'animation_precision', self.type, pgmenu.Theme.widget_animation_precision)
        # Disable animation
        self.disable_default_animation = resolve_widget(kwargs, 'disable_default_animation', self.type, pgmenu.Theme.widget_disable_default_animation)
        # No need to define attr in DEFAULT theme, as an absence of theme attr goes to default in resolve_widget
        self.animation_on_standby = resolve_widget(kwargs, 'animation_on_standby', self.type, self.m_animation_on_standby, pgmenu.AnimationTheme, self)
        self.animation_on_hover = resolve_widget(kwargs, 'animation_on_hover', self.type, self.m_animation_on_hover, pgmenu.AnimationTheme, self)
        self.animation_on_press = resolve_widget(kwargs, 'animation_on_press', self.type, self.m_animation_on_press, pgmenu.AnimationTheme, self)
        self.animation_on_hold = resolve_widget(kwargs, 'animation_on_hold', self.type, self.m_animation_on_hold, pgmenu.AnimationTheme, self)
        self.animation_on_active = resolve_widget(kwargs, 'animation_on_active', self.type, self.m_animation_on_active, pgmenu.AnimationTheme, self)
        self.animation_on_release = resolve_widget(kwargs, 'animation_on_release', self.type, self.m_animation_on_release, pgmenu.AnimationTheme, self)
        self.animation_on_select = resolve_widget(kwargs, 'animation_on_select', self.type, self.m_animation_on_select, pgmenu.AnimationTheme, self)
        self.animation_on_deselect = resolve_widget(kwargs, 'animation_on_deselect', self.type, self.m_animation_on_deselect, pgmenu.AnimationTheme, self)
        self.animation_on_key_press = resolve_widget(kwargs, 'animation_on_key_press', self.type, self.m_animation_on_key_press, pgmenu.AnimationTheme, self)
        self.animation_on_key_hold = resolve_widget(kwargs, 'animation_on_key_hold', self.type, self.m_animation_on_key_hold, pgmenu.AnimationTheme, self)
        self.animation_on_key_release = resolve_widget(kwargs, 'animation_on_key_release', self.type, self.m_animation_on_key_release, pgmenu.AnimationTheme, self)
        # Set action attributes to theme according to widget type
        # No need to define attr in DEFAULT theme, as an absence of theme attr goes to default in resolve_widget
        self.on_standby = resolve_widget(kwargs, 'on_standby', self.type, self.m_on_standby)
        self.on_hover = resolve_widget(kwargs, 'on_hover', self.type, self.m_on_hover)
        self.on_press = resolve_widget(kwargs, 'on_press', self.type, self.m_on_press)
        self.on_hold = resolve_widget(kwargs, 'on_hold', self.type, self.m_on_hold)
        self.on_active = resolve_widget(kwargs, 'on_active', self.type, self.m_on_active)
        self.on_release = resolve_widget(kwargs, 'on_release', self.type, self.m_on_release)
        self.on_select = resolve_widget(kwargs, 'on_select', self.type, self.m_on_select)
        self.on_deselect = resolve_widget(kwargs, 'on_deselect', self.type, self.m_on_deselect)
        self.on_key_press = resolve_widget(kwargs, 'on_key_press', self.type, self.m_on_key_press)
        self.on_key_hold = resolve_widget(kwargs, 'on_key_hold', self.type, self.m_on_key_hold)
        self.on_key_release = resolve_widget(kwargs, 'on_key_release', self.type, self.m_on_key_release)
        self.on_resize = resolve_widget(kwargs, 'on_resize', self.type, self.m_on_resize)
        # Base hover cursor for the widget
        self.cursor = resolve_widget(kwargs, 'cursor', self.type, pygame.SYSTEM_CURSOR_ARROW)
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
        self.base_margin = None
        # If widget is part of draw priority
        self.has_draw_priority = False
        # Save widget's drawn state
        self._drawn = False

    def __setattr__(self, key, value):

        # Prevent redefining animations if it's the same value
        if hasattr(self, key):
            attr = getattr(self, key)
            if isinstance(attr, AnimateType) and not isinstance(value, AnimateType):

                if attr.base_value == value:
                    return

        # Create animation
        if not isinstance(value, AnimateType):
            # Don't run the animation run if the animation attributes aren't initialized yet
            if not hasattr(self, 'animation_scale') or not hasattr(self, 'animation_duration') or not hasattr(self, 'animation_curve') or not hasattr(self, 'animation_precision'):
                pass

            # Don't animate the cursor value
            elif key == "cursor":
                pass

            # Only allow Surface widget's surface to get animations
            elif key == "surface" and hasattr(self, "type") and self.type != pgmenu.SURFACE:
                pass

            # Check if value is a supported type in animation (int, float, tuple, list, pygame.Surface)
            # bool is also an int (0 or 1) but we don't want it to be animated
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                value = Animate(value, value * self.animation_scale, self.animation_duration, self.animation_curve, self.animation_precision)

            elif isinstance(value, (tuple, list)) and all(isinstance(val, (int, float)) for val in value):
                pairs = [(v, v * self.animation_scale) for v in value]

                value = AnimateTuple(*pairs, duration=self.animation_duration, curve=self.animation_curve, precision=self.animation_precision)

            # Only update surface if it's not a master surface
            elif isinstance(value, pygame.Surface) and key != "master":

                final_alpha = min(100 * self.animation_scale, 255)

                overlay = pygame.Surface(value.get_size(), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, final_alpha))

                final_surface = value.copy()
                final_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

                value = AnimateSurface(value, final_surface, 0, final_alpha, self.animation_duration, self.animation_curve, self.animation_precision)

        super().__setattr__(key, value)

        if key == "master":
            if value is not pygame.display.get_surface() and not isinstance(value, pgmenu.widgets.Frame):
                raise ValueError("master attribute must be a display Surface or a Frame object.")

            if isinstance(value, pgmenu.widgets.Frame):
                value.add(self)

        # Internal modified size in resize for all widgets -> Useful in resize logic, can't be updated during resize logic, only through user input
        if key in ("size", "coords", "margin") and not pgmenu.vars.videoresized:
            setattr(self, f"base_{key}", value)

        # Hook to call __setattr__ functionality in mixins
        self._mixin_hook("_mixin_setattr", key, value)

    def _mixin_hook(self, hook: str, *params, **kwargs):
        for cls in type(self).__mro__[1:]:
            m_hook = cls.__dict__.get(hook)
            if m_hook:
                m_hook(self, *params, **kwargs)

    def _update_rect(self, size, coords):
        if isinstance(self.master, pgmenu.widgets.Frame):
            size = min(self.master.size[0] - coords[0], size[0]), min(self.master.size[1] - coords[1], size[1])
            coords = self.master.coords[0] + coords[0], self.master.coords[1] + coords[1]

        self.rect = pygame.Rect(*coords, *size)

    def _format_size(self, size):
        """
        :param size:
        :return:
        Function to format size to a tuple(size, size)
        """
        size = resolve(size, getattr(pgmenu.Theme, f'{self.type}_size', None))

        if isinstance(size, (int, float)):
            size = size, size

        elif isinstance(size, Animate):
            size = size.value, size.value

        return size

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

    def set_type(self, type):
        """
        :param type:
        :return:
        Sets type of widget to the passed type only if type wasn't assigned previously.
        """
        self.type = getattr(self, "type") if hasattr(self, "type") else type

    # Method allows to modify multiple attributes at a time
    def modify(self,
               **kwargs):
        for args in kwargs:
            self.__setattr__(args, kwargs[args])

    def draw(self):
        # Makes sure a widget not drawn doesn't update
        self._drawn = True

        # Default call for mixins
        self._mixin_hook("_mixin_draw")

    def update(self, event):
        self.surface_size = self.surface.get_size()
        self._update_rect(self.surface_size, self.coords)

        # Default call for mixins
        self._mixin_hook("_mixin_update", event)

    def destroy(self):
        """Remove this widget from the engine."""
        pgmenu.widgets.remove(self)

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

    def m_animation_on_active(self):
        ...

    def m_animation_on_select(self):
        ...

    def m_animation_on_deselect(self):
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

    def m_on_active(self):
        ...

    def m_on_select(self):
        ...

    def m_on_deselect(self):
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
        pgmenu.vars.widget_cursor = self.cursor
