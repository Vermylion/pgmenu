import pygame

import pgmenu

FPS = 60

# Initiating window using pygame
pygame.init()
pygame.display.set_caption('Login Demo')
screen = pygame.display.set_mode((1280, 720))
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
pgmenu.Theme.mode('Light')
pgmenu.Theme.custom('WHITE', 
                    accentColor = (255, 255, 255),
                    textFgColor = (0, 0, 0),
                    textBgColor = (255, 255, 255),
                    widgetBgColor = (255, 255, 255, 0),
                    widgetFgColor = (255, 255, 255))
pgmenu.Theme.set('WHITE')

# Creating the widgets
bgImage = pgmenu.Image.create(screen, 'background.jpg', (0, 0), (1280, 720), borderRadius = 0)

loginFrame = pgmenu.Frame.create((390, 110), (500, 500))

loginText = pgmenu.Text.create(screen, 'Login', (250, 20), textSize = 45, centerX = True)

usernameText = pgmenu.Text.create(screen, 'Email', (50, 95), textSize = 25)
usernameTextbox = pgmenu.Textbox.create((50, 125), (400, 40))

passwordText = pgmenu.Text.create(screen, 'Password', (50, 200), textSize = 25)
passwordTextbox = pgmenu.Textbox.create((50, 230), (400, 40))

agreementCheckbox = pgmenu.Checkbox.create((50, 280), activatedFunction = lambda: checkboxType(agreementCheckbox))
submitButton = pgmenu.Button.create((50, 350), (400, 50), activatedFunction = submit)

accountText = pgmenu.Text.create(screen, "Don't have an account?", (50, 450), textSize = 20)
registerButton = pgmenu.Button.create((290, 447), (100, 30))

# Setting the visuals for the widgets
pgmenu.Frame.visuals(screen, loginFrame, borderRadius = 20, color = (255, 255, 255, 35), outlineWidth = 2, outlineColor = (255, 255, 255, 150))

pgmenu.Textbox.visuals(screen, usernameTextbox)
pgmenu.Textbox.visuals(screen, passwordTextbox, textCoverUp = '•')

pgmenu.Checkbox.visuals(screen, agreementCheckbox, text = 'Remember Me', textSize = 20, bgColor = (255, 255, 255), fgColor = (50, 135, 235))
pgmenu.Button.visuals(screen, submitButton, text = 'Log In', textSize = 23, borderRadius = 150)

pgmenu.Button.visuals(screen, registerButton, text = 'Register', color = (255, 255, 255, 0), textColor = (255, 255, 255), textSize = 23)

# Adding them to the frame
pgmenu.Frame.add(loginFrame, loginText, usernameText, usernameTextbox, passwordText,
                 passwordTextbox, agreementCheckbox, submitButton, accountText, registerButton)
# Adding them to a menu for easier global manipulation
pgmenu.Menu.add('login', bgImage, loginFrame, loginText, usernameText, usernameTextbox, passwordText,
                passwordTextbox, agreementCheckbox, submitButton, accountText, registerButton)
pgmenu.Menu.show('login')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Bye Bye!')
            running = False

    # Refresh screen every frame
    screen.fill(pgmenu.getVar('bgColor'))

    # Draw the widgets (this time not individually, because pgmenu.Menu takes care of it for us)
    # By default, pgmenu.Menu.draw() shows the current shown Menu
    pgmenu.Menu.draw()

    pygame.display.flip()
    # Update the widgets
    pgmenu.update(event)
    # Update clock
    clock.tick(FPS)
