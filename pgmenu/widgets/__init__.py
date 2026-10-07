from ._handling import add, remove, remove_all

from .label import Label
from .surface import Surface
from .frame import Frame
from .button import Button
from .checkbox import Checkbox
from .radiobutton import Radiobutton, RadioGroup
from .toggleswitch import ToggleSwitch

__all__ = [
    "add",
    "remove",
    "remove_all",

    "Label",
    "Surface",
    "Frame",
    "Button",
    "Checkbox",
    "Radiobutton",
    "RadioGroup",
    "ToggleSwitch",
]