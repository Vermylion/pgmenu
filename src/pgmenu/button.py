import pygame

import pgmenu.GlobalFunctions as GlobalFunctions
import pgmenu.text as textfile

buttonBase = dict({})
buttonVisuals = dict({})
buttonHovered = ''
buttonCount = 0
mouseDown = False


class Button:
    def __init__(self) -> None:
        pass

    def default_action_func():
        print('Button Activated')

    def default_hover_func():
        pass

    def create(coords, dimensions, activatedFunction, hoveredFunction, state):
        global buttonBase, buttonCount

        buttonCount += 1
        buttonId = f'Button {buttonCount}'
        buttonRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        buttonBase[buttonId] = [buttonRect, activatedFunction, hoveredFunction, state]

        return buttonId

    def modify(buttonId, **kwargs):
        global buttonBase, buttonVisuals

        coords = GlobalFunctions.kwargsSwitchCase('coords', (buttonBase[buttonId][0][0], buttonBase[buttonId][0][1]), kwargs)
        dimensions = GlobalFunctions.kwargsSwitchCase('dimensions', (buttonBase[buttonId][0][2], buttonBase[buttonId][0][3]), kwargs)
        activatedFunction = GlobalFunctions.kwargsSwitchCase('activatedFunction', buttonBase[buttonId][1], kwargs)
        hoveredFunction = GlobalFunctions.kwargsSwitchCase('hoveredFunction', buttonBase[buttonId][2], kwargs)
        state = GlobalFunctions.kwargsSwitchCase('state', buttonBase[buttonId][3], kwargs)

        buttonRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        buttonBase[buttonId] = [buttonRect, activatedFunction, hoveredFunction, state]

        if buttonId in buttonVisuals:
            surface, color, imageName, icon, text, textColor, textSize, textFont, outlineWidth, outlineColor, borderWidth, borderRadius, inflateActive, border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius = buttonVisuals[buttonId]
            Button.visuals(surface, buttonId, color, imageName, icon, text, textColor, textSize, textFont, outlineWidth, outlineColor,
                borderWidth, borderRadius, inflateActive, border_top_left_radius, border_top_right_radius,
                border_bottom_left_radius, border_bottom_right_radius)

        return buttonId

    def visuals(surface, buttonId, color, imageName, icon, text, textColor, textSize, textFont, outlineWidth, outlineColor,
                borderWidth, borderRadius, inflateActive, border_top_left_radius, border_top_right_radius,
                border_bottom_left_radius, border_bottom_right_radius):
        global buttonBase, buttonVisuals

        #surface = GlobalFunctions.frameOffset(surface, buttonId, buttonBase, frame.frameBase, frame.frameVisuals)

        if text != None:
            userTextSize = textSize
            if userTextSize == None:
                textSize = buttonBase[buttonId][0][3] - round(buttonBase[buttonId][0][3] / 6)

            totalText = textfile.Text.create_text_for_widgets(buttonId, text, textColor, (
            buttonBase[buttonId][0][0] + (buttonBase[buttonId][0][2] / 2),
            buttonBase[buttonId][0][1] + (buttonBase[buttonId][0][3] / 2)), textFont, textSize, centerX=True,
                                                              centerY=True)

            if userTextSize == None:
                if totalText[1][2] > buttonBase[buttonId][0][2]:
                    textSize = round(buttonBase[buttonId][0][2] / (totalText[1][2] / totalText[1][3] + 1.5))
                    textfile.Text.create_text_for_widgets(buttonId, text, textColor, (
                    buttonBase[buttonId][0][0] + (buttonBase[buttonId][0][2] / 2),
                    buttonBase[buttonId][0][1] + (buttonBase[buttonId][0][3] / 2)), textFont, textSize, centerX=True,
                                                          centerY=True)

        buttonVisuals[buttonId] = [surface, color, imageName, icon, text, textColor, textSize, textFont, outlineWidth,
                                   outlineColor, borderWidth, borderRadius, inflateActive, border_top_left_radius,
                                   border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius]

    def draw(buttonId):
        surface, color, imageName, icon, text, textColor, textSize, textFont, outlineWidth, outlineColor, borderWidth, borderRadius, inflateActive, border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius = buttonVisuals[buttonId]

        drawRect = buttonBase[buttonId][0]
        if buttonHovered == buttonId:
            if type(inflateActive) == float or type(inflateActive) == int:
                drawRect = drawRect.inflate(drawRect[2] * (inflateActive / 100), drawRect[3] * (inflateActive / 100))

        GlobalFunctions.draw(surface, drawRect, color, imageName, outlineWidth, outlineColor, borderWidth, borderRadius,
                             border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                             border_bottom_right_radius)

        if text != None:
            textSurf, textPos = textfile.widgetText[buttonId]
            if buttonHovered == buttonId:
                if type(inflateActive) == float or type(inflateActive) == int:
                    textRect = drawRect.inflate(drawRect[2] * (inflateActive / 100),
                                                drawRect[3] * (inflateActive / 100))
                textSurf, textPos = textfile.Text.set(text, textColor, (
                textRect[0] + (textRect[2] / 2), textRect[1] + (textRect[3] / 2)), textFont,
                                                      round(textSize + (textSize * (inflateActive / 100))),
                                                      centerX=True, centerY=True)
            surface.blit(textSurf, textPos)

        if icon != None:
            sideSize = min(drawRect[2], drawRect[3]) - (0.15 * min(drawRect[2], drawRect[3]))
            iconRect = pygame.Rect(drawRect[0] + (drawRect[2] / 2) - (sideSize / 2),
                                   drawRect[1] + ((0.15 * sideSize) / 2), sideSize, sideSize)
            GlobalFunctions.draw(surface, iconRect, imageName=icon, borderRadius=0)

    def enable(buttonId):
        global buttonBase

        buttonBase[buttonId][3] = 'enabled'

    def disable(buttonId):
        global buttonBase

        buttonBase[buttonId][3] = 'disabled'

    def update(event):
        global buttonHovered, mouseDown

        for buttonId in buttonBase:
            if buttonBase[buttonId][3] == 'enabled':
                x, y = pygame.mouse.get_pos()
                if buttonBase[buttonId][0].collidepoint(x, y):
                    GlobalFunctions.cursorRequested = pygame.SYSTEM_CURSOR_HAND

                    buttonHovered = buttonId
                    buttonBase[buttonId][2]()

                    if event.type == pygame.MOUSEBUTTONDOWN and not mouseDown:
                        if event.button == pygame.BUTTON_LEFT:
                            buttonBase[buttonId][1]()
                            mouseDown = True

                else:
                    if buttonHovered == buttonId:
                        buttonHovered = ''

            if event.type == pygame.MOUSEBUTTONUP and mouseDown:
                if event.button == pygame.BUTTON_LEFT:
                    mouseDown = False
