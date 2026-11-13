import pgmenu


__all__ = ["add", "remove", "remove_all"]


# Adds widget to the system and update loop
def add(widget):
    draw_order = pgmenu.vars.widgets_draw_order

    if isinstance(widget, pgmenu.widgets.Frame):
        master = widget.master
        if isinstance(master, pgmenu.widgets.Frame) and master in draw_order:
            # Nested frame: must draw before its parent so it is queued before the parent flushes
            draw_order.insert(draw_order.index(master), widget)
        else:
            draw_order.append(widget)
    else:
        # Regular widgets before any frame
        for i, w in enumerate(draw_order):
            if isinstance(w, pgmenu.widgets.Frame):
                draw_order.insert(i, widget)
                break
        else:
            draw_order.append(widget)

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
