import pygame
import pgmenu

from pgmenu.vars.constants import FORWARD, BACKWARD, THEME
from pgmenu.core.theme import resolve_kwarg


__all__ = ["RectMixin", "TextMixin", "ActionableMixin"]


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

            setattr(self, f"{prefix}{attr}", resolve_kwarg(kwargs, f"{prefix}{attr}", self.type, default))

    def _mixin_setattr(self, key, value):

        # Update base values for responsive resizing
        if key.startswith("base_"):
            return

        for attr in self.BASE_RECT_ATTRIBUTES:

            if key == attr or key.endswith(f"_{attr}"):

                if not pgmenu.vars.videoresized:
                    setattr(self, f"base_{key}", value)

                return

    def _resize_border_radii(self, w: int, h: int):
        self._resize_rect("", w, h)

    def _resize_rect(self, prefix: str, w: int, h: int):

        factor = min(w / self.base_size[0], h / self.base_size[1])

        for attr in self.BASE_RECT_ATTRIBUTES:

            base_attr = f"base_{prefix}{attr}"
            current_attr = f"{prefix}{attr}"

            value = getattr(self, base_attr)

            if value is not None:
                setattr(self, current_attr, int(value * factor))

    def _animation_update_border_radii(self, direction=FORWARD, reach=1):
        self._animation_update_rect("", direction, reach)

    def _animation_update_rect(self,
                               prefix="",
                               direction=FORWARD,
                               reach=1):

        for attr in self.BASE_RECT_ATTRIBUTES:

            value = getattr(self, f"{prefix}{attr}", None)

            if value is not None:
                value.update(direction, reach)


class TextMixin:

    def _mixin_init(self,
                    **kwargs):
        self.text_font = resolve_kwarg(kwargs, "text_font", self.type, pgmenu.UNSET)
        self.text_background = resolve_kwarg(kwargs, "text_background", self.type, pgmenu.UNSET)
        self.text_antialias = resolve_kwarg(kwargs, "text_antialias", self.type, pgmenu.UNSET)
        self.text_italic = resolve_kwarg(kwargs, "text_italic", self.type, pgmenu.UNSET)
        self.text_bold = resolve_kwarg(kwargs, "text_bold", self.type, pgmenu.UNSET)
        self.text_strikethrough = resolve_kwarg(kwargs, "text_strikethrough", self.type, pgmenu.UNSET)
        self.text_underline = resolve_kwarg(kwargs, "text_underline", self.type, pgmenu.UNSET)
        self.text_transparency = resolve_kwarg(kwargs, "text_transparency", self.type, pgmenu.UNSET)
        self.text_line_spacing = resolve_kwarg(kwargs, "text_line_spacing", self.type, pgmenu.UNSET)


class ActionableMixin:
    def _mixin_init(self,
                    **kwargs):
        ...

    # TODO -> Revamp update system with states and/or update mixin handling
    def _mixin_update(self, event):

        def down_action():
            self._on_press()
            self.on_press()
            self.animation_on_press()

        def up_action():
            self._on_release()
            self.on_release()
            self.animation_on_release()

        def hold_action():
            self._on_hold()
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
