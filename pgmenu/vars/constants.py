import pygame


# Constants for state
HIDDEN = "hidden"
DISABLED = "disabled"
NORMAL = "normal"
HOVERED = "hovered" # hovered state too
ACTIVE = "active"
# Constants for animation
FORWARD = "forward"
BACKWARD = "backward"
IN = "in"
OUT = "out"
IN_OUT = "in_out"
# Constants for animation looping
ONCE = "once"
LOOP = "loop"
YOYO = "yoyo"
# Directional constants
RIGHT = "right"
LEFT = "left"
TOP = "top"
BOTTOM = "bottom"
HORIZONTAL = "horizontal"
VERTICAL = "vertical"
# Widget types constants
WIDGET = "widget"
LABEL = "label"
SURFACE = "surface"
FRAME = "frame"
BUTTON = "button"
CHECKBOX = "checkbox"
RADIOBUTTON = "radiobutton"
TOGGLESWITCH = "toggleswitch"
SCROLLBAR = "scrollbar"
# Constant to know when to use theme
THEME = "theme"
# Constant to determine if an attribute derived from Theme is undefined
UNSET = "unset"
# Constants for responsive resize types
PROPORTIONAL = "proportional"
STRETCH = "stretch"
# lib.py update() pygame event for no events; idle
IDLE_EVENT = pygame.USEREVENT + 100
MOUSE_EVENTS = (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
                pygame.MOUSEMOTION, pygame.MOUSEWHEEL)


# Only import constants
__all__ = [name for name in dir() if name.isupper()]