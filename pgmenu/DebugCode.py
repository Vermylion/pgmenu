# Taken from husano896's PR thread (slightly modified)
import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

def main():
   while True:
      for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               return
            elif event.type == MOUSEWHEEL:
               print(event)
               print(event.x, event.y)
               print(event.flipped)
               # print(event.which)
               # can access properties with
               # proper notation(ex: event.y)
      clock.tick(60)

# Execute game:
main()