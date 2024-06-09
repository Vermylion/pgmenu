import pygame
import pgmenu

# TODO -> Might need recursion of event instead of events

# TODO -> Limit certain actions like mouse down, even if we're using events (in case someone uses event)

# TODO -> Add more actions -> on_...()

# TODO -> Have widgets be disabled when not drawn...?

# TODO -> Automatic cache clearer (when it gets too big)

# TODO -> To change widget animation requires lambda: func(widget) -> can maybe simplify it?

# TODO -> Refactor/rewrite dynamic resize


def init():
    pgmenu.Theme = pgmenu.theme.Theme()
    pgmenu.Theme.load()

    pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_ARROW


def draw_all():
    # Save active or hovered widgets to be drawn on top
    top_widgets = []
    for widget in pgmenu.vars.widgets:
        if (widget.state == pgmenu.HOVERED or widget.state == pgmenu.ACTIVE) and pgmenu.system.widget_draw_priority:
            top_widgets.append(widget)
        else:
            widget.draw()

    for widget in top_widgets:
        widget.draw()


def update(events):
    # Hacky solution for getting base window size
    # Detects first call to update
    if pgmenu.vars.prev_window_size is None:
        pgmenu.vars.prev_window_size = pygame.display.get_window_size()

    # Format input, so we can iterate it if event is passed as input instead of events
    events = [events] if isinstance(events, pygame.event.Event) else events

    # Save mouse x, y pos to not call pygame.mouse.get_pos() multiple times
    pgmenu.vars.mouse_x, pgmenu.vars.mouse_y = pygame.mouse.get_pos()

    for widget in pgmenu.vars.widgets:

        if widget.state == pgmenu.DISABLED:
            continue

        # Checks that do not require events
        # Hover
        if widget.rect.collidepoint(pgmenu.vars.mouse_x, pgmenu.vars.mouse_y):

            widget.state = pgmenu.HOVERED
            widget.animation_on_hover()
            widget.on_hover()
            # Set cursor
            widget.request_cursor()

        # Standby action
        elif widget.state != pgmenu.ACTIVE:

            widget.state = pgmenu.NORMAL
            widget.animation_on_standby()
            widget.on_standby()

        for event in events:

            # Event for dynamic resize
            if event.type == pygame.VIDEORESIZE:

                if pgmenu.system.dynamic_resize or pgmenu.system.dynamic_coords:
                    # To reset prev_window_size
                    pgmenu.vars.videoresized = True

                    win_size = pygame.display.get_window_size()

                    x_factor = win_size[0] / pgmenu.vars.prev_window_size[0]
                    y_factor = win_size[1] / pgmenu.vars.prev_window_size[1]
                    factor = (x_factor + y_factor) / 2

                if pgmenu.system.dynamic_resize:
                    # Save size for factor in border_radius
                    prev_min_size = min(widget.size.inttuple)

                    if pgmenu.system.proportional_dynamic_resize:
                        widget.size = widget.size.inttuple[0] * factor, widget.size.inttuple[1] * factor
                    else:
                        widget.size = widget.size.inttuple[0] * x_factor, widget.size.inttuple[1] * y_factor

                    widget.border_radius = widget.border_radius.base_num * (min(widget.size.inttuple) / prev_min_size)

                if pgmenu.system.dynamic_coords:
                    if pgmenu.system.proportional_dynamic_coords:
                        widget.coords = widget.coords.inttuple[0] * factor, widget.coords.inttuple[1] * factor
                    else:
                        widget.coords = widget.coords.inttuple[0] * x_factor, widget.coords.inttuple[1] * y_factor

            # Other widget actions
            widget.update(event)

    # Reset window size for VIDEORESIZE
    if pgmenu.vars.videoresized:
        pgmenu.vars.prev_window_size = pygame.display.get_window_size()
        pgmenu.vars.videoresized = False

    # Set cursor
    if pgmenu.vars.user_cursor is None:
        pygame.mouse.set_cursor(pgmenu.vars.widget_cursor)
    else:
        pygame.mouse.set_cursor(pgmenu.vars.user_cursor)
    # Reset user_cursor to default
    pgmenu.request_cursor(None)
    # Set widget_cursor
    pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_ARROW


def request_cursor(cursor):
    pgmenu.vars.user_cursor = cursor
