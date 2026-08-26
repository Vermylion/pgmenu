import pygame
import random
import time
import pgmenu

# ------------------ CONFIG ------------------
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
NUM_WIDGETS = 100        # increase until performance drops
RESIZE_RATIO = 0.1        # % of widgets resized each frame
MIN_SIZE = 50
MAX_SIZE = 800
# --------------------------------------------

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pygame Rect Stress Test")

clock = pygame.time.Clock()


class Widget:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.w = random.randint(MIN_SIZE, MAX_SIZE)
        self.h = random.randint(MIN_SIZE, MAX_SIZE)

        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),  # alpha < 255
        )

        self.surface = None
        self.prev_window_size = pygame.display.get_window_size()
        self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, self.color, (0, 0, self.w, self.h), border_radius=50)

    def rebuild_surface(self):
        """Create a per-pixel alpha surface and draw rect onto it"""
        self.surface = pygame.transform.smoothscale(self.surface, (self.w, self.h))
        # self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        # pygame.draw.rect(self.surface, self.color, (0, 0, self.w, self.h), border_radius=50)
        self._last_size = (self.w, self.h)

    def resize(self):
        win_size = pygame.display.get_window_size()

        # Percentage of the screen the widget covers
        widget_w_coverage = self.w / self.prev_window_size[0]
        widget_h_coverage = self.h / self.prev_window_size[1]

        self.w = round(win_size[0] * widget_w_coverage)
        self.h = round(win_size[1] * widget_h_coverage)

        self.rebuild_surface()

        self.prev_window_size = win_size

    def draw(self, target):
        target.blit(self.surface, (self.x, self.y))


# Create widgets
widgets = [Widget() for _ in range(NUM_WIDGETS)]

# FPS tracking
start_time = time.time()
frames = 0

running = True
while running:
    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            for w in widgets:
                w.resize()

    # --- STRESS: RANDOM RESIZES ---
    # resize_count = int(NUM_WIDGETS * RESIZE_RATIO)
    # for w in random.sample(widgets, resize_count):
    #     w.resize()

    # --- DRAW ---
    screen.fill((0, 0, 0))

    for w in widgets:
        w.draw(screen)

    pgmenu.text.write(screen, (20, 20), str(round(clock.get_fps())))

    pygame.display.flip()

    # --- FPS TRACKING ---
    frames += 1
    clock.tick(60)

    if time.time() - start_time >= 5:
        fps = frames / 5
        print(f"FPS: {fps:.2f} | Widgets: {NUM_WIDGETS}")
        frames = 0
        start_time = time.time()

pygame.quit()