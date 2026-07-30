import pygame
import pgmenu
import math

pygame.init()

screen = pygame.display.set_mode((300, 300), pygame.RESIZABLE)
pygame.display.set_caption("Window")
clock = pygame.time.Clock()
fps = 1000

# label = pgmenu.label.Label(screen, (80, 70), "Button", (255, 255, 255), 22, center_x=True, center_y=True)
text_base = pgmenu.text.render("Button", (255, 255, 255), 22)
text_w, text_h = text_base.get_size()
text_size = pgmenu.animation.AnimateTuple((text_w, text_w*1.2), (text_h, text_h*1.2))
text = pgmenu.text.render("Button", (255, 255, 255), round(22*1.2))

rect_size = pgmenu.animation.AnimateTuple((100, 120), (30, 36))
border_radius = pgmenu.animation.Animate(11, 11*1.2)
update_direction = pgmenu.BACKWARD

running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                update_direction = pgmenu.FORWARD

            if event.key == pygame.K_b:
                update_direction = pgmenu.BACKWARD

        screen = pgmenu.display.fullscreen_controls(screen, event)

    screen.fill((0, 0, 0))

    coords = pgmenu.position.center_coords(rect_size, (80, 70, 0, 0))

    # label.size.update(update_direction)
    if pygame.Rect(*coords, *rect_size).collidepoint(pygame.mouse.get_pos()):
        rect_size.update(pgmenu.FORWARD)
        text_size.update(pgmenu.FORWARD)
        border_radius.update(pgmenu.FORWARD)
    else:
        rect_size.update(pgmenu.BACKWARD)
        text_size.update(pgmenu.BACKWARD)
        border_radius.update(pgmenu.BACKWARD)

    pgmenu.draw.aarect(screen, (60, 130, 230), (*coords, *rect_size.int_tuple), border_radius=border_radius)
    pgmenu.draw_all()
    pgmenu.update(events)

    text_surf = pygame.transform.smoothscale(text, text_size)

    coords = pgmenu.position.center_coords(text_size, (80, 70, 0, 0))
    screen.blit(text_surf, coords)

    pgmenu.draw_all()
    pgmenu.update(events)
    pygame.display.flip()
    clock.tick(fps)