import pygame
import pgmenu


pygame.init()

screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
pygame.display.set_caption("Test window")
clock = pygame.time.Clock()
fps = 1000

# Test surface for "futuristic" surface
gradient = pygame.image.load("../tests/assets/gradient.png")

white = pygame.Surface(gradient.get_size(), pygame.SRCALPHA)
white.fill((255, 255, 255))
white.set_alpha(50)

gradient2 = gradient.copy()
gradient2.blit(white, (0, 0))

pygame.image.save(gradient2, "../tests/assets/gradient2.png")

glow_strength = 1

pgmenu.Theme.set(size=(100 + glow_strength * 2, 30 + glow_strength * 2),
                 border_radius=10 + glow_strength,
                 aa_strength=1,
                 width=1,
                 margin=glow_strength + 3,
                 animation_duration=0.1,
                 inside_aa_strength=1,
                 fill={'type': "image", 'path': "../tests/assets/gradient.png"},
                 outline_fill={'type': "image", 'path': "../tests/assets/gradient2.png"},
                 responsive_coords={'type': "variable", 'module': "pgmenu", 'variable': "PROPORTIONAL"})

icon = pgmenu.draw.aarect(None, (205, 42, 42), (0, 0, 32, 32), border_radius=5, width=0)

button1 = pgmenu.button.Button(screen, (250, 115), text="Play (Alt + C)", border_radius=2, border_top_left_radius=pgmenu.Theme.border_radius)
button2 = pgmenu.button.Button(screen, (355, 115), text="Stop (Alt + C)", border_radius=2, border_top_right_radius=pgmenu.Theme.border_radius)
button3 = pgmenu.button.Button(screen, (250, 150), text="Set Hotkeys", border_radius=2, border_bottom_left_radius=pgmenu.Theme.border_radius)
button4 = pgmenu.button.Button(screen, (355, 150), text="Help", icon=icon, margin=3, border_radius=2, border_bottom_right_radius=pgmenu.Theme.border_radius, state=pgmenu.DISABLED)

menu1 = pgmenu.menu.Menu(button1, button2, button4)
menu2 = pgmenu.menu.Menu(button3)
pgmenu.menu.show(menu1)

running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pgmenu.menu.show(menu2)

        screen = pgmenu.display.fullscreen_controls(screen, event)

    screen.fill((0, 0, 0))

    # pgmenu.draw_all()
    # menu1.draw()
    pgmenu.menu.draw()

    pgmenu.text.write(screen, (20, 20), str(round(clock.get_fps())))

    pgmenu.update(events)
    pygame.display.flip()
    clock.tick(fps)
