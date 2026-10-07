# Constants, system settings, global state (must come first; everything else reads these)
from pgmenu.vars import constants, system
from pgmenu.vars.constants import *
import pgmenu.vars as vars
from pgmenu.vars import Theme, AnimationTheme

# Core
from pgmenu.core import cache, animation, theme, position, rect, text # utils isn't imported as it's only for lib side
from pgmenu.core import draw, aarect, resize, display, lib, menu, simple
from pgmenu.core.lib import *          # draw_all, update, request_cursor...

# Base for widgets (Widget + mixins)
from pgmenu.base import widget, mixins, togglewidget
from pgmenu.base import Widget

# Widgets
import pgmenu.widgets as widgets

# TODO -> Define what the star import should import
__all__ = []

# Initialize the library
lib.init()