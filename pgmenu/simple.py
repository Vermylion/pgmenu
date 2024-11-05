import pygame
import pgmenu


# Project that simplifies pgmenu syntax to tkinter level
# Meant to be as easy to use as tkinter, but using the superior pgmenu
# TODO -> Work on finishing PgmenuWindow, right now it's just a demo to show that it's possible
class PgmenuWindow:

    def __init__(self,
                 size: tuple[int, int] = (230, 210),
                 title: str = "pgmenu",
                 fps: int = 60,
                 flags: int = pygame.RESIZABLE):

        self.size = size
        self.title = title
        self.fps = fps
        self.flags = flags
        # Args used later on
        self.blit_surfaces = dict()

        # Set the theme based on system too

        pygame.init()

        self.screen = pygame.display.set_mode(self.size, self.flags)
        pygame.display.set_caption(self.title)

        # Change logo to pgmenu logo

        self.clock = pygame.time.Clock()

    def blit(self, surface, dest):
        self.blit_surfaces[surface] = dest

    def loop(self, loop=None):
        running = True
        while running:

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                self.screen = pgmenu.display.fullscreen_controls(self.screen, event)

            self.screen.fill(pgmenu.Theme.bgcolor)  # Normally pgmenu.Theme.background

            if loop is not None:
                loop()

            for surface in self.blit_surfaces:
                self.screen.blit(surface, self.blit_surfaces[surface])

            pgmenu.draw_all()

            pgmenu.update(events)
            pygame.display.flip()
            self.clock.tick(self.fps)
