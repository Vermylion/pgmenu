import pygame
import pgmenu
from pgmenu.core.aarect import AARect
from pgmenu.vars.constants import THEME
from pgmenu.core.theme import resolve, resolve_kwarg


__all__ = ['aarect', 'gradient']


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
    '''

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
    '''

    # kwargs aarect arguments
    fill = resolve(fill, 'fill', 'aarect')
    rect = resolve(rect, 'rect', 'aarect')
    width = resolve(width, 'width', 'aarect')
    border_radius = resolve(border_radius, 'border_radius', 'aarect', round(min(rect[2:]) / 4))
    border_top_left_radius = resolve(border_top_left_radius, 'border_top_left_radius', 'aarect', border_radius)
    border_top_right_radius = resolve(border_top_right_radius, 'border_top_right_radius', 'aarect', border_radius)
    border_bottom_left_radius = resolve(border_bottom_left_radius, 'border_bottom_left_radius', 'aarect', border_radius)
    border_bottom_right_radius = resolve(border_bottom_right_radius, 'border_bottom_right_radius', 'aarect', border_radius)
    antialiasing = resolve(antialiasing, 'antialiasing', 'aarect')
    transparency = resolve(transparency, 'transparency', 'aarect')
    aa_strength = resolve(aa_strength, 'aa_strength', 'aarect')
    # Additional parameters for modifying inside rect
    inner_fill = resolve_kwarg(kwargs, 'inner_fill', 'aarect', None)
    inner_transparency = resolve_kwarg(kwargs, 'inner_transparency', 'aarect', transparency)
    inner_aa_strength = resolve_kwarg(kwargs, 'inner_aa_strength', 'aarect', aa_strength)
    inner_antialiasing = resolve_kwarg(kwargs, 'inner_antialiasing', 'aarect', antialiasing)
    # Additional parameters
    debug = resolve_kwarg(kwargs, 'debug', 'aarect')

    rect = AARect(surface, fill, rect, width, border_radius, border_top_left_radius, border_top_right_radius,
                  border_bottom_left_radius, border_bottom_right_radius, antialiasing, transparency, aa_strength,
                  inner_fill=inner_fill, inner_transparency=inner_transparency, inner_aa_strength=inner_aa_strength,
                  inner_antialiasing=inner_antialiasing, debug=debug)
    rect_surf = rect.aarect()

    return rect_surf


# TODO -> Implement gradient one of these days
def gradient(color1,
             color2,
             angle,
             curve):
    ...
