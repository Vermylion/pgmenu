import pygame

import GlobalFunctions
import frame
import text as textfile

textboxBase = dict({})
textboxVisuals = dict({})
textboxCount = 0
textboxHovered = ''
textboxSelected = ''
mouseDown = False
keyDown = False

cursorBase = dict({})
visualCursorPos = dict({})


class Textbox:
    def __init__(self) -> None:
        pass

    def default_action_func():
        print('Textbox Action')

    def default_hover_func():
        pass

    def create(coords, dimensions, limitType, limitLength, limitInt, activatedFunction, hoveredFunction, typedFunction,
               submitFunction, state):
        global textboxBase, textboxCount, cursorBase

        textboxCount += 1
        cursorPos = 0
        textboxId = f'Textbox {textboxCount}'
        textboxRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        textboxBase[textboxId] = [textboxRect, limitType, limitLength, limitInt, cursorPos, activatedFunction,
                                  hoveredFunction, typedFunction, submitFunction, state]

        cursorBase[
            textboxId] = []  # [pygame.Rect(pygame.Rect(textboxBase[textboxId][0][0] + (0.015 * textboxBase[textboxId][0][2]) + textLength, textboxBase[textboxId][0][1] + (0.15 * textboxBase[textboxId][0][3]), 2, textboxVisuals[textboxId][5]))]

        return textboxId

    def modify(textboxId, coords, dimensions, limitType, limitLength, limitInt, activatedFunction, hoveredFunction,
               typedFunction, submitFunction, state):
        global textboxBase

        cursorPos = 0
        textboxRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        textboxBase[textboxId] = [textboxRect, limitType, limitLength, limitInt, cursorPos, activatedFunction,
                                  hoveredFunction, typedFunction, submitFunction, state]

        return textboxId

    def visuals(surface, textboxId, color, image, text, textColor, textFont, textCoverUp, outlineWidth, outlineColor,
                borderWidth, borderRadius, borderedOverlay, idleBorderedOverlayColor, activeBorderedOverlayColor,
                darkenActive, border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                border_bottom_right_radius):
        global textboxVisuals, lettersText

        if str(surface).split()[0] == 'Frame':
            if frame.frameBase[surface][2] == 'enabled':
                surface = frame.frameBase[surface][1]
            else:
                surface = frame.frameVisuals[surface][0]

        actualText = text
        if text == '' and textboxBase[textboxId][1] == int and textboxBase[textboxId][3] != None:
            # if type(limitInt[0]) == int
            actualText = str(textboxBase[textboxId][3][0])
            text = str(textboxBase[textboxId][3][0])
        if textCoverUp != None:
            text = str(textCoverUp) * len(text)

        textSize = textboxBase[textboxId][0][3] - round(textboxBase[textboxId][0][3] / 4)
        textboxVisuals[textboxId] = [surface, color, image, actualText, textColor, textSize, textFont, textCoverUp,
                                     outlineWidth, outlineColor, borderWidth, borderRadius, borderedOverlay,
                                     idleBorderedOverlayColor, activeBorderedOverlayColor, darkenActive,
                                     border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                                     border_bottom_right_radius]
        totalText = textfile.Text.create_text_for_widgets(textboxId, text, textColor, (
        textboxBase[textboxId][0][0] + 3 + textboxVisuals[textboxId][12],
        textboxBase[textboxId][0][1] + (textboxBase[textboxId][0][3] / 2)), textFont, textSize, centerX=False,
                                                          centerY=True)

        lettersText = dict({})
        visualCursorPos[textboxId] = 0

    def draw(textboxId):
        surface, color, image, text, textColor, textSize, textFont, textCoverUp, outlineWidth, outlineColor, borderWidth, borderRadius, borderedOverlay, idleBorderedOverlayColor, activeBorderedOverlayColor, darkenActive, border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius = \
        textboxVisuals[textboxId]
        if textboxSelected == textboxId:
            if type(darkenActive) == int or type(darkenActive) == float:
                color = list(color)
                color[0], color[1], color[2] = max(color[0] - darkenActive, 0), max(color[1] - darkenActive, 0), max(
                    color[2] - darkenActive, 0)
                color = tuple(color)

        drawRect = textboxBase[textboxId][0]
        GlobalFunctions.draw(surface, drawRect, color, image, outlineWidth, outlineColor, borderWidth, borderRadius,
                             border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                             border_bottom_right_radius)

        textSurf, textPos = textfile.widgetText[textboxId]
        croppedTextSurf = pygame.Surface((drawRect[2] - 10, drawRect[3]), pygame.SRCALPHA)
        croppedTextSurf.blit(textSurf, (0, 0))

        surface.blit(croppedTextSurf, textPos)

        if textboxSelected == textboxId:
            pygame.draw.rect(surface, (255, 255, 255), cursorBase[textboxId][0])

        if borderedOverlay > 0:
            borderedOverlayColor = idleBorderedOverlayColor
            if textboxId == textboxSelected:
                borderedOverlayColor = activeBorderedOverlayColor
            GlobalFunctions.draw(surface, drawRect, borderedOverlayColor, image, outlineWidth, outlineColor,
                                 borderedOverlay, borderRadius, border_top_left_radius, border_top_right_radius,
                                 border_bottom_left_radius, border_bottom_right_radius)

    def delete(textboxId, start=0, end=None):
        global textboxVisuals, textboxBase
        text = textboxVisuals[textboxId][3]

        if type(end) != int:
            end = len(text)

        textboxVisuals[textboxId][3] = text.replace(text[start:end], '')

        textboxBase[textboxId][4] -= len(text[start:end])
        if textboxBase[textboxId][4] < 0:
            textboxBase[textboxId][4] = 0

        Textbox.update_text_visuals(textboxId)

    def insert(textboxId, string, place=0):
        global textboxVisuals, textboxBase
        text = textboxVisuals[textboxId][3]

        textboxVisuals[textboxId][3] = text[:place] + string + text[place:]

        textboxBase[textboxId][4] += len(string)
        if textboxBase[textboxId][4] > len(textboxVisuals[textboxId][3]):
            textboxBase[textboxId][4] = len(textboxVisuals[textboxId][3])

        Textbox.update_text_visuals(textboxId)

    def enable(textboxId):
        global textboxBase

        textboxBase[textboxId][-1] = 'enabled'

    def disable(textboxId):
        global textboxBase

        textboxBase[textboxId][-1] = 'disabled'

    def get(textboxId):
        return textboxVisuals[textboxId][3]

    def update_text_visuals(textboxId):
        Textbox.update_cursor_pos(textboxId)

        global visualCursorPos, cursorBase
        text = textboxVisuals[textboxId][3]

        if textboxVisuals[textboxId][7] != None:
            text = str(textboxVisuals[textboxId][7]) * len(text)

        if cursorBase[textboxId][0][0] >= (textboxBase[textboxId][0][0] + textboxBase[textboxId][0][2]) - (
                textboxVisuals[textboxId][5] / 2):
            visualCursorPos[textboxId] += 1
            if visualCursorPos[textboxId] > len(text):
                visualCursorPos[textboxId] = len(text)
        elif cursorBase[textboxId][0][0] <= textboxBase[textboxId][0][0] + (textboxVisuals[textboxId][5] / 2):
            visualCursorPos[textboxId] -= 1
            if visualCursorPos[textboxId] < 0:
                visualCursorPos[textboxId] = 0

        text = text[visualCursorPos[textboxId]:]

        textfile.Text.create_text_for_widgets(textboxId, text, textboxVisuals[textboxId][4], (
        textboxBase[textboxId][0][0] + 3 + textboxVisuals[textboxId][12],
        textboxBase[textboxId][0][1] + (textboxBase[textboxId][0][3] / 2)), textboxVisuals[textboxId][6],
                                              textboxVisuals[textboxId][5], centerX=False, centerY=True)
        Textbox.update_cursor_pos(textboxId)

    def update_cursor_pos(textboxId):
        global cursorBase

        totalText = textfile.Text.set(
            textboxVisuals[textboxId][3][visualCursorPos[textboxId]:textboxBase[textboxId][4]], (255, 255, 255), (0, 0),
            textboxVisuals[textboxId][6], textSize=textboxVisuals[textboxId][5])
        # (textboxBase[textboxId][0][0] + (0.015 * textboxBase[textboxId][0][2]), textboxBase[textboxId][0][1] + (textboxBase[textboxId][0][3] / 2))
        cursorBase[textboxId] = [
            pygame.Rect(textboxBase[textboxId][0][0] + 3 + textboxVisuals[textboxId][12] + totalText[1][2],
                        textboxBase[textboxId][0][1] + (0.15 * textboxBase[textboxId][0][3]), 2,
                        textboxVisuals[textboxId][5])]
        # print(cursorBase[textboxId], textboxBase[textboxId][0][0] + textboxBase[textboxId][0][2], textboxId)

    def update(event):
        global textboxBase, textboxVisuals, textboxHovered, textboxSelected, lettersText, cursorBase, visualCursorPos, mouseDown, keyDown

        for textboxId in textboxBase:
            if textboxBase[textboxId][-1] == 'enabled':
                x, y = pygame.mouse.get_pos()

                if textboxBase[textboxId][0].collidepoint(x, y):
                    GlobalFunctions.cursorRequested = pygame.SYSTEM_CURSOR_IBEAM

                    textboxHovered = textboxId
                    textboxBase[textboxId][6]()

                    if event.type == pygame.MOUSEBUTTONDOWN and not mouseDown:
                        if event.button == pygame.BUTTON_LEFT:
                            textboxSelected = textboxId

                            textboxBase[textboxId][5]()
                            mouseDown = True

                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == pygame.BUTTON_LEFT:
                            if textboxSelected == textboxId:
                                if textboxVisuals[textboxSelected][3] == '' and textboxBase[textboxSelected][
                                    1] == int and textboxBase[textboxSelected][3] != None:
                                    textboxVisuals[textboxSelected][3] = str(textboxBase[textboxSelected][3][0])
                                    Textbox.update_text_visuals(textboxSelected)
                                textboxSelected = ''

                    if textboxHovered == textboxId:
                        textboxHovered = ''

            if textboxSelected == textboxId:
                textboxTextChanged = False

                if cursorBase[textboxId] == []:
                    Textbox.update_cursor_pos(textboxId)

                if event.type == pygame.KEYDOWN and not keyDown:
                    # if event.key != pygame.K_LSHIFT:
                    keyDown = True

                    if event.key == pygame.K_RETURN:
                        textboxBase[textboxId][8]()

                    elif event.key == pygame.K_BACKSPACE:
                        if textboxBase[textboxId][4] != 0:
                            textboxVisuals[textboxId][3] = textboxVisuals[textboxId][3][
                                                           :textboxBase[textboxId][4] - 1] + textboxVisuals[textboxId][
                                                                                                 3][
                                                                                             textboxBase[textboxId][4]:]
                            textboxBase[textboxId][4] -= 1
                            textboxBase[textboxId][7]()
                            textboxTextChanged = True
                        if visualCursorPos[textboxId] != 0:
                            visualCursorPos[textboxId] -= 1

                    elif event.key == pygame.K_DELETE:
                        if textboxBase[textboxId][4] != len(textboxVisuals[textboxId][3]):
                            textboxVisuals[textboxId][3] = textboxVisuals[textboxId][3][:textboxBase[textboxId][4]] + \
                                                           textboxVisuals[textboxId][3][textboxBase[textboxId][4] + 1:]
                            textboxBase[textboxId][7]()
                            textboxTextChanged = True
                        if visualCursorPos[textboxId] != 0:
                            visualCursorPos[textboxId] -= 1

                    elif event.key == pygame.K_LEFT:
                        if textboxBase[textboxId][4] != 0:
                            textboxBase[textboxId][4] -= 1
                            textboxTextChanged = True

                    elif event.key == pygame.K_RIGHT:
                        if textboxBase[textboxId][4] != len(textboxVisuals[textboxId][3]):
                            textboxBase[textboxId][4] += 1
                            textboxTextChanged = True

                elif event.type == pygame.TEXTINPUT and not keyDown:
                    keyDown = True
                    censured = False
                    textboxTextChanged = True

                    textboxBase[textboxId][7]()

                    textboxVisuals[textboxId][3] = textboxVisuals[textboxId][3][
                                                   :textboxBase[textboxId][4]] + event.text + textboxVisuals[textboxId][
                                                                                                  3][
                                                                                              textboxBase[textboxId][
                                                                                                  4]:]
                    textboxBase[textboxId][4] += 1

                    limitType, limitLength, limitInt = textboxBase[textboxId][1], textboxBase[textboxId][2], \
                                                       textboxBase[textboxId][3]

                    if limitType != None:
                        try:
                            limitType(textboxVisuals[textboxId][3])
                            if limitType == int and limitInt != None:
                                if float(textboxVisuals[textboxId][3]) < limitInt[0] or float(
                                        textboxVisuals[textboxId][3]) > limitInt[1]:
                                    censured = True
                        except:
                            censured = True
                    if type(limitLength) == int:
                        if len(textboxVisuals[textboxId][3]) - 1 >= limitLength:
                            censured = True

                    if censured:
                        textboxVisuals[textboxId][3] = textboxVisuals[textboxId][3][:textboxBase[textboxId][4] - 1] + \
                                                       textboxVisuals[textboxId][3][textboxBase[textboxId][4]:]
                        textboxBase[textboxId][4] -= 1

                if textboxTextChanged:
                    Textbox.update_text_visuals(textboxId)

            if event.type == pygame.MOUSEBUTTONUP and mouseDown:
                if event.button == pygame.BUTTON_LEFT:
                    mouseDown = False

            if event.type == pygame.KEYUP and keyDown:
                keyDown = False
