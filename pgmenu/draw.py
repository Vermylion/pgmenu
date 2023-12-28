import pygame
from aarect import AARect


def aarect(surface: pygame.Surface,
           fill: list | tuple | pygame.Surface,
           rect: list | tuple | pygame.Rect,
           width: int = 0,
           border_radius: int = 0,
           border_top_left_radius: None = None,
           border_top_right_radius: None = None,
           border_bottom_left_radius: None = None,
           border_bottom_right_radius: None = None,
           anti_aliasing: bool = True,
           transparency: int = 255,
           aa_strength: int = 1,
           **kwargs):

    # Additional parameters for modifying inside rect from kwargs
    inside_fill = kwargs['inside_fill'] if 'inside_fill' in kwargs else fill
    inside_transparency = kwargs['inside_transparency'] if 'inside_transparency' in kwargs else transparency

