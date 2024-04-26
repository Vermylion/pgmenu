import pygame
import pgmenu


# TODO -> Might need recursion of event instead of events

# TODO -> Limit certain actions like mouse down, even if we're using events (in case someone uses event)

# TODO -> Add more actions -> on_...()

# TODO -> Have widgets be disabled when not drawn...?

# TODO -> Automatic cache clearer (when it gets too big)

# TODO -> Separate update function for each widget? Might impact performance


def init():
    pgmenu.vars.Theme = pgmenu.theme.Theme()

    pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_ARROW


def draw_all():
    # Save active or hovered widgets to be drawn on top
    top_widgets = []
    for widget in pgmenu.vars.widgets:
        if (widget.state == pgmenu.HOVERED or widget.state == pgmenu.ACTIVE) and pgmenu.widget_draw_priority:
            top_widgets.append(widget)
        else:
            widget.draw()

    for widget in top_widgets:
        widget.draw()


def update(events):
    # Detect mouse for hover over widgets
    for widget in pgmenu.vars.widgets:

        if widget.state == pgmenu.DISABLED:
            continue

        # Detect mouse collisions
        x, y = pygame.mouse.get_pos()
        if widget.rect.collidepoint(x, y):

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

        # Detect pygame actions
        # Format input, so we can iterate it if event is passed as input instead of events
        events = [events] if isinstance(events, pygame.event.Event) else events

        for event in events:

            # Update only current or selected widget
            if widget.state == pgmenu.HOVERED or widget.state == pgmenu.ACTIVE:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    widget.state = pgmenu.ACTIVE
                    widget.animation_on_press()
                    widget.on_press()

                if event.type == pygame.MOUSEBUTTONUP:
                    widget.animation_on_release()
                    widget.on_release()

                if event.type == pygame.KEYDOWN:
                    widget.animation_on_key_press(event.key)
                    widget.on_key_press(event.key)

                if event.type == pygame.KEYUP:
                    widget.animation_on_key_release(event.key)
                    widget.on_key_release(event.key)

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
