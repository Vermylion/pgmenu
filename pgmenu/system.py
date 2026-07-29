# Collection of important variables that can impact the functioning of the library
# Meant to be accessed, and modified, by the user

# Whether active or hovered widgets are drawn on top
widget_draw_priority = True
# Max cache size per cached dict
# Cache size 100 equals to about 150mb of ram added
# Keep in mind this is 100 per cache, and there are 5 cache total
# FIXME -> 5 cache dict may be too much; divide max_cache_size per cache dict?
max_cache_size = 300 # Min value of 1
