import pygame
import pgmenu

from functools import wraps


# TODO -> Should responsive_coords account for extra space when responsive_size is False? (ex: centered button isn't centered anymore)


def _scale(base, master_size, master_base_size, mode, resize_x, resize_y):
    base = max(base[0], 1), max(base[1], 1)

    # Percentage of the screen the base covers
    widget_x_coverage = base[0] / master_base_size[0]
    widget_y_coverage = base[1] / master_base_size[1]

    resized_x = round(master_size[0] * widget_x_coverage)
    resized_y = round(master_size[1] * widget_y_coverage)

    if mode == pgmenu.PROPORTIONAL:

        x_resized_factor = resized_x / base[0]
        y_resized_factor = resized_y / base[1]

        aspect_ratio = base[0] / base[1]

        if x_resized_factor < y_resized_factor:
            resized_y = resized_x / aspect_ratio

        elif y_resized_factor < x_resized_factor:
            resized_x = resized_y * aspect_ratio

    if not resize_x:
        resized_x = base[0]

    if not resize_y:
        resized_y = base[1]

    return resized_x, resized_y


def responsive_resize(widget, event):

    if event.type == pygame.VIDEORESIZE:

        if widget.responsive_size or widget.responsive_coords:
            # To reset prev_window_size
            pgmenu.vars.videoresized = True

            if isinstance(widget.master, pgmenu.frame.Frame):
                master_size = widget.master.size
                master_base_size = widget.master.base_size

            else:
                master_size = pygame.display.get_window_size()
                master_base_size = pgmenu.vars.base_window_size

        if widget.responsive_size:

            base_size = widget.get_2d_base_size()

            w, h = _scale(base_size, master_size, master_base_size, widget.responsive_size, widget.responsive_size_w, widget.responsive_size_h)

            widget.resize(w, h)
            widget.on_resize()

        if widget.responsive_coords:

            x, y = _scale(widget.base_coords, master_size, master_base_size, widget.responsive_coords, widget.responsive_coords_x, widget.responsive_coords_y)

            widget.coords = x, y


def reset_videoresize():
    # Reset window size for VIDEORESIZE
    if pgmenu.vars.videoresized:
        # pgmenu.vars.prev_window_size = pygame.display.get_window_size()
        pgmenu.vars.videoresized = False