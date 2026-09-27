import pygame
import pgmenu
from pgmenu import animation

window = pgmenu.simple.PgmenuWindow((1000, 400))
window.fps = 1000
screen = window.screen

icon = pygame.image.load("../tests/assets/fox.jpeg")

button1 = pgmenu.button.Button(screen, (50, 50), (150, 150), icon=icon, text="", margin=30, border_radius=74, animation_duration=0.5, animation_curve=pgmenu.animation.elastic, animation_scale=1.15)
button2 = pgmenu.button.Button(screen, (220, 50), (150, 150), icon=icon, text="", margin=30, border_radius=74, animation_duration=0.5, animation_curve=pgmenu.animation.elastic, animation_scale=1.15)
button3 = pgmenu.button.Button(screen, (390, 50), (150, 150), icon=icon, text="", margin=30, border_radius=74, animation_duration=0.5, animation_curve=pgmenu.animation.elastic, animation_scale=1.15)
button4 = pgmenu.button.Button(screen, (560, 50), (150, 150), icon=icon, text="", margin=30, border_radius=74, animation_duration=0.5, animation_curve=pgmenu.animation.elastic, animation_scale=1.15)
button5 = pgmenu.button.Button(screen, (730, 50), (150, 150), icon=icon, text="", margin=30, border_radius=74, animation_duration=0.5, animation_curve=pgmenu.animation.elastic, animation_scale=1.15)


def loop():
    pgmenu.text.write(screen, (20, 20), str(round(window.clock.get_fps())))


window.loop(loop)
