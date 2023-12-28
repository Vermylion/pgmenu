import pygame
import pygame.gfxdraw
import math
import time

global cached_surfaces
cached_surfaces = dict()


# TODO: Tweak antialiasing formulas for aa_corners inside and aa_sides inside

# A Class that will make an antialiased rectangle object
# Everything is created when class is initiated
class AARect:

    def __init__(self,
                 surface: pygame.Surface,
                 fill: list | tuple | pygame.Surface,
                 rect: list | tuple | pygame.Rect,
                 width: int = 0,
                 border_radius: int = 0,
                 border_top_left_radius: None = None,
                 border_top_right_radius: None = None,
                 border_bottom_left_radius: None = None,
                 border_bottom_right_radius: None = None,
                 anti_aliasing: bool = True,
                 transparency: int = 255,
                 aa_strength: int = 1,
                 **kwargs):

        self.object_cache_id = None
        self.aa_alpha_pixels = dict()

        self.surface = surface
        self.fill = fill
        self.rect = rect
        self.width = width
        self.border_radius = border_radius
        self.border_top_left_radius = border_top_left_radius if border_top_left_radius else self.border_radius
        self.border_top_right_radius = border_top_right_radius if border_top_right_radius else self.border_radius
        self.border_bottom_left_radius = border_bottom_left_radius if border_bottom_left_radius else self.border_radius
        self.border_bottom_right_radius = border_bottom_right_radius if border_bottom_right_radius else self.border_radius
        self.anti_aliasing = anti_aliasing
        self.transparency = transparency
        self.aa_strength = aa_strength

        self.draw_border_top_left_radius = False
        self.draw_border_top_right_radius = False
        self.draw_border_bottom_left_radius = False
        self.draw_border_bottom_right_radius = False

        self.border_radius_values = {'draw_border_top_left_radius': self.border_top_left_radius,
                                     'draw_border_top_right_radius': self.border_top_right_radius,
                                     'draw_border_bottom_left_radius': self.border_bottom_left_radius,
                                     'draw_border_bottom_right_radius': self.border_bottom_right_radius}

        # Additional parameters for modifying inside rect
        self.inside_fill = kwargs['inside_fill'] if 'inside_fill' in kwargs else self.fill
        self.inside_transparency = kwargs['inside_transparency'] if 'inside_transparency' in kwargs else self.transparency
        # Changing border_radius doesn't do anything. Can be implemented in the future if need be
        self.inside_border_radius = kwargs['inside_border_radius'] if 'inside_border_radius' in kwargs else self.border_radius
        self.inside_border_top_left_radius = kwargs['inside_border_top_left_radius'] if 'inside_border_top_left_radius' in kwargs else self.inside_border_radius
        self.inside_border_top_right_radius = kwargs['inside_border_top_right_radius'] if 'inside_border_top_right_radius' in kwargs else self.inside_border_radius
        self.inside_border_bottom_left_radius = kwargs['inside_border_bottom_left_radius'] if 'inside_border_bottom_left_radius' in kwargs else self.inside_border_radius
        self.inside_border_bottom_right_radius = kwargs['inside_border_bottom_right_radius'] if 'inside_border_bottom_right_radius' in kwargs else self.inside_border_radius

        # Start antialiased rect process
        # Creating it or retrieving it from cache
        self.aarect()

    # Small function that calls other main functions
    # Allows appeal to function names
    # -> Creates or retrieves rect
    def aarect(self):
        # Format arguments
        self.format_rect()

        # If object doesn't exist, create it
        if self.object_cache_id not in cached_surfaces:
            # Debug timer
            start = time.time()
            self.create_rect()
            end = time.time()
            print(f"Drawing aa rect: End: {end}, Start: {start}, Seconds: {round(end - start, 4)} s, MS: {round((end - start) * 1000)} ms, FPS: {round(1 / (end - start))} fps")

        # retrieve object from cache
        rect_surface = cached_surfaces[self.object_cache_id]

        self.surface.blit(rect_surface, (self.rect[0], self.rect[1]))

    # Formats rect arguments correctly
    def format_rect(self):
        global cached_surfaces

        # Manage fill values
        if not isinstance(self.fill, tuple) and not isinstance(self.fill, list) and not isinstance(self.fill, pygame.Surface):
            raise TypeError("Fill type should be either tuple/list or pygame.Surface.")

        # Manage transparency / alpha value
        if self.fill is tuple or self.fill is list:
            if len(self.fill) == 4:
                self.transparency = self.fill[3]
                self.fill = tuple(list(self.fill)[0:3])

        # Resize surface
        if self.fill is pygame.Surface:
            self.fill = pygame.transform.scale(self.fill, (self.rect[2], self.rect[3]))

        # Limit width
        self.width = round(min(self.width, (min(self.rect[2], self.rect[3]) / 2)))

        # Limit radius
        self.border_radius = round(min(self.border_radius, (min(self.rect[2], self.rect[3]) / 2)))
        self.border_top_left_radius = round(min(self.border_top_left_radius, (min(self.rect[2], self.rect[3]) / 2)))
        self.border_top_right_radius = round(min(self.border_top_right_radius, (min(self.rect[2], self.rect[3]) / 2)))
        self.border_bottom_left_radius = round(min(self.border_bottom_left_radius, (min(self.rect[2], self.rect[3]) / 2)))
        self.border_bottom_right_radius = round(min(self.border_bottom_right_radius, (min(self.rect[2], self.rect[3]) / 2)))

        # Reformat border_radius list
        self.border_radius_values = {'draw_border_top_left_radius': self.border_top_left_radius,
                                     'draw_border_top_right_radius': self.border_top_right_radius,
                                     'draw_border_bottom_left_radius': self.border_bottom_left_radius,
                                     'draw_border_bottom_right_radius': self.border_bottom_right_radius}

        # Set anti_aliasing bool
        if self.border_radius <= 0:
            self.anti_aliasing = False

        self.object_cache_id = (str(self.fill), (self.rect[2], self.rect[3]), self.width, self.border_radius, self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius, self.anti_aliasing, self.transparency, self.aa_strength)

    def create_rect(self):
        global cached_surfaces
        aa_pixel_width = self.aa_strength if self.anti_aliasing else 0

        # Get outside antialiased rounded surface
        # Debug timer
        start = time.time()
        rect_surface = self.draw_rect(inside_border=False)
        end = time.time()
        print(f"Drawing outside surf: End: {end}, Start: {start}, Seconds: {round(end - start, 4)} s, MS: {round((end - start) * 1000)} ms, FPS: {round(1 / (end - start))} fps")

        if self.width:
            # Get inside antialiased rounded surface
            # Debug timer
            start = time.time()
            rect_surface_inside = self.draw_rect((self.rect[0], self.rect[1], self.rect[2] - self.width * 2 - aa_pixel_width * 2, self.rect[3] - self.width * 2 - aa_pixel_width * 2), True)
            end = time.time()
            print(f"Drawing inside surf: End: {end}, Start: {start}, Seconds: {round(end - start, 4)} s, MS: {round((end - start) * 1000)} ms, FPS: {round(1 / (end - start))} fps")

            # Remove inside rect from the rest of the rect
            rect_surface.blit(rect_surface_inside, (self.width + aa_pixel_width, self.width + aa_pixel_width), special_flags=pygame.BLEND_RGBA_SUB)

        cached_surfaces[(str(self.fill), (self.rect[2], self.rect[3]), self.width, self.border_radius, self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius, self.anti_aliasing, self.transparency, self.aa_strength)] = rect_surface

    def draw_rect(self, rect = None, inside_border = False):
        fill = self.inside_fill if inside_border else self.fill
        transparency = self.inside_transparency if inside_border else self.transparency

        self.aa_alpha_pixels = dict()
        aa_pixel_width = self.aa_strength if self.anti_aliasing else 0
        rect = rect if rect is not None else self.rect

        # Exit if one of the rect values is 0 or less
        if rect[2] < 1 or rect[3] < 1:
            draw_rect_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
            return draw_rect_surface

        # Calls every corner in an efficient manner
        # aa_corners() called in func
        self.get_corners(rect, inside_border)

        # Get aa sides if border_radius is bigger than aa_strength
        if self.border_radius >= aa_pixel_width:
            self.aa_sides(rect, inside_border)

        draw_rect_surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        is_surface = fill is pygame.Surface

        # Draw out the rect
        for x in range(rect[2]):
            for y in range(rect[3]):

                # Check if pixel has been manipulated and set pixel alpha
                if (x, y) in self.aa_alpha_pixels:
                    alpha = self.aa_alpha_pixels[(x, y)]
                    # Takes away additional transparency
                    alpha = alpha - (255 - transparency)
                    # Restrain alpha to 0, and not lower
                    if alpha < 0:
                        alpha = 0
                else:
                    alpha = transparency

                # Draw only visible pixels
                if alpha != 0:

                    # Get color from surface if self.fill is pygame.Surface
                    if is_surface:
                        color = pygame.Surface.get_at(fill, (x, y))
                        if color[3] != 255:
                            alpha = color[3]
                        color = (color[0], color[1], color[2], alpha)
                    else:
                        color = (*fill, alpha)

                    pygame.gfxdraw.pixel(draw_rect_surface, x, y, color)

        self.aa_alpha_pixels = dict()

        return draw_rect_surface

    def get_corners(self, rect = None, inside_border = False):
        aa_pixel_width = self.aa_strength if self.anti_aliasing else 0
        rect = rect if rect is not None else self.rect
        border_radius_values = self.border_radius_values.copy()
        dict_values_to_remove = []

        # Make the corners; if multiple are the same, they will be done at the same time
        while True:
            # Stop while loop if all corners are done
            if len(border_radius_values) == 0:
                break

            # Reset all draw_border vars to False
            for var_name in self.border_radius_values:
                setattr(self, var_name, False)

            for border_radius_name in border_radius_values:
                if border_radius_values[border_radius_name] == list(border_radius_values.values())[0]:
                    setattr(self, border_radius_name, True)
                    dict_values_to_remove.append(border_radius_name)

            border_radius = list(border_radius_values.values())[0]
            if inside_border:
                # Shrink border_radius if it's an inside border_radius
                # Limit border_radius to 0
                border_radius = max(border_radius - self.width - aa_pixel_width, 0)

            if border_radius > 0:
                self.aa_corners(border_radius, rect, inside_border)

            # Delete done corners from corners to do
            for dict_key in dict_values_to_remove:
                del border_radius_values[dict_key]
            dict_values_to_remove = []

    # Returns pixels outside the circle / given radius
    # Calculates 1 corner and then mirrors it to return 4
    def aa_corners(self, border_radius, rect = None, inside_border = False):
        transparency = self.inside_transparency if inside_border else self.transparency

        aa_pixel_width = self.aa_strength if self.anti_aliasing else 0
        aa_pixel_width_displacement = aa_pixel_width + 1 if self.anti_aliasing else aa_pixel_width
        rect = rect if rect is not None else self.rect

        for x in range(border_radius):
            x_offset = rect[2] - x - 1

            for y in range(border_radius):
                y_offset = rect[3] - y - 1

                # Formula that calculates the distance of a pixel from the center of the circle
                distance = math.sqrt((x - border_radius) ** 2 + (y - border_radius) ** 2)
                pixel_distance = round(distance)

                if pixel_distance > border_radius - aa_pixel_width_displacement:

                    if self.anti_aliasing and pixel_distance <= border_radius:
                        if inside_border:
                            alpha = ((distance - (border_radius - 1)) + 1) * (transparency / (aa_pixel_width + 2))
                            alpha = 255 - alpha
                        else:
                            alpha = ((-distance + border_radius + 1) + 1) * (transparency / (aa_pixel_width + 2))

                        if alpha > 255:
                            alpha = 255
                    else:
                        alpha = 0

                    # Save pixels' pos and alpha
                    # Mirrors pixel to fill the 4 total corners
                    if self.draw_border_top_left_radius:
                        self.aa_alpha_pixels[(x, y)] = alpha
                    if self.draw_border_top_right_radius:
                        self.aa_alpha_pixels[(x_offset, y)] = alpha
                    if self.draw_border_bottom_left_radius:
                        self.aa_alpha_pixels[(x, y_offset)] = alpha
                    if self.draw_border_bottom_right_radius:
                        self.aa_alpha_pixels[(x_offset, y_offset)] = alpha

        return self.aa_alpha_pixels

    # Calculate antialiasing for the outside sides of the rect
    def aa_sides(self, rect = None, inside_border = False):
        transparency = self.inside_transparency if inside_border else self.transparency

        aa_pixel_width = self.aa_strength if self.anti_aliasing else 0
        rect = rect if rect is not None else self.rect

        # Shrink all border_radius if it's an inside border
        border_top_left_radius = self.border_top_left_radius - self.width - aa_pixel_width if inside_border else self.border_top_left_radius
        border_top_right_radius = self.border_top_right_radius - self.width - aa_pixel_width if inside_border else self.border_top_right_radius
        border_bottom_left_radius = self.border_bottom_left_radius - self.width - aa_pixel_width if inside_border else self.border_bottom_left_radius
        border_bottom_right_radius = self.border_bottom_right_radius - self.width - aa_pixel_width if inside_border else self.border_bottom_right_radius

        for alpha_pos in range(1, aa_pixel_width + 1):
            if inside_border:
                alpha_value = (alpha_pos + 1) * (transparency / (aa_pixel_width + 2))
                alpha_value = 255 - alpha_value
            else:
                alpha_value = (alpha_pos + 1) * (transparency / (aa_pixel_width + 2))

            # Left Side
            for y in range(rect[3] - (border_top_left_radius + border_bottom_left_radius)):
                self.aa_alpha_pixels[(alpha_pos - 1, y + border_top_left_radius)] = alpha_value
            # Right Side
            for y in range(rect[3] - (border_top_right_radius + border_bottom_right_radius)):
                self.aa_alpha_pixels[(rect[2] - alpha_pos, y + border_top_right_radius)] = alpha_value

            # Top Side
            for x in range(rect[2] - (border_top_left_radius + border_top_right_radius)):
                self.aa_alpha_pixels[(x + border_top_left_radius, alpha_pos - 1)] = alpha_value
            # Bottom Side
            for x in range(rect[2] - (border_bottom_left_radius + border_bottom_right_radius)):
                self.aa_alpha_pixels[(x + border_bottom_left_radius, rect[3] - alpha_pos)] = alpha_value

        return self.aa_alpha_pixels