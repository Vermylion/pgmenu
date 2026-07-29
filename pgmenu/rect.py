import math
import pygame
import pgmenu
from pgmenu.constants import THEME
from pgmenu.vars import cache


def fit_rects(dest_rect: tuple[int, int], *rects: tuple[int, int], margin: int = 0) -> list[tuple[int, int, int, int]]:
    """
    Fits multiple rectangles within a destination rectangle while maintaining their aspect ratio.
    The rectangles will all have the same height and be placed from left to right.

    :param dest_rect: (width, height) of the destination rectangle.
    :param rects: A variable number of rectangles (width, height) to fit within the destination.
    :param margin: The margin to apply between the rectangles and between the edges.
    :return: A list of rectangles [(x, y, width, height), ...] where each is positioned within dest_rect.
    """

    # Keep the same cache_id in function
    cache_id = (dest_rect, rects, margin)

    # Load from cache if already in cache
    cached = pgmenu.cache.lru_get(cache["rect"], cache_id)
    if cached is not None:
        return cached

    dest_width, dest_height = dest_rect
    # rects = list(rects)  # Convert to a list if needed

    # Scale all rects to the destination height and adjust width proportionally
    scaled_rects = []
    total_width = 0

    for width, height in rects:
        aspect_ratio = width / height
        new_height = dest_height - 2 * margin  # Account for vertical margins
        new_width = math.ceil(new_height * aspect_ratio)
        scaled_rects.append((new_width, new_height))
        total_width += new_width

    total_width += margin * (len(scaled_rects) + 1)  # Include margins between and around the rects

    # If the total width exceeds the destination width, scale all rects down proportionally
    if total_width > dest_width:
        scale_factor = (dest_width - margin * (len(scaled_rects) + 1)) / (total_width - margin * (len(scaled_rects) + 1))
        scaled_rects = [(math.ceil(width * scale_factor), math.ceil(height * scale_factor)) for width, height in scaled_rects]

    # Place rects left to right
    positioned_rects = []
    x_pos = margin  # Start with the left margin

    for width, height in scaled_rects:
        positioned_rects.append((x_pos, margin, width, height))  # Place rect (x, y, width, height)
        x_pos += width + margin  # Move x position for the next rectangle

    # Unpack rects list if there is only 1 rect
    if len(positioned_rects) == 1:
        positioned_rects = positioned_rects[0]

    # Cache calculated rects
    pgmenu.cache.lru_set(cache["rect"], cache_id, positioned_rects)

    return positioned_rects


def center_rects(dest_rect: tuple[int, int, int, int],
                 *rects: tuple[int, int, int, int],
                 center_x: bool = THEME,
                 center_y: bool = THEME) -> list[tuple[float, float, int, int]]:

    # Keep the same cache_id in function
    cache_id = (dest_rect, rects, center_x, center_y)

    # Load from cache if already in cache
    cached = pgmenu.cache.lru_get(cache["rect"], cache_id)
    if cached is not None:
        return cached

    # Filler values
    x_min = rects[0][0]
    y_min = rects[0][1]
    max_width = rects[0][0] + rects[0][2]
    max_height = rects[0][1] + rects[0][3]

    # Loop through each rectangle and adjust x_min, y_min, max_width, and max_height
    for x, y, width, height in rects:
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        max_width = max(max_width, x + width)
        max_height = max(max_height, y + height)

    # Calculate the total width and height of the bounding box
    total_width = max_width - x_min
    total_height = max_height - y_min

    # Center bounding box
    centered_bounding_coords = pgmenu.position.center_coords((total_width, total_height), dest_rect, center_x, center_y)

    # Calculate by how much each rect has to be shifted
    offset_x = centered_bounding_coords[0] - x_min
    offset_y = centered_bounding_coords[1] - y_min

    # Shift all rects by the centered bounding offset
    shifted_rects = [[rect[0] + offset_x, rect[1] + offset_y, *rect[2:]] for rect in rects]

    # Unpack rects list if there is only 1 rect
    if len(shifted_rects) == 1:
        shifted_rects = shifted_rects[0]

    # Cache calculated rects
    pgmenu.cache.lru_set(cache["rect"], cache_id, shifted_rects)

    return shifted_rects
