import pygame
import pgmenu


# NOTE -> Can run at 60 fps with 204 buttons (size (100, 50))


pygame.init()
pygame.display.set_caption('pgmenu')
screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 1000

for y in range(1):
    for x in range(1):
        button1 = pgmenu.button.Button(screen, (50 + 130 * x, 50 * (y + 1)), (100, 50), animation_duration=0.15)

while True:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    screen.fill((0, 0, 0))

    pgmenu.draw_all()

    pgmenu.text.write(screen, (20, 20), str(round(clock.get_fps())), 'VarelaRound.ttf', (255, 255, 255), 20, cache=True)

    pgmenu.update(events)
    pygame.display.flip()
    clock.tick(FPS)