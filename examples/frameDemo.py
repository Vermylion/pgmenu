import pygame

import pgmenu

FPS = 60

# Initiating window using pygame
pygame.init()
pygame.display.set_caption('Frame Demo')
screen = pygame.display.set_mode((400, 700))
# Filling screen using theme-given background color
screen.fill(pgmenu.getVar('bgColor'))
clock = pygame.time.Clock()

# pgmenu default mode is 'System'
# pgmenu default theme is Blue
pgmenu.Theme.mode('System') # 'System', 'Dark', 'Light'
pgmenu.Theme.set('BLUE') # 'BLUE', 'RED', 'GREEN', 'YELLOW', 'PURPLE', 'BLUE&BLACK', 'RED&BLACK', 'GREEN&BLACK', 'YELLOW&BLACK', 'PURPLE&BLACK'

def changeState():
    if pgmenu.Checkbox.get(checkbox3) == True:
        pgmenu.Frame.enable(frame)
    if pgmenu.Checkbox.get(checkbox3) == False:
        pgmenu.Frame.disable(frame)
    
def moveWidget():
    if pgmenu.Checkbox.get(checkbox) == True:
        pgmenu.Text.modify(text, coords = (40, 40))
        pgmenu.Button.modify(button, coords = (120, 100))
    if pgmenu.Checkbox.get(checkbox) == False:
        pgmenu.Text.modify(text, coords = (20, 20))
        pgmenu.Button.modify(button, coords = (20, 70))
        
def moveFrame():
    if pgmenu.Checkbox.get(checkbox2) == True:
        pgmenu.Frame.modify(frame, coords = (150, 450))
    if pgmenu.Checkbox.get(checkbox2) == False:
        pgmenu.Frame.modify(frame, coords = (20, 450))

# Creating the widgets
checkbox3 = pgmenu.Checkbox.create((20, 150), activatedFunction = changeState, status = True)
checkbox = pgmenu.Checkbox.create((20, 250), activatedFunction = moveWidget)
checkbox2 = pgmenu.Checkbox.create((20, 350), activatedFunction = moveFrame)
frame = pgmenu.Frame.create((20, 450))

button = pgmenu.Button.create((20, 70))
text = pgmenu.Text.create(screen, 'pgmenu', (20, 20))

pgmenu.Frame.add(frame, button, text)

# Setting the visuals for the widgets
pgmenu.Checkbox.visuals(screen, checkbox3, text = 'Change State')
pgmenu.Checkbox.visuals(screen, checkbox, text = 'Move Widget')
pgmenu.Checkbox.visuals(screen, checkbox2, text = 'Move Frame')
pgmenu.Frame.visuals(screen, frame)

pgmenu.Button.visuals(screen, button)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Bye Bye!')
            running = False

    # Refresh screen every frame
    screen.fill(pgmenu.getVar('bgColor'))

    # Draw the widgets
    pgmenu.Checkbox.draw(checkbox3)
    pgmenu.Checkbox.draw(checkbox)
    pgmenu.Checkbox.draw(checkbox2)
    pgmenu.Frame.draw(frame)
    
    pgmenu.Text.draw(text)
    pgmenu.Button.draw(button)

    pygame.display.flip()
    # Update the widgets
    pgmenu.update(event)
    # Update clock
    clock.tick(FPS)