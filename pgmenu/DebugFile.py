import pygame
import pgmenu


window = pgmenu.simple.PgmenuWindow((400, 400))
window.fps = 1000
screen = window.screen

icon = pygame.image.load("../tests/assets/fox.jpeg")

pgmenu.Theme.load("MODERN")

button = pgmenu.button.Button(screen, (35, 350), (330, 30), text="Button", icon=icon, margin=3)

button.responsive_size = pgmenu.STRETCH
button.responsive_coords = pgmenu.STRETCH


def loop():
    pygame.display.set_caption(f"pgmenu {screen.get_size()}, {button.size.int_tuple}, {button.coords.int_tuple}")
    pgmenu.text.write(screen, (20, 20), str(round(window.clock.get_fps())))


window.loop(loop)
