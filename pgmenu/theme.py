import os, sys
import json
import pygame


# TODO -> Can I set in theme dynamic args? -> Ex: margin = round(min(self.size.inttuple) * 0.1)


class Theme:

    def __init__(self):
        ...

    def inherit_theme(self,
                      obj: object | None,
                      *var_names):
        ...

    def load(self, theme: str = "DEFAULT"):
        # FIXME -> Is path going to be a problem? Check it out
        # Format theme text correctly if the file extension was included
        theme = os.path.splitext(theme)[0]
        # Load attributes
        with open(f"{theme}.json") as f:

            attributes = json.load(f)[theme]
            for attribute in attributes:
                # Ignore custom comments
                if attribute == "#":
                    continue

                value = attributes[attribute]

                if type(value) == dict:
                    # Allow for different custom json types
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

                # For now, transform all lists into tuples (lists are unhashable for cache)
                if type(value) == list:
                    value = tuple(value)

                setattr(self, attribute, value)
