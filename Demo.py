import pygame

import pgmenu

FPS = 200
BGCOLOR = (30, 30, 30)

pygame.init()
pygame.display.set_caption('Window')
screen = pygame.display.set_mode((1100, 900), pygame.RESIZABLE)
screen.fill(BGCOLOR)

clock = pygame.time.Clock()


def special():
    print(pgmenu.Checkbox.get(checkbox))
    pgmenu.Checkbox.statusOn(checkbox3)
    pgmenu.Button.enable(button3)


def show():
    print(pgmenu.Textbox.get(textbox))


def ungroup():
    pgmenu.Checkbox.ungroup(checkbox, checkbox2)


def disableFrame():
    pgmenu.Frame.disable(frame)


pgmenu.theme('BLUE')

button = pgmenu.Button.create((100, 100), activatedFunction=disableFrame)
button2 = pgmenu.Button.create((100, 200))
button3 = pgmenu.Button.create((100, 600), state='disabled', activatedFunction=ungroup)

checkbox = pgmenu.Checkbox.create((300, 200), activatedFunction=special)
checkbox2 = pgmenu.Checkbox.create((300, 350), activatedFunction=special, status=True)
checkbox3 = pgmenu.Checkbox.create((300, 500), 20, activatedFunction=special, state='disabled')

textbox = pgmenu.Textbox.create((200, 400), (200, 30), int, 3, limitInt=(0, 255), submitFunction=show)

image = pgmenu.Image.create(screen, 'plus.png', (400, 400), (200, 200))

frame = pgmenu.Frame.create(coords=(500, 150), dimensions=(500, 600))
pgmenu.Frame.add(frame, button, button2)

pgmenu.Frame.visuals(screen, frame, (40, 40, 40))

pgmenu.Button.visuals(screen, button, color=(255, 255, 255, 128), icon='plus.png')
pgmenu.Button.visuals(screen, button2, text='Button', color=(255, 255, 255), textColor=BGCOLOR, outlineWidth=5,
                      outlineColor=(200, 200, 200))
pgmenu.Button.visuals(screen, button3, text='Confirm', borderRadius=15)

pgmenu.Checkbox.visuals(screen, checkbox, text='Hey', textColor=(255, 255, 255), inflateActive=15)
pgmenu.Checkbox.visuals(screen, checkbox2, text='Ur mom', fgColor=BGCOLOR)
pgmenu.Checkbox.visuals(screen, checkbox3, text='Cascadia', textSize=50)

pgmenu.Checkbox.group(checkbox, checkbox2)

pgmenu.Textbox.visuals(screen, textbox, text='Hey ;)')

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Bye Bye!')
            running = False

    screen.fill(BGCOLOR)

    pgmenu.Frame.draw(frame)

    pgmenu.Button.draw(button)
    pgmenu.Button.draw(button2)
    pgmenu.Button.draw(button3)

    pgmenu.Checkbox.draw(checkbox)
    pgmenu.Checkbox.draw(checkbox2)
    pgmenu.Checkbox.draw(checkbox3)

    pgmenu.Textbox.draw(textbox)

    pgmenu.Image.draw(image)

    pgmenu.Text.write(screen, str(round(clock.get_fps())), (255, 255, 255), (15, 15), fontSize=15, centerX=False,
                      centerY=False)

    pygame.display.update()
    pgmenu.update(event)
    clock.tick(FPS)
