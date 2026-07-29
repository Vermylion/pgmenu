import pygame
import pgmenu
from pgmenu.aarect import AARect
from pgmenu.constants import THEME
from pgmenu.theme import resolve, resolve_kwarg


def aarect(surface: pygame.Surface | None = None,
           fill: list | tuple | pygame.Surface | pygame.Color = THEME,
           rect: list | tuple | pygame.Rect = THEME,
           width: int = THEME,
           border_radius: int = THEME,
           border_top_left_radius: int | None = THEME,
           border_top_right_radius: int | None = THEME,
           border_bottom_left_radius: int | None = THEME,
           border_bottom_right_radius: int | None = THEME,
           antialiasing: bool = THEME,
           transparency: int = THEME,
           aa_strength: int = THEME,
           **kwargs):
    """

    :param surface:
    :param fill:
    :param rect:
    :param width:
    :param border_radius:
    :param border_top_left_radius:
    :param border_top_right_radius:
    :param border_bottom_left_radius:
    :param border_bottom_right_radius:
    :param antialiasing:
    :param transparency:
    :param aa_strength:
    :key inner_fill:
    :key inner_transparency:
    :key inner_aa_strength:
    :key inner_antialiasing:
    """

    # kwargs aarect arguments
    fill = resolve(fill, pgmenu.Theme.aarect_fill)
    rect = resolve(rect, pgmenu.Theme.aarect_rect)
    width = resolve(width, pgmenu.Theme.aarect_width)
    border_radius = resolve(border_radius, pgmenu.Theme.aarect_border_radius, round(min(rect[2:]) / 4))
    border_top_left_radius = resolve(border_top_left_radius, pgmenu.Theme.aarect_border_top_left_radius, border_radius)
    border_top_right_radius = resolve(border_top_right_radius, pgmenu.Theme.aarect_border_top_right_radius, border_radius)
    border_bottom_left_radius = resolve(border_bottom_left_radius, pgmenu.Theme.aarect_border_bottom_left_radius, border_radius)
    border_bottom_right_radius = resolve(border_bottom_right_radius, pgmenu.Theme.aarect_border_bottom_right_radius, border_radius)
    antialiasing = resolve(antialiasing, pgmenu.Theme.aarect_antialiasing)
    transparency = resolve(transparency, pgmenu.Theme.aarect_transparency)
    aa_strength = resolve(aa_strength, pgmenu.Theme.aarect_aa_strength)
    # Additional parameters for modifying inside rect
    inner_fill = resolve_kwarg(kwargs, 'inner_fill', pgmenu.Theme.aarect_inner_fill, fill)
    inner_transparency = resolve_kwarg(kwargs, 'inner_transparency', pgmenu.Theme.aarect_inner_transparency, transparency)
    inner_aa_strength = resolve_kwarg(kwargs, 'inner_aa_strength', pgmenu.Theme.aarect_inner_aa_strength, aa_strength)
    inner_antialiasing = resolve_kwarg(kwargs, 'inner_antialiasing', pgmenu.Theme.aarect_inner_antialiasing, antialiasing)
    # Additional parameters
    debug = kwargs.get('debug', pgmenu.Theme.aarect_debug)

    rect = AARect(surface, fill, rect, width, border_radius, border_top_left_radius, border_top_right_radius,
                  border_bottom_left_radius, border_bottom_right_radius, antialiasing, transparency, aa_strength,
                  inner_fill=inner_fill, inner_transparency=inner_transparency, inner_aa_strength=inner_aa_strength,
                  inner_antialiasing=inner_antialiasing, debug=debug)
    rect_surf = rect.aarect()

    return rect_surf


def gradient(color1,
             color2,
             angle,
             curve):
    ...
