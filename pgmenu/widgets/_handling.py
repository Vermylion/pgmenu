import pgmenu


__all__ = ["add", "remove", "remove_all"]


# Adds widget to the system and update loop
def add(widget):
    # Sets Frame objects at the end of the draw order so other surfaces have time to blit on to them
    def insert_before_frames():
        for i in range(len(pgmenu.vars.widgets_draw_order)):
            if pgmenu.vars.widgets_draw_order[i].type == pgmenu.FRAME:
                pgmenu.vars.widgets_draw_order.insert(i, widget)
                return
        pgmenu.vars.widgets_draw_order.append(widget)

    if widget.type == pgmenu.FRAME:
        # Frames always go at the true end, so multiple frames keep their original (e.g. nesting) order relative to each other
        pgmenu.vars.widgets_draw_order.append(widget)
    else:
        # Regular widgets must be inserted before any existing Frame, otherwise they'd draw after it and the Frame couldn't have them blitted onto it yet
        insert_before_frames()

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
