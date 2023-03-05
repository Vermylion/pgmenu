from itertools import chain
import pygame

import GlobalFunctions
import text as textfile

checkboxBase = dict({})
checkboxVisuals = dict({})
checkboxGroups = dict({})
checkboxCount = 0
checkboxHovered = ''
mouseDown = False


class Checkbox:
    def __init__(self) -> None:
        pass

    def default_action_func():
        print('Checkbox Activated')

    def default_hover_func():
        pass

    def create(coords, size, activatedFunction, hoveredFunction, status, state):
        global checkboxBase, checkboxCount

        checkboxCount += 1
        checkboxId = f'Checkbox {checkboxCount}'
        checkboxRect = pygame.Rect(coords[0], coords[1], size, size)
        checkboxBase[checkboxId] = [checkboxRect, activatedFunction, hoveredFunction, status, state]

        return checkboxId

    def modify(checkboxId, **kwargs):
        global checkboxBase

        coords = GlobalFunctions.kwargsSwitchCase('coords', (checkboxBase[checkboxId][0][0], checkboxBase[checkboxId][0][1]), kwargs)
        size = GlobalFunctions.kwargsSwitchCase('size', checkboxBase[checkboxId][0][2], kwargs)
        activatedFunction = GlobalFunctions.kwargsSwitchCase('activatedFunction', checkboxBase[checkboxId][1], kwargs)
        hoveredFunction = GlobalFunctions.kwargsSwitchCase('hoveredFunction', checkboxBase[checkboxId][2], kwargs)
        status = GlobalFunctions.kwargsSwitchCase('status', checkboxBase[checkboxId][3], kwargs)
        state = GlobalFunctions.kwargsSwitchCase('state', checkboxBase[checkboxId][4], kwargs)

        checkboxRect = pygame.Rect(coords[0], coords[1], size, size)
        checkboxBase[checkboxId] = [checkboxRect, activatedFunction, hoveredFunction, status, state]

        if checkboxId in checkboxVisuals:
            surface, fgColor, bgColor, fgImageName, bgImageName, text, textColor, textSize, textFont, outlineWidth, outlineColor, borderWidth, borderRadius, inflateActive, border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius = checkboxVisuals[checkboxId]
            Checkbox.visuals(surface, checkboxId, fgColor, bgColor, fgImageName, bgImageName, text, textColor, textSize, textFont,
                outlineWidth, outlineColor, borderWidth, borderRadius, inflateActive, border_top_left_radius,
                border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius)

        return checkboxId

    def visuals(surface, checkboxId, fgColor, bgColor, fgImageName, bgImageName, text, textColor, textSize, textFont,
                outlineWidth, outlineColor, borderWidth, borderRadius, inflateActive, border_top_left_radius,
                border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius):
        global checkboxVisuals

        if text != None:
            if textSize == None:
                textSize = checkboxBase[checkboxId][0][3]

            textfile.Text.create_text_for_widgets(checkboxId, text, textColor, ((checkboxBase[checkboxId][0][0] + checkboxBase[checkboxId][0][2] +((0.15 * checkboxBase[checkboxId][0][2]) * 2)), checkboxBase[checkboxId][0][1] + (checkboxBase[checkboxId][0][3] / 2)), textFont, textSize, centerX=False, centerY=True)

        checkboxVisuals[checkboxId] = [surface, fgColor, bgColor, fgImageName, bgImageName, text, textColor, textSize, textFont,
                                       outlineWidth, outlineColor, borderWidth, borderRadius, inflateActive,
                                       border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                                       border_bottom_right_radius]

    def draw(checkboxId):
        surface, fgColor, bgColor, fgImageName, bgImageName, text, textColor, textSize, textFont, outlineWidth, outlineColor, borderWidth, borderRadius, inflateActive, border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius = checkboxVisuals[checkboxId]

        drawRect = checkboxBase[checkboxId][0]
        if checkboxHovered == checkboxId:
            if type(inflateActive) == float or type(inflateActive) == int:
                drawRect = drawRect.inflate(drawRect[2] * (inflateActive / 100), drawRect[3] * (inflateActive / 100))

        GlobalFunctions.draw(surface, drawRect, bgColor, bgImageName, outlineWidth, outlineColor, borderWidth, borderRadius,
                             border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                             border_bottom_right_radius)

        if checkboxBase[checkboxId][3] == True:
            checkedRect = pygame.Rect(drawRect[0] + (0.15 * drawRect[2]), drawRect[1] + (0.15 * drawRect[3]),
                                      drawRect[2] - ((0.15 * drawRect[2]) * 2),
                                      drawRect[3] - ((0.15 * drawRect[3]) * 2))

            GlobalFunctions.draw(surface, checkedRect, fgColor, fgImageName, 0, outlineColor, borderWidth, borderRadius,
                                 border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                                 border_bottom_right_radius)

        if text != None:
            textSurf, textPos = textfile.widgetText[checkboxId]
            surface.blit(textSurf, textPos)

    def enable(checkboxId):
        global checkboxBase

        checkboxBase[checkboxId][4] = 'enabled'

    def disable(checkboxId):
        global checkboxBase

        checkboxBase[checkboxId][4] = 'disabled'

    def statusOn(checkboxId):
        global checkboxBase

        checkboxBase[checkboxId][3] = True

    def statusOff(checkboxId):
        global checkboxBase

        checkboxBase[checkboxId][3] = False

    def get(checkboxId):
        return checkboxBase[checkboxId][3]

    def group(*checkboxIds):
        global checkboxGroups

        checkboxGroup = []
        for checkboxId in checkboxIds:
            checkboxGroup.append(checkboxId)
        checkboxGroups[len(checkboxGroups)] = checkboxGroup

    def ungroup(*checkboxIds):
        global checkboxGroups

        for checkboxId in checkboxIds:
            for group in checkboxGroups:
                if checkboxId in checkboxGroups[group]:
                    del checkboxGroups[group][checkboxGroups[group].index(checkboxId)]

    def update(event):
        global checkboxBase, checkboxHovered, mouseDown

        for checkboxId in checkboxBase:
            if checkboxBase[checkboxId][4] == 'enabled':
                x, y = pygame.mouse.get_pos()

                if checkboxBase[checkboxId][0].collidepoint(x, y):
                    GlobalFunctions.cursorRequested = pygame.SYSTEM_CURSOR_HAND

                    checkboxHovered = checkboxId
                    checkboxBase[checkboxId][2]()

                    if event.type == pygame.MOUSEBUTTONDOWN and not mouseDown:
                        if event.button == pygame.BUTTON_LEFT:
                            if checkboxBase[checkboxId][3] == False:
                                checkboxBase[checkboxId][3] = True
                                for checkboxGroup in checkboxGroups:
                                    if checkboxId in checkboxGroups[checkboxGroup]:
                                        for otherCheckboxId in checkboxGroups[checkboxGroup]:
                                            if otherCheckboxId != checkboxId:
                                                Checkbox.statusOff(otherCheckboxId)
                            else:
                                listGroupIds = list(chain(*checkboxGroups.values()))
                                if checkboxId in listGroupIds:
                                    for id in listGroupIds:
                                        if id != checkboxId:
                                            if checkboxBase[id][3] != False:
                                                checkboxBase[checkboxId][3] = False
                                else:
                                    checkboxBase[checkboxId][3] = False

                            checkboxBase[checkboxId][1]()
                            mouseDown = True

                else:
                    if checkboxHovered == checkboxId:
                        checkboxHovered = ''

            if event.type == pygame.MOUSEBUTTONUP and mouseDown:
                if event.button == pygame.BUTTON_LEFT:
                    mouseDown = False
