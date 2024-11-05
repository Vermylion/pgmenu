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


def clear_cache(var_name):
    setattr(pgmenu.vars, var_name, dict())


# FIXME -> Cache clearer doesn't seem to be doing anything
def auto_cache_clearer():
    if pgmenu.vars.cache_duration is not None:
        curr_time = time.time()

        if pgmenu.vars.cache_start == 0:
            pgmenu.vars.cache_start = curr_time

        if curr_time >= pgmenu.vars.cache_start + pgmenu.vars.cache_duration:
            pgmenu.vars.cache_start = curr_time
            print("Cleared cache")

            for cache_var in pgmenu.vars.cache:
                print(getattr(pgmenu.vars, cache_var))
                # clear_cache(cache_var)

            pgmenu.vars.aarect_cached_surfaces = dict()
            pgmenu.vars.text_cached_surfaces = dict()
            pgmenu.vars.surface_cached_surfaces = dict()

            for cache_var in pgmenu.vars.cache:
                print(getattr(pgmenu.vars, cache_var))


def _draw(*widgets):
    # Save active or hovered widgets to be drawn on top
    top_widgets = []
    for widget in pgmenu.vars.widgets_draw_order:
        if widget in widgets:
            if (widget.state == pgmenu.HOVERED or widget.state == pgmenu.ACTIVE) and pgmenu.system.widget_draw_priority and widget.has_draw_priority:
                top_widgets.append(widget)

            else:
                widget.draw()

    for widget in top_widgets:
        widget.draw()


def draw_all():
    _draw(*pgmenu.vars.widgets)


def update(events):
    # Hacky solution for getting base window size
    # Detects first call to update
    if pgmenu.vars.prev_window_size is None:
        pgmenu.vars.prev_window_size = pygame.display.get_window_size()

    # Manage cache
    # auto_cache_clearer()

    # Format input, so we can iterate it if event is passed as input instead of events
    events = [events] if isinstance(events, pygame.event.Event) else events

    # Save mouse x, y pos to not call pygame.mouse.get_pos() multiple times
    pgmenu.vars.mouse_x, pgmenu.vars.mouse_y = pygame.mouse.get_pos()

    for widget in pgmenu.vars.widgets:

        if widget.state == pgmenu.DISABLED or widget._drawn == False:
            continue

        # Checks that do not require events
        # Hover action
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
