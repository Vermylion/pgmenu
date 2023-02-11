import pygame

import GlobalFunctions
import frame

imageBase = dict({})
imageCount = 0


class Image:
    def __init__(self) -> None:
        pass

    def create(surface, imageName, coords, dimensions):
        global imageBase, imageCount
        if str(surface).split()[0] == 'Frame':
            if frame.frameBase[2] == 'enabled':
                surface = frame.frameBase[1]
            else:
                surface = frame.frameVisuals[surface][0]

        imageCount += 1
        imageId = f'Image {imageCount}'
        imageRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        imageBase[imageId] = [imageRect, surface, imageName]

        return imageId

    def modify(imageId, surface, imageName, coords, dimensions):
        global imageBase, imageCount

        if str(surface).split()[0] == 'Frame':
            if frame.frameBase[surface][2] == 'enabled':
                surface = frame.frameBase[surface][1]
            else:
                surface = frame.frameVisuals[surface][0]

        imageRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        imageBase[imageId] = [imageRect, surface, imageName]

        return imageId

    def draw(imageId):
        global imageBase

        GlobalFunctions.draw(imageBase[imageId][1], imageBase[imageId][0], image=imageBase[imageId][2])

    def set(imageName):
        imageSurf = pygame.image.load(imageName).convert_alpha()
        return imageSurf
