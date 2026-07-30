from typing import Sequence

import pygame
from pygame import Vector2, Color

pygame.init()


class CachedSurface(pygame.Surface):

    def __init__(self,
                 surface,
                 cache_id):
        super().__init__(surface.get_size(), surface.get_flags())

        self.blit(surface, (0, 0))

        self.cache_id = cache_id

surf1 = pygame.Surface((100, 100), pygame.SRCALPHA)
surf = CachedSurface(surf1, "test")
print(surf)

print(type(surf))