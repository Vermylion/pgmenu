import importlib
import importlib.abc
import importlib.util
import os
import pkgutil


# TODO -> Review code and functionability; written by AI


# ---------------------------------------------------------------------------
# Flat namespace: make `pgmenu.<module>` resolve to `pgmenu.<subpackage>.<module>`
# so `import pgmenu.animation as animation`, `from pgmenu.text import render`
# and `pgmenu.animation.Animate` all work. The alias table is built by scanning
# the sub-packages, so new files are picked up automatically.
# ---------------------------------------------------------------------------
_SUBPACKAGES = ("vars", "core", "base", "widgets")
_ALIASES = {}  # short name -> real dotted path

for _sub in _SUBPACKAGES:
    _path = os.path.join(os.path.dirname(__file__), _sub)
    for _info in pkgutil.iter_modules([_path]):
        if _info.ispkg or _info.name.startswith("_"):
            continue
        # A module named like its own sub-package (vars/vars.py) or like any other
        # sub-package: the package already owns `pgmenu.<name>`, so don't alias it
        if _info.name in _SUBPACKAGES:
            continue
        # Real collision between two flat modules
        if _info.name in _ALIASES:
            raise ImportError(
                f"pgmenu: module name '{_info.name}' exists in both "
                f"'{_ALIASES[_info.name]}' and '{__name__}.{_sub}.{_info.name}'. "
                f"Module names must be unique across sub-packages."
            )
        _ALIASES[_info.name] = f"{__name__}.{_sub}.{_info.name}"


class _AliasFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Resolves pgmenu.<name> to the real module, so both paths give the SAME module object."""

    def find_spec(self, fullname, path=None, target=None):
        parts = fullname.split(".")
        if len(parts) == 2 and parts[0] == __name__ and parts[1] in _ALIASES:
            return importlib.util.spec_from_loader(fullname, self)
        return None

    def create_module(self, spec):
        return importlib.import_module(_ALIASES[spec.name.split(".")[1]])

    def exec_module(self, module):
        pass  # already executed under its real name


import sys
sys.meta_path.insert(0, _AliasFinder())

# ---------------------------------------------------------------------------
# Ordered imports (order matters: constants/system/vars first, everything reads them)
# ---------------------------------------------------------------------------
from pgmenu.vars import constants, system
from pgmenu.vars.constants import *
import pgmenu.vars as vars
from pgmenu.vars import Theme, AnimationTheme

# Core
from pgmenu.core import cache, animation, theme, position, rect, text
from pgmenu.core import draw, aarect, resize, display, lib, menu, simple
from pgmenu.core.lib import draw_all, update, request_cursor

# Base (Widget + mixins)
from pgmenu.base import widget, mixins, togglewidget
from pgmenu.base import Widget, RectMixin, TextMixin, ActionableMixin   # adjust to what base/__init__ exports

# Widgets
import pgmenu.widgets as widgets
from pgmenu.widgets import Label, Surface, Frame, Button, Checkbox, Radiobutton, Scrollbar

# Expose any module not explicitly imported above (e.g. utils, scrollbar, future files)
for _name, _real in _ALIASES.items():
    globals().setdefault(_name, importlib.import_module(_real))

# ---------------------------------------------------------------------------
# Star import: every module + constants + public API, all under `pgmenu`
# ---------------------------------------------------------------------------
__all__ = sorted(
    set(_ALIASES)                                              # all flat modules
    | {"widgets", "core", "base"}                              # sub-packages ("vars" left out: it shadows the builtin)
    | {n for n in dir(constants) if n.isupper()}               # constants only, so no stray `pygame`
    | {"Theme", "AnimationTheme"}
    | {"draw_all", "update", "request_cursor"}
    | {"Widget", "RectMixin", "TextMixin", "ActionableMixin"}
    | {"Label", "Surface", "Frame", "Button", "Checkbox", "Radiobutton", "Scrollbar"}
)

# Initialize the library
lib.init()