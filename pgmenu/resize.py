import pygame
import pgmenu


# TODO -> Dynamic resize doesn't reset correctly -> Everything gets bigger

# TODO -> Should responsive_coords account for extra space when responsive_size is False? (ex: centered button isn't centered anymore)

# TODO -> PROPORTIONAL resize doesn't work exactly as expected, has to be tweaked


def responsive_resize(widget, event):
    if event.type == pygame.VIDEORESIZE:

        if widget.responsive_size or widget.responsive_coords:
            # To reset prev_window_size
            pgmenu.vars.videoresized = True

            win_size = pygame.display.get_window_size()

            w_x_factor = win_size[0] / pgmenu.vars.prev_window_size[0]
            h_y_factor = win_size[1] / pgmenu.vars.prev_window_size[1]

            if w_x_factor < 1 or h_y_factor < 1:
                proportional_factor = max(w_x_factor, h_y_factor)
            else:
                proportional_factor = min(w_x_factor, h_y_factor)

        if widget.responsive_size:
            prev_min_size = min(widget.size.inttuple)

            # Set modifying factors
            if widget.responsive_size == pgmenu.STRETCH:
                w_factor, h_factor = w_x_factor, h_y_factor

            else:
                w_factor, h_factor = proportional_factor, proportional_factor

            if widget.responsive_size_w:
                widget.size = widget.size.inttuple[0] * w_factor, widget.size.inttuple[1]

            if widget.responsive_size_h:
                widget.size = widget.size.inttuple[0], widget.size.inttuple[1] * h_factor

            # Modify border_radii size, keeping each of their sizes proportional
            for border_radius in widget._border_radii:
                setattr(widget, border_radius, getattr(widget, border_radius).base_num * (min(widget.size.inttuple) / prev_min_size))

        if widget.responsive_coords:

            # Set modifying factors
            if widget.responsive_coords == pgmenu.STRETCH:
                x_factor, y_factor = w_x_factor, h_y_factor

            else:
                x_factor, y_factor = proportional_factor, proportional_factor

            if widget.responsive_coords_x:
                widget.coords = widget.coords.inttuple[0] * x_factor, widget.coords.inttuple[1]

            if widget.responsive_coords_y:
                widget.coords = widget.coords.inttuple[0], widget.coords.inttuple[1] * y_factor


def reset_videoresize():
    # Reset window size for VIDEORESIZE
    if pgmenu.vars.videoresized:
        pgmenu.vars.prev_window_size = pygame.display.get_window_size()
        pgmenu.vars.videoresized = False
