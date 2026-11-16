import pygame
import pgmenu

window = pgmenu.simple.PgmenuWindow((1080, 720))
window.fps = 1000
screen = window.screen

size = (900, 600)

textarea = pgmenu.widgets.TextArea(screen, pgmenu.position.center_coords(size, (0, 0, *screen.get_size())), size, margin=25)
scrollbar_x = pgmenu.widgets.Scrollbar(textarea, pgmenu.BOTTOM)
scrollbar_y = pgmenu.widgets.Scrollbar(textarea, pgmenu.RIGHT)


def loop():
    pgmenu.text.write(screen, (20, 20), str(round(window.clock.get_fps())))


window.loop(loop)
