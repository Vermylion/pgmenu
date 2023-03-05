import pygame
import darkdetect

import GlobalFunctions

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

Themes = {
    'BLUE': {
        'accentColor': (50, 135, 235),
        'widgetOutlineColor': (40, 105, 185)
    },

    'RED': {
        'accentColor': (235, 50, 50),
        'widgetOutlineColor': (185, 40, 40)
    },

    'GREEN': {
        'accentColor': (40, 185, 120),
        'widgetOutlineColor': (30, 135, 90),
    },

    'YELLOW': {
        'accentColor': (235, 210, 50),
        'widgetOutlineColor': (185, 165, 40)
    },

    'PURPLE': {
        'accentColor': (130, 50, 235),
        'widgetOutlineColor': (100, 40, 185)
    },

    'BLUE&BLACK': {
        'accentColor': (25, 25, 25),
        'widgetOutlineColor': (50, 135, 235),
        'widgetOutlineWidth': 2
    },

    'RED&BLACK': {
        'accentColor': (25, 25, 25),
        'widgetOutlineColor': (235, 50, 50),
        'widgetOutlineWidth': 2
    },

    'GREEN&BLACK': {
        'accentColor': (25, 25, 25),
        'widgetOutlineColor': (40, 185, 120),
        'widgetOutlineWidth': 2
    },

    'YELLOW&BLACK': {
        'accentColor': (25, 25, 25),
        'widgetOutlineColor': (235, 210, 50),
        'widgetOutlineWidth': 2
    },

    'PURPLE&BLACK': {
        'accentColor': (25, 25, 25),
        'widgetOutlineColor': (130, 50, 235),
        'widgetOutlineWidth': 2
    }
}

def themesSwitchCase(varName, selectedTheme):
    if varName in Themes[selectedTheme]:
        return Themes[selectedTheme][varName]
    else:
        return globals()[varName]

class Theme:
    def __int__(self) -> None:
        pass

    def mode(modeType):
        global mainColor, bgColor, fgColor, widgetBgColor, widgetFgColor, textFgColor, textBgColor

        if modeType.lower() == 'system':
            modeType = darkdetect.theme()

        if modeType.lower() == 'light':
            mainColor = (255, 255, 255)
            bgColor = (230, 230, 230)
            fgColor = (210, 210, 210)
            widgetBgColor = (190, 190, 190)
            widgetFgColor = (160, 160, 160)

            textFgColor = (240, 240, 240)
            textBgColor = (10, 10, 10)
        else:
            mainColor = (0, 0, 0)
            bgColor = (30, 30, 30)
            fgColor = (50, 50, 50)
            widgetBgColor = (70, 70, 70)
            widgetFgColor = (100, 100, 100)

            textFgColor = (240, 240, 240)
            textBgColor = (240, 240, 240)


    def set(themeName):
        global mainColor; mainColor = themesSwitchCase('mainColor', themeName)
        global bgColor; bgColor = themesSwitchCase('bgColor', themeName)
        global fgColor; fgColor = themesSwitchCase('fgColor', themeName)
        global widgetBgColor; widgetBgColor = themesSwitchCase('widgetBgColor', themeName)
        global widgetFgColor; widgetFgColor = themesSwitchCase('widgetFgColor', themeName)

        global textFgColor; textFgColor = themesSwitchCase('textFgColor', themeName)
        global textBgColor; textBgColor = themesSwitchCase('textBgColor', themeName)

        global widgetOutlineColor; widgetOutlineColor = themesSwitchCase('widgetOutlineColor', themeName)
        global widgetOutlineWidth; widgetOutlineWidth = themesSwitchCase('widgetOutlineWidth', themeName)
        global widgetBorderWidth; widgetBorderWidth = themesSwitchCase('widgetBorderWidth', themeName)

        global accentColor; accentColor = themesSwitchCase('accentColor', themeName)

    def custom(themeName, **kwargs):
        global Themes

        for arg in kwargs:
            if not themeName in Themes:
                Themes[themeName] = {arg: kwargs[arg]}
            else:
                Themes[themeName][arg] = kwargs[arg]