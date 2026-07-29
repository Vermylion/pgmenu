import pygame
import pgmenu

pygame.init()

screen = pygame.display.set_mode((300, 300), pygame.RESIZABLE)
pygame.display.set_caption("Window")
clock = pygame.time.Clock()
fps = 1000



running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        screen = pgmenu.display.fullscreen_controls(screen, event)

    screen.fill((0, 0, 0))

    pgmenu.draw.aarect(screen, (60, 130, 230), (70, 70, 200, 70), width=5, inner_fill=(30, 100, 200), border_radius=3, border_top_left_radius=40)

    pgmenu.update(events)
    pygame.display.flip()
    clock.tick(fps)