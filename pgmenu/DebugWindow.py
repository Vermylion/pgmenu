import pygame
import pgmenu


pygame.init()
pygame.display.set_caption('pgmenu')
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60

text = '''Hey\nHow's it going'''

text_surf = pgmenu.text.render(text, 'VarelaRound.ttf', (255, 255, 255), 120, italic=True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    screen.fill((0, 0, 0))
    screen.blit(text_surf, (500, 500))

    pygame.display.flip()
    clock.tick(FPS)