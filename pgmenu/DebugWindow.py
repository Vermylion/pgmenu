import pgmenu
import pygame
import time
import random

from pgmenu import toggleswitch
from pgmenu.animation import Animate

pygame.init()

win_size = (1080, 720)
screen = pygame.display.set_mode(win_size, pygame.RESIZABLE)
pygame.display.set_caption("Window")
clock = pygame.time.Clock()
fps = 1000

# pgmenu.AnimationTheme.load("SIMPLE")

gradient = pygame.image.load("../tests/assets/gradient.png")
gradient2 = pygame.image.load("../tests/assets/gradient2.png")
pinksky = pygame.image.load("../tests/assets/pinksky.jpg")
pinksky = pygame.transform.smoothscale(pinksky, win_size)


def make_animated_surf(size):
    rect = pgmenu.draw.aarect(None, (63, 68, 72), (0, 0, *size))
    rect2 = pgmenu.draw.aarect(None, (68, 72, 77), (0, 0, *size))
    return pgmenu.animation.AnimateSurface(rect, rect2, 0, 255, 0.3, pgmenu.animation.circ)

def on_resize(size):
    surface.surface = make_animated_surf(size)

def on_hover():
    surface.surface.update(pgmenu.FORWARD)

def on_standby():
    surface.surface.update(pgmenu.BACKWARD)


def m_animation_on_standby():
    label.color.update(pgmenu.BACKWARD)

def m_animation_on_hover():
    label.color.update(pgmenu.FORWARD)
    pgmenu.request_cursor(pygame.SYSTEM_CURSOR_HAND)


def button_action():
    print("button pressed")


pgmenu.Theme.set(**{'widget_disable_default_animation': False})


frame = pgmenu.frame.Frame(screen, pgmenu.position.center_coords((600, 450), (0, 0, 1080, 720)), (600, 450))

surface = pgmenu.surface.Surface(frame, make_animated_surf((200, 100)), (300, 275), on_resize=lambda: on_resize(surface.size.int_tuple), on_hover=on_hover, on_standby=on_standby, state=pgmenu.NORMAL)

color2 = pgmenu.animation.AnimateTuple(*((250, 50), (50, 50), (50, 250)), duration=0.5, curve=pgmenu.animation.circ)
label = pgmenu.label.Label(frame, (250, 150), color=color2, size=100, animation_scale=1.4, animation_duration=0.15,
                           animation_on_standby=m_animation_on_standby, animation_on_hover=m_animation_on_hover,
                           responsive_size=pgmenu.PROPORTIONAL)

icon = pgmenu.draw.aarect(None, (255, 0, 0), (0, 0, 50, 50))
button = pgmenu.button.Button(frame, (300, 50), (100, 30), icon=icon, animation_duration=0.1, text="Button", margin=3, text_italic=False, text_bold=False, animation_curve=pgmenu.animation.circ, on_release=button_action)

checkbox1 = pgmenu.checkbox.Checkbox(frame, (50, 50), text_side=pgmenu.RIGHT)
checkbox2 = pgmenu.checkbox.Checkbox(frame, (50, 100), text_side=pgmenu.RIGHT)

radiobutton1 = pgmenu.radiobutton.Radiobutton(frame, (50, 175))
radiobutton2 = pgmenu.radiobutton.Radiobutton(frame, (50, 225))
radiobutton3 = pgmenu.radiobutton.Radiobutton(frame, (50, 275))
radiogroup = pgmenu.radiobutton.RadioGroup(radiobutton1, radiobutton2, radiobutton3)

menu = pgmenu.menu.Menu(frame, radiobutton1, radiobutton2, radiobutton3)
pgmenu.menu.show(menu)

toggleswitch = pgmenu.toggleswitch.ToggleSwitch(frame, (50, 350), (60, 30), toggle_direction=pgmenu.RIGHT)

size_animated = pgmenu.animation.AnimateTuple((100, 130), (50, 50*1.3), duration=0.6)
pgmenu.animation.run_animation(size_animated, pgmenu.FORWARD, loop=pgmenu.YOYO)

go = False
start = time.time()
incr = 0
debug=0

running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                frame.size = (450, 400)

            if event.key == pygame.K_b:
                frame.coords = (50, 50)

            if event.key == pygame.K_c:
                radiobutton1.selected = False

            if event.key == pygame.K_d:
                frame.border_radius = 30

            if event.key == pygame.K_ASTERISK:
                go = True if not go else False

            if event.key == pygame.K_BACKSPACE:
                screen = pygame.display.set_mode(win_size, pygame.RESIZABLE)
                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE))

        screen = pgmenu.display.fullscreen_controls(screen, event)

    screen.fill(pgmenu.Theme.bgcolor)
    # screen.blit(pinksky, (0,0))

    if go and (time.time() - start) >= 0.05:
        start = time.time()
        incr += 1
        w = random.randint(10, 3000)
        h = random.randint(10, 3000)

        if incr % 100 == 0:
            w, h = win_size
            debug = incr

        if incr == debug + 1:
            print(debug, "| Sizes:", *[w.size for w in pgmenu.vars.widgets], "| Coords:", *[w.coords for w in pgmenu.vars.widgets])
            print("Frame top left radius:", frame.border_top_left_radius)

        screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE))

    pgmenu.draw.aarect(screen, (200, 50, 50), (*pgmenu.position.center_coords(size_animated.tuple, (450, 50, *size_animated.base_tuple)), *size_animated.int_tuple))

    pgmenu.draw_all()
    # pgmenu.menu.draw()

    pgmenu.text.write(screen, (20, 20), str(round(clock.get_fps())))
    # if pgmenu.vars.kb_selected_widget:
    #     pgmenu.text.write(screen, (300, 20), str(checkbox1.check_transparency))

    win_size = pygame.display.get_window_size()
    pygame.display.set_caption(f"Window {win_size[0]}x{win_size[1]}")
    pgmenu.update(events)
    pygame.display.flip()
    clock.tick(fps)
