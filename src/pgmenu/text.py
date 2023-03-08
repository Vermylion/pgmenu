import pygame

import pgmenu.GlobalFunctions as GlobalFunctions

widgetText = dict({})
textSurface = dict({})
textCount = 0


class Text:
    def __init__(self) -> None:
        pass

    def create(surface, string, color, coords, font, textSize, centerX, centerY):
        global textSurface, textCount

        textCount += 1
        textId = f'Text {textCount}'
        totalText = Text.set(string, color, coords, font, textSize, centerX, centerY)
        textSurface[textId] = [totalText[1], surface, totalText[0], string, color, font, textSize, centerX, centerY]

        return textId

    def modify(textId, **kwargs):
        global textSurface

        string = GlobalFunctions.kwargsSwitchCase('string', textSurface[textId][3], kwargs)
        surface = GlobalFunctions.kwargsSwitchCase('surface', textSurface[textId][1], kwargs)
        coords = GlobalFunctions.kwargsSwitchCase('coords', (textSurface[textId][0][0], textSurface[textId][0][1]), kwargs)
        color = GlobalFunctions.kwargsSwitchCase('color', textSurface[textId][4], kwargs)
        font = GlobalFunctions.kwargsSwitchCase('font', textSurface[textId][5], kwargs)
        textSize = GlobalFunctions.kwargsSwitchCase('textSize', textSurface[textId][6], kwargs)
        centerX = GlobalFunctions.kwargsSwitchCase('centerX', textSurface[textId][7], kwargs)
        centerY = GlobalFunctions.kwargsSwitchCase('centerY', textSurface[textId][8], kwargs)
        
        totalText = Text.set(string, color, coords, font, textSize, centerX, centerY)
        textSurface[textId] = [totalText[1], surface, totalText[0], string, color, font, textSize, centerX, centerY]
        
        return textId

    def draw(textId):
        textPos, surface, textSurf, *_ = textSurface[textId]
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

        totalText = Text.set(string, color, coords, font, textSize, centerX, centerY)
        surface.blit(totalText[0], totalText[1])

        return totalText

    def create_text_for_widgets(widgetId, string, color, coords, font='freesansbold.ttf', textSize=30, centerX=True,
                                centerY=True):
        global widgetText

        totalText = Text.set(string, color, coords, font, textSize, centerX, centerY)
        widgetText[widgetId] = totalText

        return totalText
