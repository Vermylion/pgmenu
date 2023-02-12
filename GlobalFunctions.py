import pygame

imageSurfaces = dict({})

cursorRequested = pygame.SYSTEM_CURSOR_ARROW

Themes = {
    'BLUE': {
        'widgetFgColor': (50, 135, 235),
        'widgetBgColor': (230, 230, 230),
        'widgetOutlineColor': (30, 115, 215),
        'widgetOutlineWidth': 0,
        'widgetTextFgColor': (230, 230, 230),
        'widgetTextBgColor': (20, 20, 20)
    },

    'RED': {
        'widgetFgColor': (235, 50, 50),
        'widgetBgColor': (230, 230, 230),
        'widgetOutlineColor': (215, 30, 30),
        'widgetOutlineWidth': 0,
        'widgetTextFgColor': (230, 230, 230),
        'widgetTextBgColor': (20, 20, 20)
    },

    'YELLOW': {
        'widgetFgColor': (235, 210, 50),
        'widgetBgColor': (230, 230, 230),
        'widgetOutlineColor': (215, 190, 30),
        'widgetOutlineWidth': 0,
        'widgetTextFgColor': (20, 20, 20),
        'widgetTextBgColor': (30, 30, 30)
    },

    'YELLOW&BLACK': {
        'widgetFgColor': (50, 50, 50),
        'widgetBgColor': (20, 20, 20),
        'widgetOutlineColor': (235, 210, 50),
        'widgetOutlineWidth': 2,
        'widgetTextFgColor': (230, 230, 230),
        'widgetTextBgColor': (230, 230, 230)
    },
}


def createTheme(themeName, fgColor, bgColor, outlineColor, outlineWidth, textFgColor, textBgColor):
    Themes[str(themeName)] = {
        'widgetFgColor': fgColor,
        'widgetBgColor': bgColor,
        'widgetOutlineColor': outlineColor,
        'widgetOutlineWidth': outlineWidth,
        'widgetTextFgColor': textFgColor,
        'widgetTextBgColor': textBgColor}


def create_image_surface(widgetRect, image):
    global imageSurfaces

    loadedImage = pygame.image.load(image).convert_alpha()
    resizedImage = pygame.transform.scale(loadedImage, (widgetRect[2], widgetRect[3]))

    imageSurfaces[str([widgetRect, image])] = resizedImage

    return resizedImage


def draw(surface, drawRect, color=(255, 255, 255), image=None, outlineWidth=0, outlineColor=(0, 0, 0), borderWidth=0,
         borderRadius=10, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1,
         border_bottom_right_radius=-1):
    drawSurface = pygame.Surface((drawRect[2] + (outlineWidth * 2), drawRect[3] + (outlineWidth * 2)), pygame.SRCALPHA)

    if image != None:
        if not str([drawRect, image]) in imageSurfaces:
            create_image_surface(drawRect, image)
        imageSurface = imageSurfaces[str([drawRect, image])]
        drawSurface.blit(imageSurface, (outlineWidth, outlineWidth))

    else:
        if outlineWidth > 0:
            outlineRect = pygame.Rect(0, 0, drawRect[2] + (outlineWidth * 2), drawRect[3] + (outlineWidth * 2))
            pygame.draw.rect(drawSurface, outlineColor, outlineRect, borderWidth, borderRadius, border_top_left_radius,
                             border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius)

        mainRect = pygame.Rect(outlineWidth, outlineWidth, drawRect[2], drawRect[3])
        pygame.draw.rect(drawSurface, color, mainRect, borderWidth, borderRadius, border_top_left_radius,
                         border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius)

    surface.blit(drawSurface, (drawRect[0] - outlineWidth, drawRect[1] - outlineWidth))

    return drawSurface

def frameOffset(surface, widgetId, widgetBase, frameBase, frameVisuals):
    if str(surface).split()[0] == 'Frame':
        print(widgetBase[widgetId][0])
        widgetX, widgetY = widgetBase[widgetId][0][0] + frameBase[surface][0][0], widgetBase[widgetId][0][1] + \
                           frameBase[surface][0][1]
        if frameBase[surface][2] == 'disabled':
            widgetX, widgetY = widgetX - frameBase[surface][0][0], widgetY - frameBase[surface][0][1]
        surface = frameVisuals[surface][0]
        widgetBase[widgetId][0] = pygame.Rect(widgetX, widgetY, widgetBase[widgetId][0][2], widgetBase[widgetId][0][3])
        print(widgetBase[widgetId][0])
    return surface
