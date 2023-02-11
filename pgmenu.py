import pygame

import GlobalFunctions
import button
import checkbox
import frame
import image as imagefile
import menu
import text as textfile
import textbox

widgetFgColor = ''
widgetBgColor = ''
widgetOutlineColor = ''
widgetOutlineWidth = ''
widgetTextFgColor = ''
widgetTextBgColor = ''


def theme(themeName):
    print(themeName)
    global widgetFgColor;
    widgetFgColor = GlobalFunctions.Themes[themeName]['widgetFgColor']
    global widgetBgColor;
    widgetBgColor = GlobalFunctions.Themes[themeName]['widgetBgColor']
    global widgetOutlineColor;
    widgetOutlineColor = GlobalFunctions.Themes[themeName]['widgetOutlineColor']
    global widgetOutlineWidth;
    widgetOutlineWidth = GlobalFunctions.Themes[themeName]['widgetOutlineWidth']
    global widgetTextFgColor;
    widgetTextFgColor = GlobalFunctions.Themes[themeName]['widgetTextFgColor']
    global widgetTextBgColor;
    widgetTextBgColor = GlobalFunctions.Themes[themeName]['widgetTextBgColor']


theme('BLUE')  # YELLOW&BLACK


def createTheme(themeName, fgColor=widgetFgColor, bgColor=widgetBgColor, outlineColor=widgetOutlineColor,
                outlineWidth=widgetOutlineWidth, textFgColor=widgetTextFgColor, textBgColor=widgetTextBgColor):
    GlobalFunctions.createTheme(themeName, fgColor, bgColor, outlineColor, outlineWidth, textFgColor, textBgColor)


class Menu:
    def __init__(self) -> None:
        pass

    def create(menuName):
        menu.Menu.create(menuName)

    def delete(menuName):
        menu.Menu.delete(menuName)

    def add(menuName, *widgetIds):
        menu.Menu.add(menuName, *widgetIds)

    def remove(menuName, *widgetIds):
        menu.Menu.remove(menuName, *widgetIds)

    def show(menuName):
        menu.Menu.show(menuName)

    def draw(menuName=None):
        menu.Menu.draw(menuName)

    def enable(menuName):
        menu.Menu.enable(menuName)

    def disable(menuName):
        menu.Menu.disable(menuName)

    def enableAll():
        menu.Menu.enableAll()

    def disableAll():
        menu.Menu.disableAll()


class Text:
    def __init__(self) -> None:
        pass

    def create(surface, string, color, coords=(10, 10), font='CeraRoundProBold.otf', textSize=30, centerX=False,
               centerY=False):
        return textfile.Text.create(surface, string, color, coords, font, textSize, centerX, centerY)

    def modify(textId, surface, string, color, coords=(10, 10), font='CeraRoundProBold.otf', textSize=30, centerX=False,
               centerY=False):
        return textfile.Text.modify(textId, surface, string, color, coords, font, textSize, centerX, centerY)

    def draw(textId):
        textfile.Text.draw(textId)

    def set(string, color, coords=(10, 10), font='CeraRoundProBold.otf', fontSize=30, centerX=True, centerY=True):
        return textfile.Text.set(string, color, coords, font, fontSize, centerX, centerY)

    def write(surface, string, color, coords=(10, 10), font='CeraRoundProBold.otf', fontSize=30, centerX=True,
              centerY=True):
        return textfile.Text.write(surface, string, color, coords, font, fontSize, centerX, centerY)


class Image:
    def __init__(self) -> None:
        pass

    def create(surface, imageName, coords=(10, 10), dimensions=(100, 100)):
        return imagefile.Image.create(surface, imageName, coords, dimensions)

    def modify(imageId, surface, imageName, coords=(10, 10), dimensions=(100, 100)):
        return imagefile.Image.create(imageId, surface, imageName, coords, dimensions)

    def draw(imageId):
        imagefile.Image.draw(imageId)

    def set(imageName):
        return imagefile.Image.set(imageName)


class Frame:
    def __init__(self) -> None:
        pass

    def create(coords=(10, 10), dimensions=(200, 200), state='enabled'):
        return frame.Frame.create(coords, dimensions, state)

    def modify(frameId, coords=(10, 10), dimensions=(200, 200), state='enabled'):
        return frame.Frame.modify(frameId, coords, dimensions, state)

    def visuals(surface, frameId, color=widgetBgColor, image=None, outlineWidth=widgetOutlineWidth,
                outlineColor=widgetOutlineColor, borderWidth=0, borderRadius=10, border_top_left_radius=-1,
                border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1):
        frame.Frame.visuals(surface, frameId, color, image, outlineWidth, outlineColor, borderWidth, borderRadius,
                            border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                            border_bottom_right_radius)

    def draw(frameId):
        frame.Frame.draw(frameId)

    def add(frameId, *widgetIds):
        frame.Frame.add(frameId, *widgetIds)

    def remove(frameId, *widgetIds):
        frame.Frame.remove(frameId, *widgetIds)

    def enable(frameId):
        frame.Frame.enable(frameId)

    def disable(frameId):
        frame.Frame.disable(frameId)

class Button:
    def __init__(self) -> None:
        pass

    def default_action_func():
        button.Button.default_action_func()

    def default_hover_func():
        button.Button.default_hover_func()

    def create(coords=(10, 10), dimensions=(100, 30), activatedFunction=default_action_func,
               hoveredFunction=default_hover_func, state='enabled'):
        return button.Button.create(coords, dimensions, activatedFunction, hoveredFunction, state)

    def modify(buttonId, coords=(10, 10), dimensions=(100, 30), activatedFunction=default_action_func,
               hoveredFunction=default_hover_func, state='enabled'):
        return button.Button.modify(buttonId, coords, dimensions, activatedFunction, hoveredFunction, state)

    def visuals(surface, buttonId, color=widgetFgColor, image=None, icon=None, text=None, textColor=widgetTextFgColor,
                textSize=None, textFont='CeraRoundProBold.otf', outlineWidth=widgetOutlineWidth,
                outlineColor=widgetOutlineColor, borderWidth=0, borderRadius=5, inflateActive=7,
                border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1,
                border_bottom_right_radius=-1):
        button.Button.visuals(surface, buttonId, color, image, icon, text, textColor, textSize, textFont, outlineWidth,
                              outlineColor, borderWidth, borderRadius, inflateActive, border_top_left_radius,
                              border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius)

    def draw(buttonId):
        button.Button.draw(buttonId)

    def enable(buttonId):
        button.Button.enable(buttonId)

    def disable(buttonId):
        button.Button.disable(buttonId)


class Checkbox:
    def __init__(self) -> None:
        pass

    def default_action_func():
        checkbox.Checkbox.default_action_func()

    def default_hover_func():
        checkbox.Checkbox.default_hover_func()

    def create(coords=(10, 10), size=30, activatedFunction=default_action_func, hoveredFunction=default_hover_func,
               status=False, state='enabled'):
        return checkbox.Checkbox.create(coords, size, activatedFunction, hoveredFunction, status, state)

    def modify(checkboxId, coords=(10, 10), size=30, activatedFunction=default_action_func,
               hoveredFunction=default_hover_func, status=False, state='enabled'):
        return checkbox.Checkbox.modify(checkboxId, coords, size, activatedFunction, hoveredFunction, status, state)

    def visuals(surface, checkboxId, fgColor=widgetFgColor, bgColor=widgetBgColor, fgImage=None, bgImage=None,
                text=None, textColor=widgetTextFgColor, textSize=None, textFont='CeraRoundProBold.otf',
                outlineWidth=widgetOutlineWidth, outlineColor=widgetOutlineColor, borderWidth=0, borderRadius=5,
                inflateActive=10, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1,
                border_bottom_right_radius=-1):
        checkbox.Checkbox.visuals(surface, checkboxId, fgColor, bgColor, fgImage, bgImage, text, textColor, textSize,
                                  textFont, outlineWidth, outlineColor, borderWidth, borderRadius, inflateActive,
                                  border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                                  border_bottom_right_radius)

    def draw(checkboxId):
        checkbox.Checkbox.draw(checkboxId)

    def enable(checkboxId):
        checkbox.Checkbox.enable(checkboxId)

    def disable(checkboxId):
        checkbox.Checkbox.disable(checkboxId)

    def statusOn(checkboxId):
        checkbox.Checkbox.statusOn(checkboxId)

    def statusOff(checkboxId):
        checkbox.Checkbox.statusOff(checkboxId)

    def get(checkboxId):
        return checkbox.Checkbox.get(checkboxId)

    def group(*checkboxIds):
        checkbox.Checkbox.group(*checkboxIds)

    def ungroup(*checkboxIds):
        checkbox.Checkbox.ungroup(*checkboxIds)


class Textbox:
    def __init__(self) -> None:
        pass

    def default_action_func():
        textbox.Textbox.default_action_func()

    def default_hover_func():
        textbox.Textbox.default_hover_func()

    def create(coords=(10, 10), dimensions=(100, 30), limitType=None, limitLength=None, limitInt=None,
               activatedFunction=default_action_func, hoveredFunction=default_hover_func,
               typedFunction=default_action_func, submitFunction=default_action_func, state='enabled'):
        return textbox.Textbox.create(coords, dimensions, limitType, limitLength, limitInt, activatedFunction,
                                      hoveredFunction, typedFunction, submitFunction, state)

    def modify(textboxId, coords=(10, 10), dimensions=(100, 30), limitType=None, limitLength=None, limitInt=None,
               activatedFunction=default_action_func, hoveredFunction=default_hover_func,
               typedFunction=default_action_func, submitFunction=default_action_func, state='enabled'):
        return textbox.Textbox.modify(textboxId, coords, dimensions, limitType, limitLength, limitInt,
                                      activatedFunction, hoveredFunction, typedFunction, submitFunction, state)

    def visuals(surface, textboxId, color=widgetBgColor, image=None, text='', textColor=widgetTextBgColor,
                textFont='CeraRoundProBold.otf', textCoverUp=None, outlineWidth=widgetOutlineWidth,
                outlineColor=widgetOutlineColor, borderWidth=0, borderRadius=5, borderedOverlay=3,
                idleBorderedOverlayColor=widgetBgColor, activeBorderedOverlayColor=widgetFgColor, darkenActive=25,
                border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1,
                border_bottom_right_radius=-1):
        textbox.Textbox.visuals(surface, textboxId, color, image, text, textColor, textFont, textCoverUp, outlineWidth,
                                outlineColor, borderWidth, borderRadius, borderedOverlay, idleBorderedOverlayColor,
                                activeBorderedOverlayColor, darkenActive, border_top_left_radius,
                                border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius)

    def draw(textboxId):
        textbox.Textbox.draw(textboxId)

    def delete(textboxId, start=0, end=None):
        return textbox.Textbox.delete(textboxId, start, end)

    def insert(textboxId, string, place=0):
        return textbox.Textbox.insert(textboxId, string, place)

    def enable(textboxId):
        textbox.Textbox.enable(textboxId)

    def disable(textboxId):
        textbox.Textbox.disable(textboxId)

    def get(textboxId):
        return textbox.Textbox.get(textboxId)


def update(event):
    button.Button.update(event)
    checkbox.Checkbox.update(event)
    textbox.Textbox.update(event)

    frame.Frame.update(event)

    pygame.mouse.set_cursor(GlobalFunctions.cursorRequested)
    GlobalFunctions.cursorRequested = pygame.SYSTEM_CURSOR_ARROW


def draw(surface, drawRect, color=widgetFgColor, image=None, outlineWidth=0, outlineColor=widgetOutlineColor,
         borderWidth=0, borderRadius=10, border_top_left_radius=-1, border_top_right_radius=-1,
         border_bottom_left_radius=-1, border_bottom_right_radius=-1):
    return GlobalFunctions.draw(surface, drawRect, color, image, outlineWidth, outlineColor, borderWidth, borderRadius,
                                border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                                border_bottom_right_radius)
