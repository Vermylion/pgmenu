import pygame
import pgmenu

from pgmenu.animation import *
from pgmenu.constants import THEME
from pgmenu.theme import resolve, resolve_kwarg, resolve_widget


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
        # Call to mixins if there are any
        self._init_mixins(kwargs)

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

        # Hook to call __setattr__ functionality in mixins
        for cls in type(self).__mro__:
            hook = cls.__dict__.get("_mixin_setattr_hook")
            if hook:
                hook(self, key, value)

    def _init_mixins(self, kwargs):
        seen = set()
        for cls in type(self).__mro__[1:]:
            init = cls.__dict__.get("_mixin_init")
            if init and init not in seen:
                seen.add(init)
                init(self, kwargs)

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

# Only fully dynamic Mixin
# FIXME -> Should all Mixins be fully dynamic?
# TODO -> Review/revamp code as it was mostly AI written
# FIXME -> For now, border_radius has to be set manually
# FIXME -> Make it work better; less hassle and simpler
class RectMixin:

    RECT_ATTRIBUTES = (
        "width",
        "border_radius",
        "border_top_left_radius",
        "border_top_right_radius",
        "border_bottom_left_radius",
        "border_bottom_right_radius",
        "antialiasing",
        "transparency",
        "aa_strength",
        "inner_fill",
        "inner_transparency",
        "inner_aa_strength",
        "inner_antialiasing",
    )

    BASE_RECT_ATTRIBUTES = (
        "border_radius",
        "border_top_left_radius",
        "border_top_right_radius",
        "border_bottom_left_radius",
        "border_bottom_right_radius",
    )

    def _mixin_init(self, kwargs):
        self._init_rect(kwargs)

    def _init_rect(self, kwargs, prefix=""):
        """
        Initializes a rectangle attribute group.

        Example:
            _init_rect(kwargs)
                -> border_radius

            _init_rect(kwargs, "check_")
                -> check_border_radius
        """

        # Base values used for responsive resizing
        for attr in self.BASE_RECT_ATTRIBUTES:
            setattr(self, f"base_{prefix}{attr}", None)

        for attr in self.RECT_ATTRIBUTES:

            default = pgmenu.UNSET if attr.startswith("inner_") else None

            # Theme defaults for normal rectangle properties
            if attr in ("antialiasing", "transparency", "aa_strength"):
                default = getattr(pgmenu.Theme, f"rectmixin_{attr}")

            # Set default for other rects to widget's general rect attributes
            if prefix != "":
                default = getattr(self, attr)

            setattr(self,
                    f"{prefix}{attr}",
                    resolve_widget(kwargs,f"{prefix}{attr}", self.type, default))

    def _mixin_setattr_hook(self, key, value):

        # Update base values for responsive resizing
        if key.startswith("base_"):
            return

        for attr in self.BASE_RECT_ATTRIBUTES:

            if key == attr or key.endswith(f"_{attr}"):

                if not pgmenu.vars.videoresized:
                    setattr(self, f"base_{key}", value)

                return

    def _resize_border_radii(self, w, h):
        self._resize_rect("", w, h)

    def _resize_rect(self, prefix, w, h):

        factor = min(w / self.base_size[0], h / self.base_size[1])

        for attr in self.BASE_RECT_ATTRIBUTES:

            base_attr = f"base_{prefix}{attr}"
            current_attr = f"{prefix}{attr}"

            value = getattr(self, base_attr)

            if value is not None:
                setattr(self, current_attr, round(value * factor))

    def _animation_update_border_radii(self, direction=pgmenu.FORWARD, reach=1):
        self._animation_update_rect("", direction, reach)

    def _animation_update_rect(self,
                               prefix="",
                               direction=pgmenu.FORWARD,
                               reach=1):

        for attr in self.BASE_RECT_ATTRIBUTES:

            value = getattr(self, f"{prefix}{attr}", None)

            if value is not None:
                value.update(direction, reach)


class TextMixin:

    def _mixin_init(self,
                    kwargs):
        self.text_font = resolve_widget(kwargs, "text_font", self.type, pgmenu.UNSET)
        self.text_background = resolve_widget(kwargs, "text_background", self.type, pgmenu.UNSET)
        self.text_antialias = resolve_widget(kwargs, "text_antialias", self.type, pgmenu.UNSET)
        self.text_italic = resolve_widget(kwargs, "text_italic", self.type, pgmenu.UNSET)
        self.text_bold = resolve_widget(kwargs, "text_bold", self.type, pgmenu.UNSET)
        self.text_strikethrough = resolve_widget(kwargs, "text_strikethrough", self.type, pgmenu.UNSET)
        self.text_underline = resolve_widget(kwargs, "text_underline", self.type, pgmenu.UNSET)
        self.text_transparency = resolve_widget(kwargs, "text_transparency", self.type, pgmenu.UNSET)