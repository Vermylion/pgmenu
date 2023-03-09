import pygame

import pgmenu

FPS = 60

# Initiating window using pygame
pygame.init()
pygame.display.set_caption('Login Demo')
screen = pygame.display.set_mode((400, 900))
# Filling screen using theme-given background color
screen.fill(pgmenu.bgColor)
clock = pygame.time.Clock()

# pgmenu default mode is 'System'
# pgmenu default theme is Blue
pgmenu.Theme.mode('System') # 'System', 'Dark', 'Light'
pgmenu.Theme.set('BLUE') # 'BLUE', 'RED', 'GREEN', 'YELLOW', 'PURPLE', 'BLUE&BLACK', 'RED&BLACK', 'GREEN&BLACK', 'YELLOW&BLACK', 'PURPLE&BLACK'

def disable():
    pgmenu.Checkbox.disable(checkbox)
    pgmenu.Textbox.disable(textbox)
    pgmenu.Frame.disable(frame)

# Creating the widgets
button = pgmenu.Button.create((20, 100), activatedFunction = disable)
checkbox = pgmenu.Checkbox.create((20, 200))
textbox = pgmenu.Textbox.create((20, 300))
frame = pgmenu.Frame.create((20, 400))
text = pgmenu.Text.create(screen, 'pgmenu', (20, 20))

imageSize = pgmenu.Image.size('assets/tiger.png', resizeRatio = 7)
image = pgmenu.Image.create(screen, 'assets/tiger.png', (20, 650), dimensions = imageSize)

pgmenu.Frame.add(frame, text)

# Setting the visuals for the widgets
pgmenu.Button.visuals(screen, button)
pgmenu.Checkbox.visuals(screen, checkbox)
pgmenu.Textbox.visuals(screen, textbox)
pgmenu.Frame.visuals(screen, frame)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Bye Bye!')
            running = False

    # Refresh screen every frame
    screen.fill(pgmenu.bgColor)

    # Draw the widgets
    pgmenu.Button.draw(button)
    pgmenu.Checkbox.draw(checkbox)
    pgmenu.Textbox.draw(textbox)
    pgmenu.Frame.draw(frame)
    pgmenu.Text.draw(text)
    pgmenu.Image.draw(image)

    pygame.display.flip()
    # Update the widgets
    pgmenu.update(event)
    # Update clock
    clock.tick(FPS)
