import random
import time
import pygame
import pgmenu


NUM_WIDGETS = 800  # push this up until things break
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
MIN_SIZE = 50
MAX_SIZE = 800

pgmenu.system.max_cache_size = NUM_WIDGETS

pygame.init()

screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
pygame.display.set_caption("Window")
clock = pygame.time.Clock()
fps = 1000

widgets = []

def make_label():
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    h = 32  # h = random.randint(MIN_SIZE, MAX_SIZE)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = random.randint(0, 255)
    color = (r, g, b, a)
    
    label = pgmenu.label.Label(screen, (x, y), "Label", color, h)

    return label

def make_surface():
    def on_resize(coords, size):
        ...
        # surface.surface = pgmenu.draw.aarect(None, color, (*coords, *size), antialiasing=True, debug=True)

    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    w = 100 # w = random.randint(MIN_SIZE, MAX_SIZE)
    h = 32 # h = random.randint(MIN_SIZE, MAX_SIZE)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = random.randint(0, 255)
    color = (r, g, b, a)

    rect = pgmenu.draw.aarect(None, color, (x, y, w, h), antialiasing=True, debug=True)

    surface = pgmenu.surface.Surface(
        screen,
        rect,
        (x, y),
        on_resize=lambda s=None: on_resize(surface.coords.int_tuple, surface.size.int_tuple)
    )
    return surface

for i in range(NUM_WIDGETS):
    widgets.append(make_surface() if i % 2 == 0 else make_label())

running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        screen = pgmenu.display.fullscreen_controls(screen, event)

    screen.fill(pgmenu.Theme.bgcolor)

    pgmenu.draw_all()

    pgmenu.text.write(screen, (20, 20), str(round(clock.get_fps())))

    win_size = pygame.display.get_window_size()
    pygame.display.set_caption(f"Window {win_size[0]}x{win_size[1]}")
    pgmenu.update(events)
    pygame.display.flip()
    clock.tick(fps)