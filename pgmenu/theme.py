import os, sys
import json
import pygame
import pgmenu


# TODO -> Add support for different modes -> (dark or light mode)


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
                    if any_attr.startswith(pgmenu.vars.widget_types) and any_attr.endswith(suffix):
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

                elif value['type'] == "exec":
                    namespace = {"self": self, "pgmenu": pgmenu, "pygame": pygame}
                    exec("value = " + value["code"], namespace)
                    value = namespace["value"]

            # For now, transform all lists into tuples (lists are unhashable for cache)
            if type(value) == list:
                value = tuple(value)

            setattr(self, attr, value)

    def save(self, theme, **attrs):

        theme, theme_path = _format_theme_path(theme)

        with open(theme_path, 'w') as f:
            json.dump({theme: attrs}, f, indent=4)

    # Save all arguments attributed and loaded to this class
    def save_all(self, theme):

        theme, theme_path = _format_theme_path(theme)

        # Get all attributes by filtering them out of dir()
        attrs = vars(self) # {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")}

        with open(theme_path, 'w') as f:
            json.dump({theme: attrs}, f, indent=4)

    def load(self, theme: str = "DEFAULT"):

        theme, theme_path = _format_theme_path(theme)

        # Load attributes
        with open(theme_path) as f:

            attrs = json.load(f)[theme]
            self.set(**attrs)


def _format_theme_path(theme):
    # Format theme text correctly if the file extension was included
    theme = os.path.splitext(theme)[0]
    # Format theme to directory path
    theme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"themes/{theme}.json"))

    return theme, theme_path


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

def resolve(value, theme_attr, default = None):
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
        return value

    elif theme_attr is not None:
        return theme_attr

    else:
        return default

def resolve_kwarg(kwargs, key, theme_attr, default = None):
    """
    Function to resolve kwarg affectation and Theme default case with None.
    Any value that is pgmenu.UNSET is disregarded and sent to theme_attr or default
    """

    return resolve(kwargs.get(key, pgmenu.THEME), theme_attr, default)

def resolve_widget(kwargs, key, widget_type, default = None):
    """
    Function to resolve kwarg affectation and Theme default case with None with theme attribute per widget type.
    Any value that is pgmenu.UNSET is disregarded and sent to theme_attr or default
    """

    # an absence of theme attr goes to default in resolve_widget -> returns None, hence default
    theme_attr = getattr(pgmenu.Theme, f'{widget_type}_{key}', None)

    return resolve_kwarg(kwargs, key, theme_attr, default)
