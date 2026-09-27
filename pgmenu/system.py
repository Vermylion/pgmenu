# Collection of important variables that can impact the functioning of the library
# Meant to be accessed, and modified if need be, by the user
import pygame

# Whether active or hovered widgets are drawn on top
WIDGET_DRAW_PRIORITY = True
# Max cache size per cached dict
# Cache size 100 equals to about 150mb of ram added
# Keep in mind this is 100 per cache, and there are 5 cache total
# FIXME -> 5 cache dict may be too much; divide max_cache_size per cache dict?
MAX_CACHE_SIZE = 300 # Min value of 1
# Key (or None) to be used for keyboard widget selection
KB_SELECTION = pygame.K_TAB
# Library's base widget types
WIDGET_TYPES = ("label",
                "surface",
                "frame",
                "button",
                "checkbox",
                "radiobutton",
                "toggleswitch")
