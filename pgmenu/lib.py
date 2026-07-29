import time
import pygame
import pgmenu


# TODO -> Limit certain actions like mouse down, even if we're using events (in case someone uses event)

# TODO -> Add more actions -> on_...()

# TODO -> To change widget animation requires lambda: func(widget) -> can maybe simplify it? -> AnimateEvent


def init():
    pgmenu.Theme = pgmenu.theme.Theme()
    pgmenu.Theme.load()

    pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_ARROW


def _draw(*widgets):
    # Save active or hovered widgets to be drawn on top
    top_widgets = []
    for widget in widgets:

        if widget.state == pgmenu.HIDDEN:
            continue

        # Enact widget priority
        if pgmenu.FRAME or ((widget.state == pgmenu.HOVERED or widget.state == pgmenu.ACTIVE) and pgmenu.system.widget_draw_priority and widget.has_draw_priority):
            top_widgets.append(widget)
            continue

        widget.draw()

    for widget in top_widgets:
        widget.draw()


def draw_all():
    _draw(*pgmenu.vars.widgets_draw_order)


def update(events):
    # Hacky solution for getting base window size
    # Detects first call to update
    if pgmenu.vars.base_window_size is None:
        pgmenu.vars.base_window_size = pygame.display.get_window_size()

    # Format input, so we can iterate it if event is passed as input instead of events
    events = [events] if isinstance(events, pygame.event.Event) else events
    # Have always at least 1 event, so widget updates still get called every frame
    if len(events) == 0:
        events.append(pygame.event.Event(123))

    # Save mouse x, y pos to not call pygame.mouse.get_pos() multiple times
    pgmenu.vars.mouse_x, pgmenu.vars.mouse_y = pygame.mouse.get_pos()

    for widget in pgmenu.vars.widgets:

        if widget.state == pgmenu.DISABLED or widget.state == pgmenu.HIDDEN or widget._drawn == False:
            continue

        # Checks that do not require events
        # Hover action
        if widget.rect.collidepoint(pgmenu.vars.mouse_x, pgmenu.vars.mouse_y):

            if widget.state != pgmenu.ACTIVE:
                widget.state = pgmenu.HOVERED
                widget.on_hover()
                widget.animation_on_hover()

            # Set cursor
            widget.request_cursor()

        # Standby action
        elif widget.state != pgmenu.ACTIVE:

            widget.state = pgmenu.NORMAL
            widget.on_standby()
            widget.animation_on_standby()

        # Check events
        for event in events:
            pgmenu.resize.responsive_resize(widget, event)

            # Other widget actions
            widget.update(event)

        # Reset every widget's draw state, as widgets are normally not interacted with after update state
        widget._drawn = False

    pgmenu.resize.reset_videoresize()

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
