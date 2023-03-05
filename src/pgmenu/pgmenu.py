import pygame

import GlobalFunctions
import button
import checkbox
import frame
import image as imagefile
import menu
import text as textfile
import textbox
import theme

mainColor = (0, 0, 0)
bgColor = (0, 0, 0)
fgColor = (0, 0, 0)
widgetFgColor = (0, 0, 0)
widgetBgColor = (0, 0, 0)

textFgColor = (0, 0, 0)
textBgColor = (0, 0, 0)

widgetOutlineColor = (0, 0, 0)
widgetOutlineWidth = 0
widgetBorderWidth = 0

accentColor = (0, 0, 0)


class Theme:
    def __init(self) -> None:
        pass

    def mode(modeType):
        """
        Available mode types:
        'Light'
        'Dark'
        'System'
        """

        theme.Theme.mode(modeType)

        global mainColor; mainColor = theme.mainColor
        global bgColor; bgColor = theme.bgColor
        global fgColor; fgColor = theme.fgColor
        global widgetFgColor; widgetFgColor = theme.widgetFgColor
        global widgetBgColor; widgetBgColor = theme.widgetBgColor

        global textFgColor; textFgColor = theme.textFgColor
        global textBgColor; textBgColor = theme.textBgColor

    def set(themeName):
        """
        Available themes:
        'BLUE'
        'RED'
        'GREEN'
        'YELLOW'
        'PURPLE'
        'YELLOW&BLACK'
        """

        theme.Theme.set(themeName)

        global mainColor; mainColor = theme.mainColor
        global bgColor; bgColor = theme.bgColor
        global fgColor; fgColor = theme.fgColor
        global widgetFgColor; widgetFgColor = theme.widgetFgColor
        global widgetBgColor; widgetBgColor = theme.widgetBgColor

        global widgetOutlineColor; widgetOutlineColor = theme.widgetOutlineColor
        global widgetOutlineWidth; widgetOutlineWidth = theme.widgetOutlineWidth
        global widgetBorderWidth; widgetBorderWidth = theme.widgetBorderWidth

        global textFgColor; textFgColor = theme.textFgColor
        global textBgColor; textBgColor = theme.textBgColor

        global accentColor; accentColor = theme.accentColor

    def custom(themeName, **kwargs):
        """
        Optional Arguments:
        accentColor: tuple
        textFgColor: tuple
        textBgColor: tuple
        widgetOutlineColor: tuple
        widgetOutlineWidth: int
        widgetBorderWidth: int
        ---Mode Arguments:
        mainColor: tuple
        bgColor: tuple
        fgColor: tuple
        widgetFgColor: tuple
        widgetBgColor: tuple
        """

        theme.Theme.custom(themeName, **kwargs)

        #theme.Theme.set(themeName)

Theme.mode('System')
Theme.set('BLUE')

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

    def create(surface, string, coords = (10, 10), **kwargs):
        """
        Optional Arguments:
        color: tuple
        font: str
        textSize: int
        centerX: False/True
        centerY: False/True
        """

        color = GlobalFunctions.kwargsSwitchCase('color', textBgColor, kwargs)
        font = GlobalFunctions.kwargsSwitchCase('font', 'CeraRoundProBold.otf', kwargs)
        textSize = GlobalFunctions.kwargsSwitchCase('textSize', 30, kwargs)
        centerX = GlobalFunctions.kwargsSwitchCase('centerX', False, kwargs)
        centerY = GlobalFunctions.kwargsSwitchCase('centerY', False, kwargs)

        return textfile.Text.create(surface, string, color, coords, font, textSize, centerX, centerY)

    def modify(textId, **kwargs):
        """
        Optional Arguments:
        surface: pygame.Surface
        string: str
        coords: tuple
        color: tuple
        font: str
        textSize: int
        centerX: False/True
        centerY: False/True
        """

        return textfile.Text.modify(textId, **kwargs)

    def draw(textId):
        textfile.Text.draw(textId)

    def set(string, coords = (10, 10), **kwargs):
        """
        Optional Arguments:
        color: tuple
        font: str
        textSize: int
        centerX: True/False
        centerY: True/False
        """

        color = GlobalFunctions.kwargsSwitchCase('color', textBgColor, kwargs)
        font = GlobalFunctions.kwargsSwitchCase('font', 'CeraRoundProBold.otf', kwargs)
        textSize = GlobalFunctions.kwargsSwitchCase('textSize', 30, kwargs)
        centerX = GlobalFunctions.kwargsSwitchCase('centerX', True, kwargs)
        centerY = GlobalFunctions.kwargsSwitchCase('centerY', True, kwargs)

        return textfile.Text.set(string, color, coords, font, textSize, centerX, centerY)

    def write(surface, string, coords=(10, 10), **kwargs):
        """
        Optional Arguments:
        color: tuple
        font: str
        textSize: int
        centerX: True/False
        centerY: True/False
        """

        color = GlobalFunctions.kwargsSwitchCase('color', textBgColor, kwargs)
        font = GlobalFunctions.kwargsSwitchCase('font', 'CeraRoundProBold.otf', kwargs)
        textSize = GlobalFunctions.kwargsSwitchCase('textSize', 30, kwargs)
        centerX = GlobalFunctions.kwargsSwitchCase('centerX', True, kwargs)
        centerY = GlobalFunctions.kwargsSwitchCase('centerY', True, kwargs)

        return textfile.Text.write(surface, string, color, coords, font, textSize, centerX, centerY)


class Image:
    def __init__(self) -> None:
        pass

    def create(surface, imageName, coords = (10, 10), dimensions = (200, 200), **kwargs):
        """
        Optional Arguments:
        borderRadius: int
        """

        borderRadius = GlobalFunctions.kwargsSwitchCase('borderRadius', 15, kwargs)

        return imagefile.Image.create(surface, imageName, coords, dimensions, borderRadius)

    def modify(imageId, **kwargs):
        """
        Optional Arguments:
        surface: pygame.Surface
        imageName: str
        coords: tuple
        dimensions: tuple
        borderRadius: int
        """

        return imagefile.Image.modify(imageId, **kwargs)

    def draw(imageId):
        imagefile.Image.draw(imageId)

    def set(imageName):
        return imagefile.Image.set(imageName)

    def size(imageName, **kwargs):
        """
        Optional Arguments:
        resizeRatio: int
        """

        resizeRatio = GlobalFunctions.kwargsSwitchCase('resizeRatio', 1, kwargs)

        return imagefile.Image.size(imageName, resizeRatio)

class Frame:
    def __init__(self) -> None:
        pass

    def create(coords = (10, 10), dimensions = (200, 200), **kwargs):
        """
        Optional Arguments:
        state: str
        """

        state = GlobalFunctions.kwargsSwitchCase('state', 'enabled', kwargs)

        return frame.Frame.create(coords, dimensions, state)

    def modify(frameId, **kwargs):
        """
        Optional Arguments:
        coords: tuple
        dimensions: tuple
        state: str
        """

        return frame.Frame.modify(frameId, **kwargs)

    def visuals(surface, frameId, **kwargs):
        """
        Optional Arguments:
        color: tuple
        imageName: None | str
        outlineWidth: int
        outlineColor: tuple
        borderWidth: int
        borderRadius: int
        border_top_left_radius: int
        border_top_right_radius: int
        border_bottom_left_radius: int
        border_bottom_right_radius: int
        """

        color = GlobalFunctions.kwargsSwitchCase('color', fgColor, kwargs)
        imageName = GlobalFunctions.kwargsSwitchCase('imageName', None, kwargs)
        outlineWidth = GlobalFunctions.kwargsSwitchCase('outlineWidth', widgetOutlineWidth, kwargs)
        outlineColor = GlobalFunctions.kwargsSwitchCase('outlineColor', widgetOutlineColor, kwargs)
        borderWidth = GlobalFunctions.kwargsSwitchCase('borderWidth', widgetBorderWidth, kwargs)
        borderRadius = GlobalFunctions.kwargsSwitchCase('borderRadius', 15, kwargs)
        border_top_left_radius = GlobalFunctions.kwargsSwitchCase('border_top_left_radius', -1, kwargs)
        border_top_right_radius = GlobalFunctions.kwargsSwitchCase('border_top_right_radius', -1, kwargs)
        border_bottom_left_radius = GlobalFunctions.kwargsSwitchCase('border_bottom_left_radius', -1, kwargs)
        border_bottom_right_radius = GlobalFunctions.kwargsSwitchCase('border_bottom_right_radius', -1, kwargs)

        frame.Frame.visuals(surface, frameId, color, imageName, outlineWidth, outlineColor, borderWidth, borderRadius,
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

    def create(coords=(10, 10), dimensions=(100, 30), **kwargs):
        """
        Optional Arguments:
        activatedFunction: function
        hoveredFunction: function
        state: str
        """

        activatedFunction = GlobalFunctions.kwargsSwitchCase('activatedFunction', Button.default_action_func, kwargs)
        hoveredFunction = GlobalFunctions.kwargsSwitchCase('hoveredFunction', Button.default_hover_func, kwargs)
        state = GlobalFunctions.kwargsSwitchCase('state', 'enabled', kwargs)

        return button.Button.create(coords, dimensions, activatedFunction, hoveredFunction, state)

    def modify(buttonId, **kwargs):
        """
        Optional Arguments:
        coords: tuple
        dimensions: tuple
        activatedFunction: function
        hoveredFunction: function
        state: str
        """

        return button.Button.modify(buttonId, **kwargs)

    def visuals(surface, buttonId, **kwargs):
        """
        Optional Arguments:
        color: tuple
        imageName: None | str
        icon: None | str
        text: None | str
        textColor: tuple
        textSize: None | int
        textFont: str
        outlineWidth: int
        outlineColor: tuple
        borderWidth: int
        borderRadius: int
        inflateActive: int
        border_top_left_radius: int
        border_top_right_radius: int
        border_bottom_left_radius: int
        border_bottom_right_radius: int
        """

        color = GlobalFunctions.kwargsSwitchCase('color', accentColor, kwargs)
        imageName = GlobalFunctions.kwargsSwitchCase('imageName', None, kwargs)
        icon = GlobalFunctions.kwargsSwitchCase('icon', None, kwargs)
        text = GlobalFunctions.kwargsSwitchCase('text', 'Button', kwargs)
        textColor = GlobalFunctions.kwargsSwitchCase('textColor', textFgColor, kwargs)
        textSize = GlobalFunctions.kwargsSwitchCase('textSize', None, kwargs)
        textFont = GlobalFunctions.kwargsSwitchCase('textFont', 'CeraRoundProBold.otf', kwargs)
        outlineWidth = GlobalFunctions.kwargsSwitchCase('outlineWidth', widgetOutlineWidth, kwargs)
        outlineColor = GlobalFunctions.kwargsSwitchCase('outlineColor', widgetOutlineColor, kwargs)
        borderWidth = GlobalFunctions.kwargsSwitchCase('borderWidth', widgetBorderWidth, kwargs)
        borderRadius = GlobalFunctions.kwargsSwitchCase('borderRadius', 7, kwargs)
        inflateActive = GlobalFunctions.kwargsSwitchCase('inflateActive', 7, kwargs)
        border_top_left_radius = GlobalFunctions.kwargsSwitchCase('border_top_left_radius', -1, kwargs)
        border_top_right_radius = GlobalFunctions.kwargsSwitchCase('border_top_right_radius', -1, kwargs)
        border_bottom_left_radius = GlobalFunctions.kwargsSwitchCase('border_bottom_left_radius', -1, kwargs)
        border_bottom_right_radius = GlobalFunctions.kwargsSwitchCase('border_bottom_right_radius', -1, kwargs)

        button.Button.visuals(surface, buttonId, color, imageName, icon, text, textColor, textSize, textFont, outlineWidth,
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

    def create(coords=(10, 10), size=30, **kwargs):
        """
        Optional Arguments:
        activatedFunction: function
        hoveredFunction: function
        status: False/True
        state: str
        """

        activatedFunction = GlobalFunctions.kwargsSwitchCase('activatedFunction', Checkbox.default_action_func, kwargs)
        hoveredFunction = GlobalFunctions.kwargsSwitchCase('hoveredFunction', Checkbox.default_hover_func, kwargs)
        status = GlobalFunctions.kwargsSwitchCase('status', False, kwargs)
        state = GlobalFunctions.kwargsSwitchCase('state', 'enabled', kwargs)
        
        return checkbox.Checkbox.create(coords, size, activatedFunction, hoveredFunction, status, state)

    def modify(checkboxId, **kwargs):
        """
        Optional Arguments:
        coords: tuple
        size: int
        activatedFunction: function
        hoveredFunction: function
        status: False/True
        state: str
        """
        
        return checkbox.Checkbox.modify(checkboxId, **kwargs)

    def visuals(surface, checkboxId, **kwargs):
        """
        Optional Arguments:
        fgColor: tuple
        bgColor: tuple
        fgImage: None | str
        bgImage: None | str
        text: None | str
        textColor: tuple
        textSize: None | int
        textFont: str
        outlineWidth: int
        outlineColor: tuple
        borderWidth: int
        borderRadius: int
        inflateActive: int
        border_top_left_radius: int
        border_top_right_radius: int
        border_bottom_left_radius: int
        border_bottom_right_radius: int
        """

        fgColor = GlobalFunctions.kwargsSwitchCase('fgColor', accentColor, kwargs)
        bgColor = GlobalFunctions.kwargsSwitchCase('bgColor', widgetBgColor, kwargs)
        fgImage = GlobalFunctions.kwargsSwitchCase('fgImage', None, kwargs)
        bgImage = GlobalFunctions.kwargsSwitchCase('bgImage', None, kwargs)
        text = GlobalFunctions.kwargsSwitchCase('text', 'Checkbox', kwargs)
        textColor = GlobalFunctions.kwargsSwitchCase('textColor', textBgColor, kwargs)
        textSize = GlobalFunctions.kwargsSwitchCase('textSize', None, kwargs)
        textFont = GlobalFunctions.kwargsSwitchCase('textFont', 'CeraRoundProBold.otf', kwargs)
        outlineWidth = GlobalFunctions.kwargsSwitchCase('outlineWidth', widgetOutlineWidth, kwargs)
        outlineColor = GlobalFunctions.kwargsSwitchCase('outlineColor', widgetOutlineColor, kwargs)
        borderWidth = GlobalFunctions.kwargsSwitchCase('borderWidth', widgetBorderWidth, kwargs)
        borderRadius = GlobalFunctions.kwargsSwitchCase('borderRadius', 7, kwargs)
        inflateActive = GlobalFunctions.kwargsSwitchCase('inflateActive', 10, kwargs)
        border_top_left_radius = GlobalFunctions.kwargsSwitchCase('border_top_left_radius', -1, kwargs)
        border_top_right_radius = GlobalFunctions.kwargsSwitchCase('border_top_right_radius', -1, kwargs)
        border_bottom_left_radius = GlobalFunctions.kwargsSwitchCase('border_bottom_left_radius', -1, kwargs)
        border_bottom_right_radius = GlobalFunctions.kwargsSwitchCase('border_bottom_right_radius', -1, kwargs)

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

    def default_typed_func():
        textbox.Textbox.default_typed_func()

    def default_action_func():
        textbox.Textbox.default_action_func()

    def default_hover_func():
        textbox.Textbox.default_hover_func()

    def create(coords=(10, 10), dimensions=(100, 30), **kwargs):
        """
        Optional Arguments:
        limitType: None | Any type
        limitLength: None | int
        limitNumbers: None | tuple
        activatedFunction: function
        hoveredFunction: function
        typedFunction: function
        submitFunction: function
        state: str
        """

        limitType = GlobalFunctions.kwargsSwitchCase('limitType', None, kwargs)
        limitLength = GlobalFunctions.kwargsSwitchCase('limitLength', None, kwargs)
        limitNumbers = GlobalFunctions.kwargsSwitchCase('limitNumbers', None, kwargs)
        activatedFunction = GlobalFunctions.kwargsSwitchCase('activatedFunction', Textbox.default_action_func, kwargs)
        hoveredFunction = GlobalFunctions.kwargsSwitchCase('hoveredFunction', Textbox.default_hover_func, kwargs)
        typedFunction = GlobalFunctions.kwargsSwitchCase('typedFunction', Textbox.default_typed_func, kwargs)
        submitFunction = GlobalFunctions.kwargsSwitchCase('submitFunction', None, kwargs)
        state = GlobalFunctions.kwargsSwitchCase('state', 'enabled', kwargs)

        return textbox.Textbox.create(coords, dimensions, limitType, limitLength, limitNumbers, activatedFunction,
                                      hoveredFunction, typedFunction, submitFunction, state)

    def modify(textboxId, **kwargs):
        """
        Optional Arguments:
        coords: tuple
        dimensions: tuple
        limitType: None | Any type
        limitLength: None | int
        limitNumbers: None | tuple
        activatedFunction: function
        hoveredFunction: function
        typedFunction: function
        submitFunction: function
        state: str
        """

        return textbox.Textbox.modify(textboxId, **kwargs)

    def visuals(surface, textboxId, **kwargs):
        """
        Optional Arguments:
        color: tuple
        imageName: None | str
        text: None | str
        textColor: tuple
        textFont: str
        textCoverUp: None | str
        outlineWidth: int
        outlineColor: tuple
        borderWidth: int
        borderRadius: int
        borderedOverlay: int
        cursorWidth: int
        cursorColor: tuple
        cursorBorderRadius: int
        idleBorderedOverlayColor: tuple
        activeBorderedOverlayColor: tuple
        darkenActive: int
        border_top_left_radius: int
        border_top_right_radius: int
        border_bottom_left_radius: int
        border_bottom_right_radius: int
        """

        color = GlobalFunctions.kwargsSwitchCase('color', widgetBgColor, kwargs)
        imageName = GlobalFunctions.kwargsSwitchCase('imageName', None, kwargs)
        text = GlobalFunctions.kwargsSwitchCase('text', '', kwargs)
        textColor = GlobalFunctions.kwargsSwitchCase('textColor', textBgColor, kwargs)
        textFont = GlobalFunctions.kwargsSwitchCase('textFont', 'CeraRoundProBold.otf', kwargs)
        textCoverUp = GlobalFunctions.kwargsSwitchCase('textCoverUp', None, kwargs)
        outlineWidth = GlobalFunctions.kwargsSwitchCase('outlineWidth', widgetOutlineWidth, kwargs)
        outlineColor = GlobalFunctions.kwargsSwitchCase('outlineColor', widgetOutlineColor, kwargs)
        borderWidth = GlobalFunctions.kwargsSwitchCase('borderWidth', widgetBorderWidth, kwargs)
        borderRadius = GlobalFunctions.kwargsSwitchCase('borderRadius', 7, kwargs)
        borderedOverlay = GlobalFunctions.kwargsSwitchCase('borderedOverlay', 3, kwargs)
        cursorWidth = GlobalFunctions.kwargsSwitchCase('cursorWidth', 2, kwargs)
        cursorColor = GlobalFunctions.kwargsSwitchCase('cursorColor', accentColor, kwargs)
        cursorBorderRadius = GlobalFunctions.kwargsSwitchCase('cursorBorderRadius', 2, kwargs)
        idleBorderedOverlayColor = GlobalFunctions.kwargsSwitchCase('idleBorderedOverlayColor', widgetFgColor, kwargs)
        activeBorderedOverlayColor = GlobalFunctions.kwargsSwitchCase('activeBorderedOverlayColor', accentColor, kwargs)
        darkenActive = GlobalFunctions.kwargsSwitchCase('darkenActive', 25, kwargs)
        border_top_left_radius = GlobalFunctions.kwargsSwitchCase('border_top_left_radius', -1, kwargs)
        border_top_right_radius = GlobalFunctions.kwargsSwitchCase('border_top_right_radius', -1, kwargs)
        border_bottom_left_radius = GlobalFunctions.kwargsSwitchCase('border_bottom_left_radius', -1, kwargs)
        border_bottom_right_radius = GlobalFunctions.kwargsSwitchCase('border_bottom_right_radius', -1, kwargs)

        textbox.Textbox.visuals(surface, textboxId, color, imageName, text, textColor, textFont, textCoverUp, outlineWidth,
                                outlineColor, borderWidth, borderRadius, borderedOverlay, cursorWidth, cursorColor, cursorBorderRadius, idleBorderedOverlayColor,
                                activeBorderedOverlayColor, darkenActive, border_top_left_radius,
                                border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius)

    def draw(textboxId):
        textbox.Textbox.draw(textboxId)

    def delete(textboxId, **kwargs):
        """
        Optional Arguments:
        start: int
        end: None | int
        """

        start = GlobalFunctions.kwargsSwitchCase('start', 0, kwargs)
        end = GlobalFunctions.kwargsSwitchCase('end', None, kwargs)

        return textbox.Textbox.delete(textboxId, start, end)

    def insert(textboxId, string, **kwargs):
        """
        Optional Arguments:
        place: int
        """

        place = GlobalFunctions.kwargsSwitchCase('place', 0, kwargs)

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

    frame.Frame.update()

    pygame.mouse.set_cursor(GlobalFunctions.cursorRequested)
    GlobalFunctions.cursorRequested = pygame.SYSTEM_CURSOR_ARROW

def draw(surface, drawRect, **kwargs):
    """
    Optional Arguments:
    color: tuple
    imageName: None | str
    outlineWidth: int
    outlineColor: tuple
    borderWidth: int
    borderRadius: int
    border_top_left_radius: int
    border_top_right_radius: int
    border_bottom_left_radius: int
    border_bottom_right_radius: int
    """

    color = GlobalFunctions.kwargsSwitchCase('color', fgColor, kwargs)
    imageName = GlobalFunctions.kwargsSwitchCase('imageName', None, kwargs)
    outlineWidth = GlobalFunctions.kwargsSwitchCase('outlineWidth', widgetOutlineWidth, kwargs)
    outlineColor = GlobalFunctions.kwargsSwitchCase('outlineColor', widgetOutlineColor, kwargs)
    borderWidth = GlobalFunctions.kwargsSwitchCase('borderWidth', widgetBorderWidth, kwargs)
    borderRadius = GlobalFunctions.kwargsSwitchCase('borderRadius', 10, kwargs)
    border_top_left_radius = GlobalFunctions.kwargsSwitchCase('border_top_left_radius', -1, kwargs)
    border_top_right_radius = GlobalFunctions.kwargsSwitchCase('border_top_right_radius', -1, kwargs)
    border_bottom_left_radius = GlobalFunctions.kwargsSwitchCase('border_bottom_left_radius', -1, kwargs)
    border_bottom_right_radius = GlobalFunctions.kwargsSwitchCase('border_bottom_right_radius', -1, kwargs)

    return GlobalFunctions.draw(surface, drawRect, color, imageName, outlineWidth, outlineColor, borderWidth, borderRadius,
                                border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                                border_bottom_right_radius)

def requestCursor(cursorType = pygame.SYSTEM_CURSOR_ARROW):
    GlobalFunctions.cursorRequested = cursorType