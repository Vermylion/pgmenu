import pygame
import pgmenu
from pgmenu.aarect import AARect
from pgmenu.constants import THEME


def aarect(surface: pygame.Surface | None = THEME,
           fill: list | tuple | pygame.Surface | pygame.Color = THEME,
           rect: list | tuple | pygame.Rect = THEME,
           width: int = THEME,
           border_radius: int = THEME,
           border_top_left_radius: None = THEME,
           border_top_right_radius: None = THEME,
           border_bottom_left_radius: None = THEME,
           border_bottom_right_radius: None = THEME,
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
    :param kwargs:
    inside_fill:
    inside_transparency:
    inside_border_radius:
    inside_border_top_left_radius:
    inside_border_top_right_radius:
    inside_border_bottom_left_radius:
    inside_border_bottom_right_radius:
    inside_aa_strength:
    inside_antialiasing:
    force_only_overlay:
    debug:
    """

    # kwargs aarect arguments
    fill = fill if fill != THEME else pgmenu.Theme.draw_fill
    rect = rect if rect != THEME else pgmenu.Theme.draw_rect
    width = width if width != THEME else pgmenu.Theme.width
    border_radius = border_radius if border_radius != THEME else pgmenu.Theme.border_radius  # round(min(self.size.tuple) / 3)  # if border_radius is not None else pgmenu.vars.Theme.border_radius
    border_top_left_radius = border_top_left_radius if border_top_left_radius != THEME else border_radius  # pgmenu.Theme.border_top_left_radius
    border_top_right_radius = border_top_right_radius if border_top_right_radius != THEME else border_radius  # pgmenu.Theme.border_top_right_radius
    border_bottom_left_radius = border_bottom_left_radius if border_bottom_left_radius != THEME else border_radius  # pgmenu.Theme.border_bottom_left_radius
    border_bottom_right_radius = border_bottom_right_radius if border_bottom_right_radius != THEME else border_radius  # pgmenu.Theme.border_bottom_right_radius
    antialiasing = antialiasing if antialiasing != THEME else pgmenu.Theme.antialiasing
    transparency = transparency if transparency != THEME else pgmenu.Theme.transparency
    aa_strength = aa_strength if aa_strength != THEME else pgmenu.Theme.aa_strength
    # Additional parameters for modifying inside rect
    inside_fill = kwargs['inside_fill'] if 'inside_fill' in kwargs else None  # pgmenu.Theme.inside_fill
    inside_transparency = kwargs['inside_transparency'] if 'inside_transparency' in kwargs else transparency # pgmenu.Theme.inside_transparency
    inside_border_radius = kwargs['inside_border_radius'] if 'inside_border_radius' in kwargs else border_radius # pgmenu.Theme.inside_border_radius
    inside_border_top_left_radius = kwargs['inside_border_top_left_radius'] if 'inside_border_top_left_radius' in kwargs else inside_border_radius  # pgmenu.Theme.inside_border_top_left_radius
    inside_border_top_right_radius = kwargs['inside_border_top_right_radius'] if 'inside_border_top_right_radius' in kwargs else inside_border_radius  # pgmenu.Theme.inside_border_top_right_radius
    inside_border_bottom_left_radius = kwargs['inside_border_bottom_left_radius'] if 'inside_border_bottom_left_radius' in kwargs else inside_border_radius  # pgmenu.Theme.inside_border_bottom_left_radius
    inside_border_bottom_right_radius = kwargs['inside_border_bottom_right_radius'] if 'inside_border_bottom_right_radius' in kwargs else inside_border_radius  # pgmenu.Theme.inside_border_bottom_right_radius
    inside_aa_strength = kwargs['inside_aa_strength'] if 'inside_aa_strength' in kwargs else aa_strength  # pgmenu.Theme.inside_aa_strength
    inside_antialiasing = kwargs['inside_antialiasing'] if 'inside_antialiasing' in kwargs else antialiasing  # pgmenu.Theme.inside_antialiasing
    # Additional parameters
    debug = kwargs['debug'] if 'debug' in kwargs else pgmenu.Theme.debug
    force_only_overlay = kwargs['force_only_overlay'] if 'force_only_overlay' in kwargs else pgmenu.Theme.force_only_overlay

    rect = AARect(surface, fill, rect, width, border_radius, border_top_left_radius, border_top_right_radius,
                  border_bottom_left_radius, border_bottom_right_radius, antialiasing, transparency, aa_strength,
                  inside_fill=inside_fill, inside_transparency=inside_transparency, inside_border_radius=inside_border_radius,
                  inside_border_top_left_radius=inside_border_top_left_radius, inside_border_top_right_radius=inside_border_top_right_radius,
                  inside_border_bottom_left_radius=inside_border_bottom_left_radius, inside_border_bottom_right_radius=inside_border_bottom_right_radius,
                  inside_aa_strength=inside_aa_strength, inside_antialiasing=inside_antialiasing,
                  debug=debug, force_only_overlay=force_only_overlay)
    rect_surf = rect.aarect()

    return rect_surf


def gradient(color1,
             color2,
             angle,
             curve):
    ...
