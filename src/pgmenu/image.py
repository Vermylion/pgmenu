import pygame

import pgmenu.GlobalFunctions as GlobalFunctions

imageBase = dict({})
imageCount = 0


class Image:
    def __init__(self) -> None:
        pass

    def create(surface, imageName, coords, dimensions, borderRadius):
        global imageBase, imageCount

        imageCount += 1
        imageId = f'Image {imageCount}'
        imageRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        imageBase[imageId] = [imageRect, surface, imageName, borderRadius]

        return imageId

    def modify(imageId, **kwargs):
        global imageBase, imageCount

        surface = GlobalFunctions.kwargsSwitchCase('surface', imageBase[imageId][1], kwargs)
        imageName = GlobalFunctions.kwargsSwitchCase('imageName', imageBase[imageId][2], kwargs)
        coords = GlobalFunctions.kwargsSwitchCase('coords', (imageBase[imageId][0][0], imageBase[imageId][0][1]), kwargs)
        dimensions = GlobalFunctions.kwargsSwitchCase('dimensions', (imageBase[imageId][0][2], imageBase[imageId][0][3]), kwargs)
        borderRadius = GlobalFunctions.kwargsSwitchCase('borderRadius', imageBase[imageId][3], kwargs)

        imageRect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        imageBase[imageId] = [imageRect, surface, imageName, borderRadius]

        return imageId

    def draw(imageId):
        global imageBase

        GlobalFunctions.draw(imageBase[imageId][1], imageBase[imageId][0], imageName=imageBase[imageId][2], borderRadius=imageBase[imageId][3])

    def set(imageName):
        imageSurf = pygame.image.load(imageName).convert_alpha()
        return imageSurf

    def size(imageName, resizeRatio):
        imageSize = Image.set(imageName).get_size()

        imageSize =  (imageSize[0] / resizeRatio, imageSize[1] / resizeRatio)

        return imageSize