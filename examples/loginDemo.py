import pygame

import pgmenu

FPS = 60

# Initiating window using pygame
pygame.init()
pygame.display.set_caption('Login Demo')
screen = pygame.display.set_mode((700, 700))
# Filling screen using theme-given background color
screen.fill(pgmenu.bgColor)
clock = pygame.time.Clock()

def submit():
    # Check if checkbox of id agreementCheckbox has been checked (aka equal to True)
    if pgmenu.Checkbox.get(agreementCheckbox) == True:
        print('Username:', pgmenu.Textbox.get(usernameTextbox))
        print('Password:', pgmenu.Textbox.get(passwordTextbox))

def checkboxType(id):
    print(pgmenu.Checkbox.get(id))

# pgmenu default mode is 'System' ('System', 'Dark', 'Light')
# pgmenu default theme is Blue ('BLUE', 'RED', 'GREEN', 'YELLOW', 'PURPLE', 'BLUE&BLACK', 'RED&BLACK', 'GREEN&BLACK', 'YELLOW&BLACK', 'PURPLE&BLACK')
## pgmenu.Theme.mode('System')
## pgmenu.Theme.set('BLUE')

# Creating the widgets
loginFrame = pgmenu.Frame.create((100, 100), (500, 500))

loginText = pgmenu.Text.create(screen, 'Login Demo', (250, 20), textSize = 45, centerX = True)

usernameText = pgmenu.Text.create(screen, 'Username', (50, 95), textSize = 25)
usernameTextbox = pgmenu.Textbox.create((50, 125), (400, 40))

passwordText = pgmenu.Text.create(screen, 'Password', (50, 200), textSize = 25)
passwordTextbox = pgmenu.Textbox.create((50, 230), (400, 40))

agreementCheckbox = pgmenu.Checkbox.create((50, 290), activatedFunction = lambda: checkboxType(agreementCheckbox))
submitButton = pgmenu.Button.create((100, 400), (300, 50), activatedFunction = submit)

# Setting the visuals for the widgets
pgmenu.Frame.visuals(screen, loginFrame, borderRadius = 20)

pgmenu.Textbox.visuals(screen, usernameTextbox)
pgmenu.Textbox.visuals(screen, passwordTextbox, textCoverUp = '*')

pgmenu.Checkbox.visuals(screen, agreementCheckbox, text = 'I agree that pgmenu is beautiful', textSize = 20)
pgmenu.Button.visuals(screen, submitButton, text = 'Submit', textSize = 30, borderRadius = 15)

# Adding them to the frame
pgmenu.Frame.add(loginFrame, loginText, usernameText, usernameTextbox, passwordText,
                 passwordTextbox, agreementCheckbox, submitButton)
# Adding them to a menu for easier global manipulation
pgmenu.Menu.add('login', loginFrame, loginText, usernameText, usernameTextbox, passwordText,
                passwordTextbox, agreementCheckbox, submitButton)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Bye Bye!')
            running = False

    # Refresh screen every frame
    screen.fill(pgmenu.bgColor)

    # Draw the widgets (this time not individually, because pgmenu.Menu takes care of it for us)
    pgmenu.Menu.draw('login')

    pygame.display.flip()
    # Update the widgets
    pgmenu.update(event)
    # Update clock
    clock.tick(FPS)