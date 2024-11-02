import pygame
import pgmenu


window = pgmenu.simple.PgmenuWindow((400, 400))
window.fps = 1000
screen = window.screen

icon = pygame.image.load("../tests/assets/fox.jpeg")

pgmenu.Theme.load("MODERN")

button = pgmenu.button.Button(screen, (100, 100), (200, 60), border_radius=12, icon=icon, margin=3)

button.responsive_size = pgmenu.PROPORTIONAL
button.responsive_coords = pgmenu.STRETCH

window.actions(lambda: pygame.display.set_caption(f"pgmenu {screen.get_size()}, {button.size.inttuple}, {button.coords.inttuple}"))
window.actions(lambda: pgmenu.text.write(screen, (20, 20), str(round(window.clock.get_fps()))))

window.loop()
