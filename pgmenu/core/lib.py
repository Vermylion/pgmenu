import pygame
import pgmenu
from pgmenu.base import mixins


__all__ = ["init", "draw_all", "update", "request_cursor"]


# TODO -> Limit certain actions like mouse down, even if we're using events (in case someone uses event)

# TODO -> Add more actions -> on_...()

# TODO -> To change widget animation requires lambda: func(widget) -> can maybe simplify it? -> AnimateEvent


def init():
    pgmenu.Theme = pgmenu.theme.Theme()
    pgmenu.Theme.load()

    pgmenu.AnimationTheme = pgmenu.theme.AnimationTheme()
    pgmenu.AnimationTheme.load()

    pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_ARROW


def _draw(*widgets):
    # Save active or hovered widgets to be drawn on top
    top_widgets = []
    for widget in widgets:

        if widget.state == pgmenu.HIDDEN:
            continue

        # Enact widget priority
        if widget.type == pgmenu.FRAME or ((widget.state == pgmenu.HOVERED or widget.state == pgmenu.ACTIVE) and pgmenu.system.WIDGET_DRAW_PRIORITY and widget.has_draw_priority):
            top_widgets.append(widget)
            continue

        widget.draw()

    for widget in top_widgets:
        widget.draw()


def draw_all():
    _draw(*pgmenu.vars.widgets_draw_order)


def _update_cursor():
    if pgmenu.vars.user_cursor is None:
        pygame.mouse.set_cursor(pgmenu.vars.widget_cursor)
    else:
        pygame.mouse.set_cursor(pgmenu.vars.user_cursor)
    # Reset user_cursor to default
    pgmenu.request_cursor(None)
    # Set widget_cursor
    pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_ARROW


def _widget_kb_selection():
    # Actionable widgets keyboard selection
    if pygame.key.get_just_released()[pgmenu.system.KB_SELECTION]:

        if pgmenu.vars.kb_selected_widget is None:
            pgmenu.vars.kb_selected_widget = pgmenu.vars.widgets[0]

        current, widgets = pgmenu.vars.kb_selected_widget, pgmenu.vars.widgets

        for i in range(1, len(widgets) + 1):
            widget = widgets[(widgets.index(current) + i) % len(widgets)]

            if isinstance(widget, mixins.ActionableMixin):
                pgmenu.vars.kb_selected_widget = widget
                break


def update(events):
    # Hacky solution for getting base window size
    # Detects first call to update
    if pgmenu.vars.base_window_size is None:
        pgmenu.vars.base_window_size = pygame.display.get_window_size()

    # Format input, so we can iterate it if event is passed as input instead of events
    events = [events] if isinstance(events, pygame.event.Event) else list(events)
    # General idle event for update logic
    events.append(pygame.event.Event(pgmenu.IDLE_EVENT))

    # Save mouse x, y pos to not call pygame.mouse.get_pos() multiple times
    pgmenu.vars.mouse_x, pgmenu.vars.mouse_y = pygame.mouse.get_pos()

    for widget in pgmenu.vars.widgets:

        if widget.state in (pgmenu.DISABLED, pgmenu.HIDDEN) or not widget._drawn:
            continue

        # Mouse hover
        hovered = widget.rect.collidepoint(pgmenu.vars.mouse_x, pgmenu.vars.mouse_y)

        if hovered:
            widget.request_cursor()

        # State assignment
        if widget.state != pgmenu.ACTIVE:
            if hovered or pgmenu.vars.kb_selected_widget == widget:
                widget.state = pgmenu.HOVERED
            else:
                widget.state = pgmenu.NORMAL

        # State callbacks
        if widget.state == pgmenu.NORMAL:
            widget.on_standby()
            widget.animation_on_standby()

        elif widget.state == pgmenu.HOVERED:
            widget.on_hover()
            widget.animation_on_hover()

        elif widget.state == pgmenu.ACTIVE:
            widget.on_active()
            widget.animation_on_active()

        # Check events
        for event in events:
            pgmenu.resize.responsive_resize(widget, event)

            # Deselect kb actionable widget
            if event.type in pgmenu.MOUSE_EVENTS:
                pgmenu.vars.kb_selected_widget = None

            # Other widget actions
            widget.update(event)

        # Reset every widget's draw state, as widgets are normally not interacted with after update state
        widget._drawn = False

    pgmenu.animation.update_running_animations()

    pgmenu.resize.reset_videoresize()

    if pgmenu.system.KB_SELECTION:
        _widget_kb_selection()

    # Set cursor
    _update_cursor()


def request_cursor(cursor):
    pgmenu.vars.user_cursor = cursor
