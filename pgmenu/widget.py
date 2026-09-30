import pygame
import pgmenu

from pgmenu.animation import *
from pgmenu.constants import THEME
from pgmenu.theme import resolve, resolve_kwarg, resolve_widget


# Adds widget to the system and update loop
def add(widget):
    # Sets Frame objects at the end of the draw order so other surfaces have time to blit on to them
    def insert_before_frames():
        for i in range(len(pgmenu.vars.widgets_draw_order)):
            if pgmenu.vars.widgets_draw_order[i].type == pgmenu.FRAME:
                pgmenu.vars.widgets_draw_order.insert(i, widget)
                return
        pgmenu.vars.widgets_draw_order.append(widget)

    if widget.type == pgmenu.FRAME:
        # Frames always go at the true end, so multiple frames keep their original (e.g. nesting) order relative to each other
        pgmenu.vars.widgets_draw_order.append(widget)
    else:
        # Regular widgets must be inserted before any existing Frame, otherwise they'd draw after it and the Frame couldn't have them blitted onto it yet
        insert_before_frames()

    _order_widgets(widget)


# TODO -> Organise widgets based on their coords? Or is declaration order fine too?
def _order_widgets(widget):
    pgmenu.vars.widgets.append(widget)


def _update_widget_order(widget):
    pgmenu.vars.widgets.remove(widget)
    _order_widgets(widget)


def remove(widget):
    """Unregister a widget from the engine."""
    if widget in pgmenu.vars.widgets:
        pgmenu.vars.widgets.remove(widget)
    if widget in pgmenu.vars.widgets_draw_order:
        pgmenu.vars.widgets_draw_order.remove(widget)
    if hasattr(widget, "master") and isinstance(widget.master, pgmenu.frame.Frame):
        widget.master.remove(widget)


def remove_all():
    pgmenu.vars.widgets_draw_order.clear()
    pgmenu.vars.widgets.clear()


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
            if isinstance(attr, pgmenu.animation.AnimateType) and not isinstance(value, AnimateType):

                if attr.base_value == value:
                    return

        # Create animation
        if not isinstance(value, pgmenu.animation.AnimateType):
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
            if value is not pygame.display.get_surface() and not isinstance(value, pgmenu.frame.Frame):
                raise ValueError("master attribute must be a display Surface or a Frame object.")

            if isinstance(value, pgmenu.frame.Frame):
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
        if isinstance(self.master, pgmenu.frame.Frame):
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
        pgmenu.widget.remove(self)

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


# Only fully dynamic Mixin
# FIXME -> Should all Mixins be fully dynamic?
# TODO -> Review/revamp code as it was mostly AI written
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

    def _mixin_init(self, **kwargs):
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

    def _mixin_setattr(self, key, value):

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
                setattr(self, current_attr, int(value * factor))

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
                    **kwargs):
        self.text_font = resolve_widget(kwargs, "text_font", self.type, pgmenu.UNSET)
        self.text_background = resolve_widget(kwargs, "text_background", self.type, pgmenu.UNSET)
        self.text_antialias = resolve_widget(kwargs, "text_antialias", self.type, pgmenu.UNSET)
        self.text_italic = resolve_widget(kwargs, "text_italic", self.type, pgmenu.UNSET)
        self.text_bold = resolve_widget(kwargs, "text_bold", self.type, pgmenu.UNSET)
        self.text_strikethrough = resolve_widget(kwargs, "text_strikethrough", self.type, pgmenu.UNSET)
        self.text_underline = resolve_widget(kwargs, "text_underline", self.type, pgmenu.UNSET)
        self.text_transparency = resolve_widget(kwargs, "text_transparency", self.type, pgmenu.UNSET)


class ActionableMixin:
    def _mixin_init(self,
                    **kwargs):
        ...

    def _mixin_setattr(self, key, value):
        if key == "coords":
            # _update_widget_order(self)
            ...

    # TODO -> Revamp update system with states and/or update mixin handling
    def _mixin_update(self, event):

        def down_action():
            self.state = pgmenu.ACTIVE
            self.on_press()
            self.animation_on_press()

        def up_action():
            self.state = pgmenu.NORMAL
            self.on_release()
            self.animation_on_release()

        def hold_action():
            self.on_hold()
            self.animation_on_hold()

        # Detect widget actioned
        if self.state == pgmenu.HOVERED or self.state == pgmenu.ACTIVE:

            # Keyboard activation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    down_action()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    up_action()

            elif event.type == pgmenu.IDLE_EVENT:
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    hold_action()


            # Mouse activation
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    down_action()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    up_action()

            elif event.type == pgmenu.IDLE_EVENT:
                if pygame.mouse.get_pressed()[0]:
                    hold_action()


# Base structure for Toggleable widgets: Checkbox, Radiobutton, Toggleswitch
# FIXME -> Should this live elsewhere than widget.py?
# TODO -> Possibly review code; Written by Claude off of checkbox.py code
class ToggleWidget(Widget, RectMixin, TextMixin, ActionableMixin):
    """
    Shared base for indicator+label widgets (Checkbox, Radiobutton, ...).
    Subclasses set, before super().__init__():
        self._set_indicator("prefix_")
        self._set_on_attr("name")
    """

    @property
    def is_on(self):
        return getattr(self, self._on_attr)

    @is_on.setter
    def is_on(self, value):
        setattr(self, self._on_attr, value)

    def _set_on_attr(self, name):
        self._on_attr = name

    def _set_indicator(self, prefix):
        self._indicator_prefix = prefix

    def _indicator(self, name):
        return getattr(self, f"{self._indicator_prefix}{name}")

    def toggle(self):
        self.is_on = not self.is_on

    def draw(self):
        super().draw()

        max_w = max(self.size.base_tuple[0], self.size.final_tuple[0])
        max_h = max(self.size.base_tuple[1], self.size.final_tuple[1])
        full_rect = (0, 0, *self.size.int_tuple)

        toggle_surface = pgmenu.draw.aarect(None, self.fill, full_rect, self.width, self.border_radius,
                                                self.border_top_left_radius, self.border_top_right_radius,
                                                self.border_bottom_left_radius, self.border_bottom_right_radius,
                                                self.antialiasing, self.transparency, self.aa_strength,
                                                inner_fill=self.inner_fill, inner_transparency=self.inner_transparency,
                                                inner_aa_strength=self.inner_aa_strength, inner_antialiasing=self.inner_antialiasing)

        inner_rect = (self.margin.int, self.margin.int,
                     self.size.int_tuple[0] - self.margin.int * 2, self.size.int_tuple[1] - self.margin.int * 2)
        pgmenu.draw.aarect(toggle_surface, self._indicator("fill"), inner_rect, self._indicator("width"),
                           self._indicator("border_radius"),
                           self._indicator("border_top_left_radius"), self._indicator("border_top_right_radius"),
                           self._indicator("border_bottom_left_radius"), self._indicator("border_bottom_right_radius"),
                           self._indicator("antialiasing"), self._indicator("transparency"), self._indicator("aa_strength"),
                           inner_fill=self._indicator("inner_fill"), inner_transparency=self._indicator("inner_transparency"),
                           inner_aa_strength=self._indicator("inner_aa_strength"), inner_antialiasing=self._indicator("inner_antialiasing"))

        has_text = self.text is not None and self.text != ""
        if has_text:
            text_surface = pgmenu.text.fit_height_render(self.size.base_tuple[1], self.text, self.text_color, round(self.text_margin), self.text_font,
                                                         self.text_background, self.text_antialias, self.text_italic, self.text_bold,
                                                         self.text_strikethrough, self.text_underline, self.text_transparency)
            text_surf_size = text_surface.get_size()
            side_margin = self.text_side_margin
        else:
            text_surface, text_surf_size, side_margin = None, (0, 0), 0

        surface_size = (max_w + side_margin + text_surf_size[0], max_h)
        self.surface = pgmenu.surface.cached_surface(surface_size, pygame.SRCALPHA)

        if has_text and self.text_side == pgmenu.LEFT:
            text_x, toggle_x = 0, text_surf_size[0] + side_margin
        else:
            toggle_x, text_x = 0, max_w + side_margin

        toggle_pos = pgmenu.position.center_coords(toggle_surface.get_size(), (toggle_x, 0, max_w, max_h))
        self.surface.blit(toggle_surface, toggle_pos)

        if has_text:
            text_pos = pgmenu.position.center_coords(text_surf_size, (text_x, 0, text_x + text_surf_size[0], max_h), center_x=False)
            self.surface.blit(text_surface, text_pos)

        self.master.blit(self.surface, self.coords.int_tuple)

    # TODO: IMPORTANT -> Revamp update system with states and/or update mixin handling
    def update(self, event):
        # super().update(event)

        self.surface_size = self.surface.get_size()
        self._update_rect(self.surface_size, self.coords)

        # Detect mouse collisions
        if self.state == pgmenu.HOVERED or self.state == pgmenu.ACTIVE:

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.toggle()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.toggle()

        self._mixin_hook("_mixin_update", event)

    def resize(self, w, h):
        self._resize_border_radii(w, h)
        self._resize_rect(self._indicator_prefix, w, h)

        factor = min(w / self.base_size[0], h / self.base_size[1])
        self.margin = int(self.base_margin * factor)

        self.size = w, h