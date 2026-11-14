import pgmenu


__all__ = ["add", "remove", "remove_all"]


# Adds widget to the system and update loop
def add(widget):
    pgmenu.vars.widgets_draw_order.append(widget)
    pgmenu.vars.widgets.append(widget)


def remove(widget):
    """Unregister a widget from the engine."""
    if widget in pgmenu.vars.widgets:
        pgmenu.vars.widgets.remove(widget)
    if widget in pgmenu.vars.widgets_draw_order:
        pgmenu.vars.widgets_draw_order.remove(widget)
    if hasattr(widget, "master") and isinstance(widget.master, pgmenu.widgets.Frame):
        widget.master.remove(widget)


def remove_all():
    pgmenu.vars.widgets_draw_order.clear()
    pgmenu.vars.widgets.clear()
