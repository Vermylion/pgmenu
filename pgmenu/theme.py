import os, sys
import json
import pygame


# TODO -> Can I set in theme dynamic args? -> Ex: margin = round(min(self.size.inttuple) * 0.1)

# TODO -> Add support for different modes -> (dark or light mode)


class Theme:

    def __init__(self):
        ...

    def _format_theme_path(self, theme):
        # Format theme text correctly if the file extension was included
        theme = os.path.splitext(theme)[0]
        # Format theme to directory path
        theme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"themes/{theme}.json"))

        return theme, theme_path

    def set(self, **attrs):
        for attribute in attrs:
            # Ignore custom comments
            if attribute == "#":
                continue

            value = attrs[attribute]

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
                    exec("value = " + value["code"])

            # For now, transform all lists into tuples (lists are unhashable for cache)
            if type(value) == list:
                value = tuple(value)

            setattr(self, attribute, value)

    def save(self, theme, **attrs):

        theme, theme_path = self._format_theme_path(theme)

        with open(theme_path, 'w') as f:
            json.dump({theme: attrs}, f, indent=4)

    # Save all arguments attributed and loaded to this class
    def save_all(self, theme):

        theme, theme_path = self._format_theme_path(theme)

        # Get all attributes by filtering them out of dir()
        attrs = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

        with open(theme_path, 'w') as f:
            json.dump({theme: attrs}, f, indent=4)

    def load(self, theme: str = "DEFAULT"):

        theme, theme_path = self._format_theme_path(theme)

        # Load attributes
        with open(theme_path) as f:

            attrs = json.load(f)[theme]
            self.set(**attrs)
