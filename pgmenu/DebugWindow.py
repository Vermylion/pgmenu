import pygame
import pgmenu


# NOTE -> Can run at 60 fps with 204 buttons (size (100, 50))


pygame.init()
screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
pygame.display.set_caption(f'pgmenu {screen.get_size()}')
clock = pygame.time.Clock()
FPS = 1000


def animation_standby(widget):
    widget.fill.backward()
    widget.fill.update()


def animation_hover(widget):
    widget.fill.forward()
    widget.fill.update()


def animation_standby_fading(widget):
    widget.transparency.backward()
    widget.transparency.update()


def animation_hover_fading(widget):
    widget.transparency.forward()
    widget.transparency.update()


def animation_standby_discord(widget):
    animation_standby(widget)

    widget.border_radii.backward()
    widget.border_radii.update()


def animation_hover_discord(widget):
    animation_hover(widget)

    widget.border_radii.forward()
    widget.border_radii.update()


button_left_arrow = pgmenu.button.Button(screen, (150, 75), (175, 80), (0, 123, 255), border_radius=40, text="<", animation_scale=0.8, animation_duration=0.2, no_animation=True, animation_on_standby=lambda: animation_standby(button_left_arrow), animation_on_hover=lambda: animation_hover(button_left_arrow))
button_right_arrow = pgmenu.button.Button(screen, (755, 75), (175, 80), (0, 123, 255), border_radius=40, text=">", animation_scale=0.8, animation_duration=0.2, no_animation=True, animation_on_standby=lambda: animation_standby(button_right_arrow), animation_on_hover=lambda: animation_hover(button_right_arrow))
button_done = pgmenu.button.Button(screen, (150, 565), (780, 80), (220, 53, 69), border_radius=40, text="Done", animation_scale=0.8, animation_duration=0.2, no_animation=True, animation_on_standby=lambda: animation_standby(button_done), animation_on_hover=lambda: animation_hover(button_done))

button_fading = pgmenu.button.Button(screen, (300, 300), (175, 60), border_radius=10, fill=(53, 55, 60), text="Squarycoop", margin=5, transparency=1, text_transparency=255, no_animation=True, animation_scale=255, animation_on_standby=lambda: animation_standby_fading(button_fading), animation_on_hover=lambda: animation_hover_fading(button_fading))

button_discord = pgmenu.button.Button(screen, (600, 300), (150, 150), border_radius=75, fill=pgmenu.animation.AnimateColor((53, 55, 60), (88, 101, 242), 0.2), text="MW", margin=30, no_animation=True, animation_scale=0.6, animation_duration=0.2, animation_on_standby=lambda: animation_standby_discord(button_discord), animation_on_hover=lambda: animation_hover_discord(button_discord))

button_normal = pgmenu.button.Button(screen, (200, 200))
# Text formatting
# text_fps = pgmenu.text.Text(screen, (15, 15), size=20)
# text_pos = pgmenu.text.Text(screen, (670, 15), size=20, center_x=True)

running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.VIDEORESIZE:
            pygame.display.set_caption(f'pgmenu {screen.get_size()}')

        screen = pgmenu.projects.fullscreen_controls(screen, event)

    screen.fill((43, 45, 49))

    # text_fps.text = str(round(clock.get_fps()))
    x, y = pygame.mouse.get_pos()
    # text_pos.text = f"{x} ; {y}"

    pgmenu.draw_all()

    pgmenu.text.write(screen, (15, 15), str(round(clock.get_fps())), size=20)
    # pgmenu.text.write(screen, (670, 15), f"{x}, {y}", size=20, center_x=True)

    pgmenu.update(events)
    pygame.display.flip()
    clock.tick(FPS)
