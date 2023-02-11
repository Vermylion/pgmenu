import pygame

import frame

widgetText = dict({})
textSurface = dict({})
textCount = 0


class Text:
    def __init__(self) -> None:
        pass

    def create(surface, string, color, coords, font, textSize, centerX, centerY):
        global textSurface, textCount

        if str(surface).split()[0] == 'Frame':
            if frame.frameBase[surface][2] == 'enabled':
                surface = frame.frameBase[surface][1]
            else:
                surface = frame.frameVisuals[surface][0]

        textCount += 1
        textId = f'Text {textCount}'
        totalText = Text.set(string, color, coords, font, textSize, centerX, centerY)
        textSurface[textId] = [surface, totalText[0], totalText[1]]

        return textId

    def modify(textId, surface, string, color, coords, font, textSize, centerX, centerY):
        global textSurface

        if str(surface).split()[0] == 'Frame':
            if frame.frameBase[surface][2] == 'enabled':
                surface = frame.frameBase[surface][1]
            else:
                surface = frame.frameVisuals[surface][0]

        totalText = Text.set(string, color, coords, font, textSize, centerX, centerY)
        textSurface[textId] = [surface, totalText[0], totalText[1]]

        return textId

    def draw(textId):
        surface, textSurf, textPos = textSurface[textId]
        surface.blit(textSurf, textPos)

    def set(string, color, coords, font='freesansbold.ttf', textSize=30, centerX=True, centerY=True):
        font = pygame.font.Font(font, textSize)
        text = font.render(str(string), True, color)
        textRect = text.get_rect()
        textRect[0], textRect[1] = coords

        if centerX:
            textRect.centerx = coords[0]
        if centerY:
            textRect.centery = coords[1]

        return (text, textRect)

    def write(surface, string, color, coords, font='freesansbold.ttf', textSize=30, centerX=True, centerY=True):
        if str(surface).split()[0] == 'Frame':
            if frame.frameBase[surface][2] == 'enabled':
                surface = frame.frameBase[surface][1]
            else:
                surface = frame.frameVisuals[surface][0]

        totalText = Text.set(string, color, coords, font, textSize, centerX, centerY)
        surface.blit(totalText[0], totalText[1])

        return totalText

    def create_text_for_widgets(widgetId, string, color, coords, font='freesansbold.ttf', textSize=30, centerX=True,
                                centerY=True):
        global widgetText

        totalText = Text.set(string, color, coords, font, textSize, centerX, centerY)
        widgetText[widgetId] = totalText

        return totalText
