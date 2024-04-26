import pygame


def center_coords(size: list[int, int] | tuple[int, int],
                  rect: list[int, int, int, int] | tuple[int, int, int, int],
                  center_x: bool = True,
                  center_y: bool = True):

    rect_x, rect_y, rect_width, rect_height = rect
    # Find center of rect
    if center_x: center_rect_width = rect_width / 2
    if center_y: center_rect_height = rect_height / 2

    # Offset coord to be at middle of size
    size_width, size_height = size
    if center_x: center_size_width = size_width / 2
    if center_y: center_size_height = size_height / 2

    coord_x = rect_x + center_rect_width - center_size_width if center_x else rect_x
    coord_y = rect_y + center_rect_height - center_size_height if center_y else rect_y

    return coord_x, coord_y


def place():
    ...
