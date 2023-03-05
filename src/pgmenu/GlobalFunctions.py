import pygame
from PIL import Image as PilImage, ImageDraw

imageSurfaces = dict({})

cursorRequested = pygame.SYSTEM_CURSOR_ARROW

def kwargsSwitchCase(varName, baseSettings, kwargs):
    if str(varName) in kwargs:
      return kwargs[str(varName)]
    else:
        return baseSettings


def modifyColor(color, changeby, limit):
    color = list(color)
    color[0], color[1], color[2] = max(color[0] + changeby, limit), max(color[1] + changeby, limit), max(color[2] + changeby, limit)
    color = tuple(color)

    return color


def create_image_surface(widgetRect, imageName, borderRadius):
    global imageSurfaces

    if borderRadius > 0:
        image = PilImage.open(imageName)

        image = image.resize((widgetRect[2], widgetRect[3]))

        # Round off corners of PIL image
        circle = PilImage.new('L', (borderRadius * 2, borderRadius * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, borderRadius * 2 - 1, borderRadius * 2 - 1), fill=255)
        alpha = PilImage.new('L', image.size, 255)
        w, h = image.size
        alpha.paste(circle.crop((0, 0, borderRadius, borderRadius)), (0, 0))
        alpha.paste(circle.crop((0, borderRadius, borderRadius, borderRadius * 2)), (0, h - borderRadius))
        alpha.paste(circle.crop((borderRadius, 0, borderRadius * 2, borderRadius)), (w - borderRadius, 0))
        alpha.paste(circle.crop((borderRadius, borderRadius, borderRadius * 2, borderRadius * 2)),
                    (w - borderRadius, h - borderRadius))
        image.putalpha(alpha)

        # Convert PIL image to pygame surface
        image = pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert_alpha()

    else:
        loadedImage = pygame.image.load(imageName).convert_alpha()
        image = pygame.transform.scale(loadedImage, (widgetRect[2], widgetRect[3]))

    imageSurfaces[str([widgetRect, imageName, borderRadius])] = image

    return image


def draw(surface, drawRect, color=(255, 255, 255), imageName=None, outlineWidth=0, outlineColor=(0, 0, 0), borderWidth=0,
         borderRadius=10, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1,
         border_bottom_right_radius=-1):
    drawSurface = pygame.Surface((drawRect[2] + (outlineWidth * 2), drawRect[3] + (outlineWidth * 2)), pygame.SRCALPHA)

    if imageName != None:
        if not str([drawRect, imageName, borderRadius]) in imageSurfaces:
            create_image_surface(drawRect, imageName, borderRadius)
        imageSurface = imageSurfaces[str([drawRect, imageName, borderRadius])]
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