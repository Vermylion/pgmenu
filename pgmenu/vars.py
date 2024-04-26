widgets = []

aarect_cached_surfaces = dict()

text_cached_surfaces = dict()

# Formatted later in lib
Theme = None

widget_cursor = None
user_cursor = None

# Var called by user -> imported in __init__
widget_draw_priority = True # TODO -> Separate system file? -> pgmenu.system.widget_draw_priority = False
