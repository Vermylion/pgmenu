import os, sys
from functools import partial
import json
import pygame
import pgmenu


__all__ = ["Theme", "AnimationTheme", "resolve", "resolve_kwarg", "resolve_widget"]


# TODO -> Clean up code and comments

# TODO -> Implement DEFAULT-LIGHT.json


def _format_theme_path(theme, path="../themes"):
    # Format theme text correctly if the file extension was included
    theme = os.path.splitext(theme)[0]
    # Format theme to directory path
    theme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path, f"{theme}.json"))

    return theme, theme_path


class Theme:

    def __init__(self):
        ...

    def set(self, **attrs):

        for attr in attrs:
            # Ignore custom comments
            if attr == "#":
                continue

            value = attrs[attr]

            # Global attribute assignment
            # Slower but follows attribute assignement order
            if attr.startswith("widgets_"):
                suffix = attr[len("widgets_"):]
                for any_attr in attrs:
                    if any_attr.startswith(pgmenu.system.WIDGET_TYPES) and any_attr.endswith(suffix):
                        setattr(self, any_attr, value)

            # Allow for different custom json types
            if type(value) == dict:
                if value['type'] == "method":
                    # Get module instance (ex: pgmenu.widget)
                    module = sys.modules[value['module']]
                    # Get class object
                    cls = getattr(module, value['object'])
                    instance = cls()
                    # Get method assigned to class
                    value = getattr(instance, value['method'])

                elif value['type'] == "function":
                    # Get module instance (ex: pgmenu.widget)
                    module = sys.modules[value['module']]
                    # Get function assigned to module
                    value = getattr(module, value['function'])

                elif value['type'] == "attribute":
                    value = getattr(self, value['attribute'])

                elif value['type'] == "variable":
                    module = sys.modules[value['module']]
                    value = getattr(module, value['variable'])

                elif value['type'] == "image":
                    value = pygame.image.load(value['path'])

            # For now, transform all lists into tuples (lists are unhashable for cache)
            if type(value) == list:
                value = tuple(value)

            setattr(self, attr, value)

    def load(self, theme: str = "DEFAULT"):

        theme, theme_path = _format_theme_path(theme)

        # Load attributes
        with open(theme_path) as f:

            attrs = json.load(f)[theme]
            self.set(**attrs)

    # TODO -> Fix save and save_all methods, or remove them
    # def save(self, theme, **attrs):
    #
    #     theme, theme_path = _format_theme_path(theme)
    #
    #     with open(theme_path, 'w') as f:
    #         json.dump({theme: attrs}, f, indent=4)
    #
    # # Save all arguments attributed and loaded to this class
    # def save_all(self, theme):
    #
    #     theme, theme_path = _format_theme_path(theme)
    #
    #     # Get all attributes by filtering them out of dir()
    #     attrs = vars(self) # {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")}
    #
    #     with open(theme_path, 'w') as f:
    #         json.dump({theme: attrs}, f, indent=4)


class AnimationTheme:

    def __init__(self):
        ...

    def set(self, **funcs):

        animation_funcs = {}

        def create_animation_function(animation):

            def animate(self):
                if self.disable_default_animation:
                    return

                for action in animation:
                    action_type = action["type"]
                    name = action["name"]
                    args = action.get("args", [])

                    if action_type == "attribute":
                        getattr(self, name).update(*args)

                    elif action_type == "method":
                        getattr(self, name)(*args)

                    elif action_type == "base":
                        animation_funcs[name](self)

            return animate

        for func in funcs:
            if func == "#":
                continue

            animation_funcs[func] = create_animation_function(funcs[func])

            setattr(self, func, animation_funcs[func])

    def load(self, theme: str = "DEFAULT"):

        theme, theme_path = _format_theme_path(theme, "../themes/animation")

        # Load attributes
        with open(theme_path) as f:
            funcs = json.load(f)[theme]
            self.set(**funcs)


"""
resolve_widget(...)
│
├── 1. User supplied a kwarg?
│      │
│      ├── Yes
│      │     │
│      │     ├── Value != pgmenu.THEME
│      │     │       └── Return user value
│      │     │
│      │     └── Value == pgmenu.THEME
│      │             │
│      │             ├── Widget theme attribute exists
│      │             │       └── Return widget theme value
│      │             │
│      │             └── No widget theme attribute
│      │                     └── Return default
│      │
│      └── No kwarg
│             │
│             ├── Widget theme attribute exists
│             │       └── Return widget theme value
│             │
│             └── No widget theme attribute
│                     └── Return default
"""

def resolve(value, theme_attr, default = None, bind = None):
    """
    Function to resolve THEME affectation and Theme default case with None.
    Any value that is pgmenu.UNSET is disregarded and sent to theme_attr or default

    value
    │
    ├── Explicit value
    │      └── return value
    │
    └── THEME
           │
           ├── Theme attribute exists
           │      └── return theme_attr
           │
           └── No theme attribute
                  └── return default
    """

    if value != pgmenu.THEME and value != pgmenu.UNSET:
        result = value

    elif theme_attr is not None:
        result = theme_attr

        if bind is not None and callable(result):
            return partial(result, bind)

    else:
        result = default

    return result

def resolve_kwarg(kwargs, key, theme_attr, default = None, bind = None):
    """
    Function to resolve kwarg affectation and Theme default case with None.
    Any value that is pgmenu.UNSET is disregarded and sent to theme_attr or default
    """

    return resolve(kwargs.get(key, pgmenu.THEME), theme_attr, default, bind)

def resolve_widget(kwargs, key, widget_type, default = None, theme = None, bind = None):
    """
    Function to resolve kwarg affectation and Theme default case with None with theme attribute per widget type.
    Any value that is pgmenu.UNSET is disregarded and sent to theme_attr or default
    """

    # Set unspecified theme to base theme
    theme = theme if theme is not None else pgmenu.Theme

    # an absence of theme attr goes to default in resolve_widget -> returns None, hence default
    theme_attr = getattr(theme, f'{widget_type}_{key}', None)

    return resolve_kwarg(kwargs, key, theme_attr, default, bind)
