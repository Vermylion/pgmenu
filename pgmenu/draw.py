import pygame
from pgmenu.aarect import AARect


def aarect(surface: pygame.Surface | None = None,
           fill: list | tuple | pygame.Surface | pygame.Color = (255, 255, 255),
           rect: list | tuple | pygame.Rect = (10, 10, 100, 30),
           width: int = 0,
           border_radius: int = 10,
           border_top_left_radius: None = None,
           border_top_right_radius: None = None,
           border_bottom_left_radius: None = None,
           border_bottom_right_radius: None = None,
           antialiasing: bool = True,
           transparency: int = 255,
           aa_strength: int = 1,
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

    rect = AARect(surface, fill, rect, width, border_radius, border_top_left_radius, border_top_right_radius,
                  border_bottom_left_radius, border_bottom_right_radius, antialiasing, transparency, aa_strength, **kwargs)
    rect_surf = rect.aarect()

    return rect_surf
