import math
import pygame
import pgmenu
from pgmenu.constants import THEME
from pgmenu.vars import cache

# TODO -> fit_rects and center_rects were fixed by AI for handling nul rects (0, 0)
#         Compare with previous code in tests/saves/rect.py


def fit_rects(dest_rect: tuple[int, int],
              *rects: tuple[int, int],
              margin: int = 0) -> list[tuple[int, int, int, int]]:
    """
    Fits multiple rectangles within a destination rectangle while maintaining their aspect ratio.
    The rectangles will all have the same height and be placed from left to right.
    Rects with zero width or height take up no space and don't consume a margin slot.

    :param dest_rect: (width, height) of the destination rectangle.
    :param rects: A variable number of rectangles (width, height) to fit within the destination.
    :param margin: The margin to apply between the rectangles and between the edges.
    :return: A list of rectangles [(x, y, width, height), ...] where each is positioned within dest_rect.
    """

    cache_id = (dest_rect, rects, margin)

    cached = pgmenu.cache.lru_get(cache["rect"], cache_id)
    if cached is not None:
        return cached

    dest_width, dest_height = dest_rect

    # Only rects with an actual area participate in the fitting math below.
    # This keeps the algorithm itself free of any zero-size special-casing.
    indexed = list(enumerate(rects))
    visible = [(i, w, h) for i, (w, h) in indexed if w > 0 and h > 0]

    scaled_rects = []
    total_width = 0

    for _, width, height in visible:
        aspect_ratio = width / height

        new_height = dest_height - 2 * margin  # Account for vertical margins
        new_width = math.floor(new_height * aspect_ratio)

        scaled_rects.append((new_width, new_height))
        total_width += new_width

    total_width += margin * (len(visible) + 1)  # Margins between and around the visible rects

    # If the total width exceeds the destination width, scale all rects down proportionally
    if visible and total_width > dest_width:
        scale_factor = (dest_width - margin * (len(visible) + 1)) / (total_width - margin * (len(visible) + 1))
        scaled_rects = [(math.floor(width * scale_factor), math.floor(height * scale_factor)) for width, height in scaled_rects]

    # Place visible rects left to right, tracking their original positions
    positioned_rects = [None] * len(rects)
    x_pos = margin  # Start with the left margin

    for (original_index, _, _), (width, height) in zip(visible, scaled_rects):
        width, height = max(width, 0), max(height, 0)
        positioned_rects[original_index] = (x_pos, margin, width, height)
        x_pos += width + margin  # Move x position for the next rectangle

    # Any rect that was filtered out (zero width/height) just gets a position with no size
    for i, (width, height) in indexed:
        if positioned_rects[i] is None:
            positioned_rects[i] = (x_pos, margin, 0, 0)

    # Unpack rects list if there is only 1 rect
    if len(positioned_rects) == 1:
        positioned_rects = positioned_rects[0]

    pgmenu.cache.lru_set(cache["rect"], cache_id, positioned_rects)

    return positioned_rects


def center_rects(dest_rect: tuple[int, int, int, int],
                 *rects: tuple[int, int, int, int],
                 center_x: bool = THEME,
                 center_y: bool = THEME) -> list[tuple[float, float, int, int]]:

    cache_id = (dest_rect, rects, center_x, center_y)

    cached = pgmenu.cache.lru_get(cache["rect"], cache_id)
    if cached is not None:
        return cached

    # Only rects with actual area define the bounding box being centered
    visible = [r for r in rects if r[2] > 0 and r[3] > 0] or list(rects)

    x_min = visible[0][0]
    y_min = visible[0][1]
    max_width = visible[0][0] + visible[0][2]
    max_height = visible[0][1] + visible[0][3]

    for x, y, width, height in visible:
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        max_width = max(max_width, x + width)
        max_height = max(max_height, y + height)

    total_width = max_width - x_min
    total_height = max_height - y_min

    centered_bounding_coords = pgmenu.position.center_coords((total_width, total_height), dest_rect, center_x, center_y)

    offset_x = centered_bounding_coords[0] - x_min
    offset_y = centered_bounding_coords[1] - y_min

    # All rects, including zero-size ones, are shifted by the same offset
    shifted_rects = [(rect[0] + offset_x, rect[1] + offset_y, *rect[2:]) for rect in rects]

    if len(shifted_rects) == 1:
        shifted_rects = shifted_rects[0]

    pgmenu.cache.lru_set(cache["rect"], cache_id, shifted_rects)

    return shifted_rects
