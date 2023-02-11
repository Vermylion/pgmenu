import pygame

import GlobalFunctions
import button

frameBase = dict({})
frameVisuals = dict({})
frameWidgets = dict({})
frameCount = 0


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
        frameWidgets[frameId] = []

        return frameId

    def modify(frameId, coords, dimensions, state):
        global frameBase

        frameRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        frameSurface = pygame.Surface((frameRect[2], frameRect[3]), pygame.SRCALPHA)
        frameBase[frameId] = [frameRect, frameSurface, state]

        Frame.setWidgetsOffset()

        return frameId

    def setWidgetsOffset():
        global frameBase, frameVisuals

        for frameId in frameWidgets:
            try:
                for widgetId in frameWidgets[frameId]:
                    GlobalFunctions.frameOffset(frameId, widgetId, button.buttonBase, frameBase, frameVisuals)
            except:
                pass

    def visuals(surface, frameId, color, image, outlineWidth, outlineColor, borderWidth, borderRadius,
                border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius):
        global frameVisuals

        frameVisuals[frameId] = [surface, color, image, outlineWidth, outlineColor, borderWidth, borderRadius,
                                 border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                                 border_bottom_right_radius]

        Frame.setWidgetsOffset()

    def draw(frameId):
        global frameBase

        surface, color, image, outlineWidth, outlineColor, borderWidth, borderRadius, border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius = \
            frameVisuals[frameId]

        # frameBase[frameId][1] = pygame.Surface((frameBase[frameId][0][2], frameBase[frameId][0][3]), pygame.SRCALPHA)

        GlobalFunctions.draw(surface, frameBase[frameId][0], color, image, outlineWidth, outlineColor, borderWidth,
                             borderRadius, border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                             border_bottom_right_radius)
        # pygame.draw.rect(surface, color, frameBase[frameId][0], border_radius = 10)

        surface.blit(frameBase[frameId][1], (frameBase[frameId][0][0], frameBase[frameId][0][1]))

    def add(frameId, *widgetIds):
        global frameWidgets

        for widgetId in widgetIds:
            frameWidgets[frameId].append(widgetId)

        Frame.setWidgetsOffset()

    def remove(frameId, *widgetIds):
        global frameWidgets

        for widgetId in widgetIds:
            frameWidgets[frameId].remove(widgetId)

        Frame.setWidgetsOffset()

    def enable(frameId):
        global frameBase

        frameBase[frameId][2] = 'enabled'

        Frame.setWidgetsOffset()

    def disable(frameId):
        global frameBase

        frameBase[frameId][2] = 'disabled'

        Frame.setWidgetsOffset()

    def update(event):
        pass
