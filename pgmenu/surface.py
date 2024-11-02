import pygame
import pgmenu
from pgmenu.vars import surface_cached_surfaces


class Surface:

    def __init__(self):
        ...


def cache_surface():
    ...


def resize(surface: pygame.Surface,
           size: tuple[int, int]):
    """resizes surface with pygame.transform.scale and caches result"""
    cache_id = (surface, size)

    if cache_id in surface_cached_surfaces:
        return surface_cached_surfaces[cache_id]

    surface = pygame.transform.scale(surface, size)

    surface_cached_surfaces[cache_id] = surface

    return surface
