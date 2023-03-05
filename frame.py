import pygame

import GlobalFunctions
import button
import checkbox
import textbox
import text as textfile
import image as imagefile

frameBase = dict({})
frameVisuals = dict({})
frameWidgets = dict({})
frameCount = 0


def findWidgetSettings(frameId, widgetId):
    widgetBase = correctWidgetBase(widgetId)
    return [widgetBase[widgetId][0][0], widgetBase[widgetId][0][1], frameBase[frameId][2]]

def correctWidgetBase(widgetId):
    # widget check
    if widgetId.split()[0] == 'Button':
        return button.buttonBase
    elif widgetId.split()[0] == 'Checkbox':
        return checkbox.checkboxBase
    elif widgetId.split()[0] == 'Textbox':
        return textbox.textboxBase
    elif widgetId.split()[0] == 'Text':
        return textfile.textSurface
    elif widgetId.split()[0] == 'Image':
        return imagefile.imageBase
    elif widgetId.split()[0] == 'Frame':
        return frameBase

    else:
        raise SyntaxError('Invalid widget ID')

class Frame:
    def __init__(self) -> None:
        pass

    def create(coords, dimensions, state):
        global frameBase, frameWidgets, frameCount

        frameCount += 1
        frameId = f'Frame {frameCount}'
        frameRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        frameSurface = pygame.Surface((frameRect[2], frameRect[3]), pygame.SRCALPHA)
        frameBase[frameId] = [frameRect, frameSurface, state]
        frameWidgets[frameId] = dict({})

        return frameId

    def modify(frameId, **kwargs):
        global frameBase

        coords = GlobalFunctions.kwargsSwitchCase('coords', (frameBase[frameId][0][0], frameBase[frameId][0][1]), kwargs)
        dimensions = GlobalFunctions.kwargsSwitchCase('dimensions', (frameBase[frameId][0][2], frameBase[frameId][0][3]), kwargs)
        state = GlobalFunctions.kwargsSwitchCase('state', frameBase[frameId][2], kwargs)

        frameRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        frameSurface = pygame.Surface((frameRect[2], frameRect[3]), pygame.SRCALPHA)
        frameBase[frameId] = [frameRect, frameSurface, state]

        return frameId

    def visuals(surface, frameId, color, imageName, outlineWidth, outlineColor, borderWidth, borderRadius,
                border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius):
        global frameVisuals

        frameVisuals[frameId] = [surface, color, imageName, outlineWidth, outlineColor, borderWidth, borderRadius,
                                 border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                                 border_bottom_right_radius]

    def draw(frameId):
        global frameBase

        surface, color, imageName, outlineWidth, outlineColor, borderWidth, borderRadius, border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius = frameVisuals[frameId]

        GlobalFunctions.draw(surface, frameBase[frameId][0], color, imageName, outlineWidth, outlineColor, borderWidth,
                             borderRadius, border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                             border_bottom_right_radius)

        surface.blit(frameBase[frameId][1], (frameBase[frameId][0][0], frameBase[frameId][0][1]))

    def add(frameId, *widgetIds):
        global frameWidgets

        for widgetId in widgetIds:
            frameWidgets[frameId][widgetId] = ['', '', '']

        Frame.update()

    def remove(frameId, *widgetIds):
        global frameWidgets

        for widgetId in widgetIds:
            frameWidgets[frameId].remove(widgetId)

        Frame.update()

    def enable(frameId):
        global frameBase

        frameBase[frameId][2] = 'enabled'

    def disable(frameId):
        global frameBase

        frameBase[frameId][2] = 'disabled'

    def update():
        global frameBase, frameWidgets
        for frameId in frameBase:
            for widgetId in frameWidgets[frameId]:
                # Check if widget settings are the same as the modified saved ones
                widgetSettings = findWidgetSettings(frameId, widgetId)
                if widgetSettings != frameWidgets[frameId][widgetId]:
                    # Get widget type and correct variable
                    widgetBase = correctWidgetBase(widgetId)

                    # Modify accordingly the widget settings
                    if frameBase[frameId][2] == 'enabled':
                        newWidgetX = widgetBase[widgetId][0][0] + frameBase[frameId][0][0]
                        newWidgetY = widgetBase[widgetId][0][1] + frameBase[frameId][0][1]
                    elif widgetSettings[2] == 'disabled' and frameWidgets[frameId][widgetId][2] == 'enabled':
                        newWidgetX = widgetBase[widgetId][0][0] - frameBase[frameId][0][0]
                        newWidgetY = widgetBase[widgetId][0][1] - frameBase[frameId][0][1]
                    else:
                        newWidgetX = widgetBase[widgetId][0][0]
                        newWidgetY = widgetBase[widgetId][0][1]

                    # Modify the widget using .modify
                    # widget check
                    if widgetId.split()[0] == 'Button':
                        button.Button.modify(widgetId, coords = (newWidgetX, newWidgetY))#, (widgetBase[widgetId][0][2], widgetBase[widgetId][0][3]), widgetBase[widgetId][1], widgetBase[widgetId][2], widgetBase[widgetId][3])
                    elif widgetId.split()[0] == 'Checkbox':
                        checkbox.Checkbox.modify(widgetId, coords = (newWidgetX, newWidgetY))#, widgetBase[widgetId][0][2], widgetBase[widgetId][1], widgetBase[widgetId][2], widgetBase[widgetId][3], widgetBase[widgetId][4])
                    elif widgetId.split()[0] == 'Textbox':
                        textbox.Textbox.modify(widgetId, coords = (newWidgetX, newWidgetY))#, (widgetBase[widgetId][0][2], widgetBase[widgetId][0][3]), widgetBase[widgetId][1], widgetBase[widgetId][2], widgetBase[widgetId][3], widgetBase[widgetId][5], widgetBase[widgetId][6], widgetBase[widgetId][7], widgetBase[widgetId][8], widgetBase[widgetId][9])
                    elif widgetId.split()[0] == 'Text':
                        textfile.textSurface[widgetId][0] = pygame.Rect(newWidgetX, newWidgetY, textfile.textSurface[widgetId][0][2], textfile.textSurface[widgetId][0][3])
                        #textfile.Text.modify(widgetId, widgetBase[widgetId][1], widgetBase[widgetId][3], widgetBase[widgetId][4], (newWidgetX, newWidgetY), widgetBase[widgetId][5], widgetBase[widgetId][6], widgetBase[widgetId][7], widgetBase[widgetId][8])
                    elif widgetId.split()[0] == 'Image':
                        imagefile.Image.modify(widgetId, coords = (newWidgetX, newWidgetY))#widgetBase[widgetId][1], widgetBase[widgetId][2], (newWidgetX, newWidgetY), (widgetBase[widgetId][0][2], widgetBase[widgetId][0][3]), widgetBase[widgetId][3])
                    elif widgetId.split()[0] == 'Frame':
                        Frame.modify(widgetId, coords = (newWidgetX, newWidgetY))#, (widgetBase[widgetId][0][2], widgetBase[widgetId][0][3]), widgetBase[widgetId][2])

                    # save now modified settings as our own
                    frameWidgets[frameId][widgetId] = [newWidgetX, newWidgetY, frameBase[frameId][2]]
