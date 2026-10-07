import pgmenu
from pgmenu.vars.constants import THEME
from pgmenu.core.theme import resolve


__all__ = ["center_coords", "place"]


# FIXME -> Arguments aren't clear what they are
def center_coords(size: list[int, int] | tuple[int, int],
                  rect: list[int, int, int, int] | tuple[int, int, int, int],
                  center_x: bool = THEME,
                  center_y: bool = THEME) -> tuple[float, float]:

    center_x = resolve(center_x, pgmenu.Theme.position_center_x)
    center_y = resolve(center_y, pgmenu.Theme.position_center_y)

    x, y, w, h = rect
    sw, sh = size

    if center_x:
        x += (w - sw) // 2

    if center_y:
        y += (h - sh) // 2

    return x, y


# TODO -> Implement place one of these days
def place():
    ...
