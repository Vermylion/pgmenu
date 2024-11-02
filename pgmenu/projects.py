# A collection of small, skeleton projects
# The user can use them for starting a project, see how to do it, use it in a project, etc.
# This collection should hopefully grow over time, and is meant to help the user


import pygame
import pgmenu

from pgmenu.animation import Animate


# FIXME -> really bad, doesn't work really well -> only a demo
# Infrastructure for projects, allowing x, y movements, and zooming in and out
class MovablePlaneWindow:

    def __init__(self, screen, **kwargs):
        self.screen = screen

        self.relative_window_x = 0
        self.relative_window_y = 0

        self.relative_scale = Animate(0.5, 1, duration=0.5)
        self.scale_speed = 0.1 if "scale_speed" not in kwargs else kwargs["scale_speed"]
        self.min_scale = 0.1 if "min_scale" not in kwargs else kwargs["min_scale"]

        self.move_point_x = 0
        self.move_point_y = 0
        self.move_speed = 1 if "move_speed" not in kwargs else kwargs["move_speed"]
        self.moving = False

        self.surfaces = []

        self.move_button = pygame.BUTTON_RIGHT if "move_button" not in kwargs else kwargs["move_button"]

        self.resize = self.m_resize if "resize" not in kwargs else kwargs["resize"]

    def clear(self):
        self.surfaces = []

    def blit(self, surface, dest):
        if not [dest, surface] in self.surfaces:
            self.surfaces.append([surface, dest, surface.get_size()])

    def controls(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == self.move_button:
                self.moving = True

                x, y = event.pos
                self.move_point_x = x
                self.move_point_y = y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == self.move_button:
                self.moving = False

        if event.type == pygame.MOUSEWHEEL:
            # Calculate relative scale
            new_relative_scale = max(
                round(self.relative_scale.num + event.y * self.scale_speed, len(str(self.scale_speed))), self.min_scale)
            self.relative_scale = Animate(self.relative_scale.num, new_relative_scale)

        if self.moving:
            x, y = pygame.mouse.get_pos()

            self.relative_window_x -= round(((x - self.move_point_x) * self.move_speed) / self.relative_scale.num)
            self.relative_window_y -= round(((y - self.move_point_y) * self.move_speed) / self.relative_scale.num)

            self.move_point_x = x
            self.move_point_y = y

    def m_resize(self, surface, coords, size, new_size):
        resized_surface = pygame.transform.scale(surface, new_size)
        self.surfaces[self.surfaces.index([surface, coords, size])][0] = resized_surface

        return resized_surface

    def draw(self):
        # Acts as update sequence

        # Run if relative_scale animation is not finished
        if not self.relative_scale.done:
            x, y = pygame.mouse.get_pos()

            # Allows zoom on mouse cursor pos
            self.relative_window_x += round(x / self.relative_scale.num)
            self.relative_window_y += round(y / self.relative_scale.num)

            # Update zoom animation if need be for smooth zoom
            self.relative_scale.update()

            # Allows zoom on mouse cursor pos
            self.relative_window_x -= round(x / self.relative_scale.num)
            self.relative_window_y -= round(y / self.relative_scale.num)

        for surface, coords, size in self.surfaces:

            # coord - relative_window -> places surface on screen based on how the plane was moved -> if it's in focus
            # * relative_scale -> moves coords based on zoom
            coord_x = (coords[0] - self.relative_window_x) * self.relative_scale.num
            coord_y = (coords[1] - self.relative_window_y) * self.relative_scale.num

            width, height = pygame.display.get_window_size()

            w_f = 20  # Wiggle factor to render outside of view, not the best solution but works
            if 0 - w_f < coord_x + size[0] < width + size[0] + w_f and 0 - w_f < coord_y + size[1] < height + size[
                1] + w_f:

                # Calculate new zoomed in/out size, capped at a minimum of 1
                new_size = (
                    max(round(size[0] * self.relative_scale.num), 1), max(round(size[1] * self.relative_scale.num), 1))

                if surface.get_size() != new_size:
                    # Resize the surface and change it in the dict
                    surface = self.resize(surface, coords, size, new_size)

            self.screen.blit(surface, (coord_x, coord_y))


# Project to help load as images or surfaces the gradients for modern ui
def modern_ui():
    ...
