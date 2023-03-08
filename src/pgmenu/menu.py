import pgmenu.button as button
import pgmenu.checkbox as checkbox
import pgmenu.frame as frame
import pgmenu.image as imagefile
import pgmenu.text as textfile
import pgmenu.textbox as textbox

menus = dict({})
activeMenu = ''


class Menu:
    def __init__(self) -> None:
        pass

    def create(menuName):
        global menus

        menus[menuName] = []

    def delete(menuName):
        global menus

        del menus[menuName]

    def add(menuName, *widgetIds):
        global menus

        if not menuName in menus:
            Menu.create(menuName)

        for widgetId in widgetIds:
            menus[menuName].append(widgetId)

    def remove(menuName, *widgetIds):
        global menus

        for widgetId in widgetIds:
            menus[menuName].remove(widgetId)

    def show(menuName):
        global activeMenu

        Menu.disableAll()
        Menu.enable(menuName)

        activeMenu = menuName

    def draw(menuName=None):
        if type(menuName) != str:
            menuName = activeMenu

        for widgetId in menus[menuName]:
            # widget check
            if widgetId.split()[0] == 'Button':
                button.Button.draw(widgetId)
            if widgetId.split()[0] == 'Checkbox':
                checkbox.Checkbox.draw(widgetId)
            if widgetId.split()[0] == 'Textbox':
                textbox.Textbox.draw(widgetId)
            if widgetId.split()[0] == 'Text':
                textfile.Text.draw(widgetId)
            if widgetId.split()[0] == 'Image':
                imagefile.Image.draw(widgetId)
            if widgetId.split()[0] == 'Frame':
                frame.Frame.draw(widgetId)

    def enable(menuName):
        for widgetId in menus[menuName]:
            # widget check
            if widgetId.split()[0] == 'Button':
                button.Button.enable(widgetId)
            elif widgetId.split()[0] == 'Checkbox':
                checkbox.Checkbox.enable(widgetId)
            elif widgetId.split()[0] == 'Textbox':
                textbox.Textbox.enable(widgetId)

    def disable(menuName):
        for widgetId in menus[menuName]:
            # widget check
            if widgetId.split()[0] == 'Button':
                button.Button.disable(widgetId)
            elif widgetId.split()[0] == 'Checkbox':
                checkbox.Checkbox.disable(widgetId)
            elif widgetId.split()[0] == 'Textbox':
                textbox.Textbox.disable(widgetId)

    def enableAll():
        for menu in menus:
            Menu.enable(menu)

    def disableAll():
        for menu in menus:
            Menu.disable(menu)
