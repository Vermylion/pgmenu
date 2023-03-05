# pgmenu

![](https://github.com/Vermylion/pgmenu/blob/master/Examples/Assets/pgmenu_logo.png)

pgmenu is a basic library for an easy creation of menus in pygame, supporting multiple widget types and designed with the user's experience at heart.

It's optimized to not hinder performance, maintaining above 200 FPS on average and above 100 FPS for big projects. It's also the most customizable possible, allowing for any visuals to be modified to the user's liking. On top of all that, it stays true to the normal pygame experience, using simple and almost identical syntaxes to pygame's, making it easy to just add at any moment into your project.

This library is made for your project, not the project made around the library.

If you have any **features** or **changes** to add, or **bugs** to fix, please contact me at [vermylioncode@gmail.com](mailto:vermylioncode@gmail.com). Thanks in advance!

# Quick Guide

A simple and quick guide to read on how to use this fabulous library.

## Installation

This library can be installed using [PyPI](https://pypi.org/):

    pip install pgmenu

Or manually via [GitHub](https://github.com/Vermylion/pgmenu) or [GitLab](https://gitlab.com/Vermylion/pgmenu).

This library uses mainly **pygame**. On one rare occasion, **Pillow**, **itertools** and **darkdetect** are used.

## Usage

This library, like any menu libraries, allow for multiple use case. It can be used for making **video game menus**, interactable overlay **UIs** (widgets allow for transparency), or full-blown **applications**.

Here is a list of the available widgets:
+ **pgmenu.Button**
+ **pgmenu.Checkbox**
+ **pgmenu.Textbox**
+ **pgmenu.Frame**
+ **pgmenu.Text**
+ **pgmenu.Image**

Other main functions:
+ **pgmenu.Menu**
+ **pgmenu.Theme**
+ **pgmenu.draw()**
+ **pgmenu.update()**
+ **pgmenu.requestCursor()**

## Example

An example for a simple login screen using pgmenu:

```py
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
```

## Documentation

Documentation is in the works, and will be available in the next release (**pgmenu 1.6**).

## Releases

### Next Release

+ **DOCUMENTATION**
+ **pgmenu.Surface or pgmenu.Canvas**
+ **pgmenu.Progressbar**
+ **Argument: imageSurface**
+ **Potentially: pgmenu.Slider and pgmenu.Freeslider**

### Release 1.5

+ **pgmenu.Button**
+ **pgmenu.Checkbox**
+ **pgmenu.Textbox**
+ **pgmenu.Frame**
+ **pgmenu.Text**
+ **pgmenu.Image**
+ **pgmenu.Menu**
+ **pgmenu.Theme**
+ **pgmenu.draw()**
+ **pgmenu.update()**
+ **pgmenu.requestCursor()**

---

**pgmenu** library by Vermylion

MIT License

3.10.9 Python
