import random
import pygame
import pgmenu


pygame.init()
screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
pygame.display.set_caption(f"Scroll Window {screen.get_size()}")
clock = pygame.time.Clock()
FPS = 1000

# Initiate movable plane, screen needed for blitting and drawing
window = pgmenu.projects.MovablePlaneWindow(screen)

# Generate random, colored rects to distribute along the plane
draw_range = 10000
for i in range(round(draw_range / 5)):
    # Spread out for easier data visualization
    x = random.randint(-draw_range, draw_range)
    y = random.randint(-draw_range, draw_range)
    width = random.randint(100, 200)
    height = random.randint(100, 200)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(128, 255))

    # Generate new surface with a rect
    globals()[f"rect{i}"] = pgmenu.draw.aarect(None, color, (0, 0, width, height), border_radius=0, debug=False)
    # Add surface, or blit, to window
    window.blit(globals()[f"rect{i}"], (x, y))

running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.VIDEORESIZE:
            pygame.display.set_caption(f'pgmenu {screen.get_size()}')

        # Add fullscreen controls
        screen = pgmenu.display.fullscreen_controls(screen, event)

        # Add window controls
        window.controls(event)

    screen.fill((0, 0, 0))

    # Draw all window surfaces
    window.draw()

    # Text for extra info
    # Fps
    pgmenu.text.write(screen, (20, 20), str(round(clock.get_fps())))
    x, y = pygame.mouse.get_pos()
    # Cursor's coordinates in the plane
    pgmenu.text.write(screen, (1000, 20), f"{round(x * window.relative_scale.num)}, {round(y * window.relative_scale.num)}", center_x = True)

    pgmenu.update(events)
    pygame.display.flip()
    clock.tick(FPS)
