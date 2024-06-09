widgets = []
# Cache dicts
aarect_cached_surfaces = dict()
text_cached_surfaces = dict()
surface_cached_surfaces = dict()
# Formatted later in lib
Theme = None
# Cursor vars
widget_cursor = None
user_cursor = None
# Var to save previous window size for dynamic resize
prev_window_size = None
# Hacky solution for resetting prev_window_size
videoresized = False
# For fullscreen project, need closed off var
fs_window_size = None
# Cached mouse x, y positions, so pygame.mouse.get_pos() is not called multiple times
mouse_x, mouse_y = 0, 0
