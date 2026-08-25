from pgmenu.cache import Cache


# All widgets created during runtime
widgets = []
# Finer control over functions that need widgets
widgets_draw_order = []
# Widget types
widget_types = ("label",
                "surface",
                "frame",
                "button",
                "checkbox",
                "radiobutton")
# Global cache
cache = {
    "aarect": Cache(),
    "aarect_corner": Cache(),
    "text": Cache(),
    "surface": Cache(),
    "rect": Cache()
}
# Formatted later in lib
Theme = None
# Cursor vars
widget_cursor = None
user_cursor = None
# Var to save base window size for responsive resize
base_window_size = None
# Hacky solution for resetting prev_window_size
videoresized = False
# For fullscreen project, need closed off var
fs_window_size = None
# Cached mouse x, y positions, so pygame.mouse.get_pos() is not called multiple times
mouse_x, mouse_y = 0, 0
# For Menu module, to remember which menu is shown
current_menu_showed = None
