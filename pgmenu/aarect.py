import pygame
import pygame.gfxdraw
import math
import time

import pgmenu
import pgmenu.utils as utils
from pgmenu.vars import cache


# TODO -> Look into alternatives for inside rect antialiasing, instead of using (alpha, alpha, alpha, alpha)

# TODO -> Fix corners artifacts for overlay with removing inside rect

# A Class that will make an antialiased rectangle object
# Everything is created when class is initiated
class AARect:

    def __init__(self,
                 surface: pygame.Surface | None,
                 fill: list | tuple | pygame.Surface | pygame.Color,
                 rect: list | tuple | pygame.Rect,
                 width: int = 0,
                 border_radius: int = 10,
                 border_top_left_radius: int | None = None,
                 border_top_right_radius: int | None = None,
                 border_bottom_left_radius: int | None = None,
                 border_bottom_right_radius: int | None = None,
                 antialiasing: bool = True,
                 transparency: int = 255,
                 aa_strength: int = 1,
                 **kwargs):
        """

        :param surface:
        :param fill:
        :param rect:
        :param width:
        :param border_radius:
        :param border_top_left_radius:
        :param border_top_right_radius:
        :param border_bottom_left_radius:
        :param border_bottom_right_radius:
        :param antialiasing:
        :param transparency:
        :param aa_strength:
        :param kwargs:
        inner_fill:
        inner_transparency:
        inner_aa_strength:
        inner_antialiasing:
        """

        self.aa_pixels = dict()
        self.aa_surface = None
        self.object_cache_id = None

        self.surface = surface
        self.fill = fill
        self.rect = rect
        self.width = width
        self.border_radius = border_radius
        self.border_top_left_radius = border_top_left_radius if border_top_left_radius is not None else self.border_radius
        self.border_top_right_radius = border_top_right_radius if border_top_right_radius is not None else self.border_radius
        self.border_bottom_left_radius = border_bottom_left_radius if border_bottom_left_radius is not None else self.border_radius
        self.border_bottom_right_radius = border_bottom_right_radius if border_bottom_right_radius is not None else self.border_radius
        self.antialiasing = antialiasing
        self.transparency = transparency
        self.aa_strength = aa_strength

        # Additional parameters for modifying inside rect
        self.inner_fill = kwargs.get('inner_fill', None)
        self.inner_transparency = kwargs.get('inner_transparency', self.transparency)
        self.inner_aa_strength = kwargs.get('inner_aa_strength', self.aa_strength)
        self.inner_antialiasing = kwargs.get('inner_antialiasing', self.antialiasing)
        # Additional parameters
        self.debug = kwargs.get('debug', False)
        self.force_only_overlay = False
        if self.inner_transparency == 255 and self.inner_fill is not None: self.force_only_overlay = True

        # Temp vars for varied use in class
        self.temp_fill = self.fill
        self.temp_rect = self.rect
        self.temp_border_radius = self.border_radius
        self.temp_border_top_left_radius = border_top_left_radius if border_top_left_radius is not None else self.border_top_left_radius
        self.temp_border_top_right_radius = border_top_right_radius if border_top_right_radius is not None else self.border_top_right_radius
        self.temp_border_bottom_left_radius = border_bottom_left_radius if border_bottom_left_radius is not None else self.border_bottom_left_radius
        self.temp_border_bottom_right_radius = border_bottom_right_radius if border_bottom_right_radius is not None else self.border_bottom_right_radius
        self.temp_transparency = self.transparency
        self.temp_antialiasing = self.antialiasing
        self.temp_aa_strength = self.aa_strength

        self.temp_inner_borders = False
        self.temp_inner_aa = False

        # Variables for use inside class
        self.draw_border_top_left_radius = False
        self.draw_border_top_right_radius = False
        self.draw_border_bottom_left_radius = False
        self.draw_border_bottom_right_radius = False

        self.border_radius_values = {'draw_border_top_left_radius': self.temp_border_top_left_radius,
                                     'draw_border_top_right_radius': self.temp_border_top_right_radius,
                                     'draw_border_bottom_left_radius': self.temp_border_bottom_left_radius,
                                     'draw_border_bottom_right_radius': self.temp_border_bottom_right_radius}

    # Small function that calls other main functions
    # Allows appeal to function names
    # -> Creates or retrieves rect
    def aarect(self):
        # Format arguments
        self.format_rect()

        # If object doesn't exist, create it
        if pgmenu.cache.lru_get(cache["aarect"], self.object_cache_id) is None:
            # Debug timer
            start = time.time()
            self.create_rect()
            end = time.time()
            if self.debug:
                print(f"Drawing aa rect: End: {end}, Start: {start}, Seconds: {round(end - start, 4)} s, MS: {round((end - start) * 1000, 2)} ms, FPS: {utils.div(1, (end - start), 0)} fps")

        # retrieve object from cache
        rect_surface = pgmenu.cache.lru_get(cache["aarect"], self.object_cache_id)

        # if surface is None -> not to be blit
        if self.surface:
            self.surface.blit(rect_surface, (self.rect[0], self.rect[1]))

        # Returning copy so any modification done afterward does not modify surface in cache
        return rect_surface.copy()

    # Formats rect arguments correctly
    def format_rect(self):

        # Manage fill values
        if not isinstance(self.fill, (tuple, list, pygame.Surface, pygame.Color, pgmenu.animation.AnimateType)):
            raise TypeError("Fill type should be either tuple/list, pygame.Surface or AnimateType object.")

        # Manage inside fill values
        if not isinstance(self.fill, (tuple, list, pygame.Surface, pygame.Color, pgmenu.animation.AnimateType)) and self.inner_fill is not None:
            raise TypeError("Inner Fill type should be either tuple/list, pygame.Surface or AnimateType object.")

        # Manage transparency / alpha value
        if isinstance(self.fill, tuple) or isinstance(self.fill, list) or isinstance(self.fill, pygame.Color):
            if len(self.fill) == 4:
                self.transparency = self.fill[3]
                self.fill = tuple(list(self.fill)[0:3])

        # Manage inner_transparency
        if isinstance(self.inner_fill, tuple) or isinstance(self.inner_fill, list) or isinstance(self.inner_fill, pygame.Color):
            if len(self.inner_fill) == 4:
                self.inner_transparency = self.inner_fill[3]
                self.inner_fill = tuple(list(self.inner_fill)[0:3])

        # Resize fill surface
        if isinstance(self.fill, pygame.Surface):
            self.fill = pygame.transform.smoothscale(self.fill, (self.rect[2], self.rect[3]))

        # Resize inner_fill surface
        if isinstance(self.inner_fill, pygame.Surface):
            self.inner_fill = pygame.transform.smoothscale(self.inner_fill, (self.rect[2], self.rect[3]))

        # Limit width
        self.width = round(min(self.width, (min(self.rect[2], self.rect[3]) / 2)))

        # Limit radius
        self.border_radius = math.floor(min(self.border_radius, (min(self.rect[2], self.rect[3]) / 2)))
        self.border_top_left_radius = math.floor(min(self.border_top_left_radius, (min(self.rect[2], self.rect[3]) / 2)))
        self.border_top_right_radius = math.floor(min(self.border_top_right_radius, (min(self.rect[2], self.rect[3]) / 2)))
        self.border_bottom_left_radius = math.floor(min(self.border_bottom_left_radius, (min(self.rect[2], self.rect[3]) / 2)))
        self.border_bottom_right_radius = math.floor(min(self.border_bottom_right_radius, (min(self.rect[2], self.rect[3]) / 2)))

        # Limit antialiasing width to border_radius, starts overlapping otherwise
        # A check like this might require checking with every border_radius
        # self.aa_strength = min(self.aa_strength, self.border_radius)
        # self.inner_aa_strength = min(self.inner_aa_strength, self.inner_border_radius)

        # Reformat border_radius list
        self.border_radius_values = {'draw_border_top_left_radius': self.temp_border_top_left_radius,
                                     'draw_border_top_right_radius': self.temp_border_top_right_radius,
                                     'draw_border_bottom_left_radius': self.temp_border_bottom_left_radius,
                                     'draw_border_bottom_right_radius': self.temp_border_bottom_right_radius}

        # Set antialiasing bool
        # A check like this might require checking with every border_radius
        # if self.border_radius <= 0: # and self.border_top_left_radius <= 0 and self.border_bottom_right_radius <= 0 :
        #     self.antialiasing = False

        self.object_cache_id = (str(self.fill), (self.rect[2], self.rect[3]), self.width, self.border_radius, self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius,
                                self.antialiasing, self.transparency, self.aa_strength, str(self.inner_fill), self.inner_antialiasing, self.inner_transparency, self.inner_aa_strength, self.force_only_overlay)

    def create_rect(self):
        aa_pixel_width = self.aa_strength if self.antialiasing else 0

        rect_surfaces = self.draw_rects()

        # Remove inner rounded rectangle if width
        if self.width and not self.force_only_overlay:
            rect_surfaces['rect_surface'].blit(rect_surfaces['remove_inner_rect_surface'], (self.width + aa_pixel_width, self.width + aa_pixel_width), special_flags=pygame.BLEND_RGBA_SUB)

        # no subtracting when an inner fill is given
        if self.width and self.inner_fill:
            rect_surfaces['rect_surface'].blit(rect_surfaces['overlay_rect_surface'], (self.width + aa_pixel_width, self.width + aa_pixel_width))

        pgmenu.cache.lru_set(cache["aarect"], self.object_cache_id, rect_surfaces['rect_surface'])

    # FIXME -> Replace temp variables with a dataclass
    def draw_rects(self):
        rect_surfaces = dict()

        aa_pixel_width = self.aa_strength if self.antialiasing else 0

        # Outer rectangle
        self.temp_fill = self.fill
        self.temp_rect = self.rect
        self.temp_border_radius = self.border_radius
        self.temp_border_top_left_radius = self.border_top_left_radius
        self.temp_border_top_right_radius = self.border_top_right_radius
        self.temp_border_bottom_left_radius = self.border_bottom_left_radius
        self.temp_border_bottom_right_radius = self.border_bottom_right_radius
        self.temp_transparency = self.transparency
        self.temp_antialiasing = self.antialiasing
        self.temp_aa_strength = self.aa_strength
        self.temp_inner_borders = False
        self.temp_inner_aa = False

        self.border_radius_values = {'draw_border_top_left_radius': self.temp_border_top_left_radius, 'draw_border_top_right_radius': self.temp_border_top_right_radius,
                                     'draw_border_bottom_left_radius': self.temp_border_bottom_left_radius, 'draw_border_bottom_right_radius': self.temp_border_bottom_right_radius}

        rect_surface = self.draw_rect()
        # To unpack later and avoid problem with a non-uniform return of rects
        rect_surfaces['rect_surface'] = rect_surface

        # To remove inner rectangle
        if self.width and not self.force_only_overlay:
            self.temp_fill = self.fill
            self.temp_rect = (self.rect[0], self.rect[1], self.rect[2] - self.width * 2 - aa_pixel_width * 2, self.rect[3] - self.width * 2 - aa_pixel_width * 2)
            self.temp_border_radius = max(self.border_radius - self.width - aa_pixel_width, 0)
            self.temp_border_top_left_radius = max(self.border_top_left_radius - self.width - aa_pixel_width, 0)
            self.temp_border_top_right_radius = max(self.border_top_right_radius - self.width - aa_pixel_width, 0)
            self.temp_border_bottom_left_radius = max(self.border_bottom_left_radius - self.width - aa_pixel_width, 0)
            self.temp_border_bottom_right_radius = max(self.border_bottom_right_radius - self.width - aa_pixel_width, 0)
            self.temp_transparency = self.transparency
            self.temp_antialiasing = self.inner_antialiasing if self.inner_antialiasing else self.antialiasing
            self.temp_aa_strength = self.inner_aa_strength
            self.temp_inner_borders = True
            self.temp_inner_aa = True

            self.border_radius_values = {'draw_border_top_left_radius': self.temp_border_top_left_radius, 'draw_border_top_right_radius': self.temp_border_top_right_radius, 'draw_border_bottom_left_radius': self.temp_border_bottom_left_radius,
                                         'draw_border_bottom_right_radius': self.temp_border_bottom_right_radius}

            remove_inner_rect_surface = self.draw_rect()
            # To unpack later and avoid problem with a non-uniform return of rects
            rect_surfaces['remove_inner_rect_surface'] = remove_inner_rect_surface

        # Inner rectangle overlay if there is one
        if self.width and self.inner_fill:
            self.temp_fill = self.inner_fill
            self.temp_rect = (self.rect[0], self.rect[1], self.rect[2] - self.width * 2 - aa_pixel_width * 2, self.rect[3] - self.width * 2 - aa_pixel_width * 2)
            self.temp_border_radius = max(self.border_radius - self.width - aa_pixel_width, 0)
            self.temp_border_top_left_radius = max(self.border_top_left_radius - self.width - aa_pixel_width, 0)
            self.temp_border_top_right_radius = max(self.border_top_right_radius - self.width - aa_pixel_width, 0)
            self.temp_border_bottom_left_radius = max(self.border_bottom_left_radius - self.width - aa_pixel_width, 0)
            self.temp_border_bottom_right_radius = max(self.border_bottom_right_radius - self.width - aa_pixel_width, 0)
            self.temp_transparency = self.inner_transparency
            self.temp_antialiasing = self.inner_antialiasing if self.force_only_overlay else False # Not too sure why -> Looks better with transparency?
            self.temp_aa_strength = self.inner_aa_strength
            self.temp_inner_borders = True
            self.temp_inner_aa = False

            self.border_radius_values = {'draw_border_top_left_radius': self.temp_border_top_left_radius, 'draw_border_top_right_radius': self.temp_border_top_right_radius, 'draw_border_bottom_left_radius': self.temp_border_bottom_left_radius,
                                         'draw_border_bottom_right_radius': self.temp_border_bottom_right_radius}

            overlay_rect_surface = self.draw_rect()
            # To unpack later and avoid problem with a non-uniform return of rects
            rect_surfaces['overlay_rect_surface'] = overlay_rect_surface

        return rect_surfaces

    def draw_rect(self):
        aa_pixel_width = self.temp_aa_strength if self.temp_antialiasing else 0

        # Exit if one of the rect values is 0 or less
        if self.temp_rect[2] < 1 or self.temp_rect[3] < 1:
            draw_rect_surface = pygame.Surface((0, 0))
            return draw_rect_surface

        # Reset/Create surface containing antialiasing
        self.aa_surface = pygame.Surface((self.temp_rect[2], self.temp_rect[3]), pygame.SRCALPHA)

        # Create rect surface
        draw_rect_surface = pygame.Surface((self.temp_rect[2], self.temp_rect[3]), pygame.SRCALPHA)

        if isinstance(self.temp_fill, pygame.Surface):
            draw_rect_surface.blit(self.temp_fill, (0, 0))
        else:
            draw_rect_surface.fill(self.temp_fill)

        # Set transparency
        draw_rect_surface.set_alpha(self.temp_transparency)

        # Calls every corner in an efficient manner
        # aa_corners() called in func
        self.get_corners()

        # Get aa sides
        self.aa_sides()

        draw_rect_surface.blit(self.aa_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        return draw_rect_surface

    def get_corners(self):
        aa_pixel_width = self.aa_strength if self.antialiasing else 0
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

            if border_radius >= 0:
                self.aa_corners(border_radius)

            # Delete done corners from corners to do
            for dict_key in dict_values_to_remove:
                del border_radius_values[dict_key]
            dict_values_to_remove = []

    # Returns pixels outside the circle / given radius
    # Calculates 1 corner and then mirrors it to return 4
    def aa_corners(self, border_radius):
        aa_pixel_width = self.temp_aa_strength if self.temp_antialiasing else 0

        cache_id = (border_radius, aa_pixel_width, self.temp_antialiasing, self.temp_inner_aa)

        if pgmenu.cache.lru_get(cache["aarect_corner"], cache_id) is None:

            aa_corner_surface = pygame.Surface((border_radius, border_radius), pygame.SRCALPHA)

            for x in range(border_radius):
                for y in range(border_radius):

                    # Formula that calculates the distance of a pixel from the center of the circle of radius border_radius
                    distance = math.sqrt((x - border_radius) ** 2 + (y - border_radius) ** 2)
                    pixel_distance = round(distance)

                    if pixel_distance >= border_radius - aa_pixel_width:
                        if self.temp_antialiasing and pixel_distance <= border_radius:
                            # Alpha formula
                            alpha = (border_radius - distance + 2) * (255 / (aa_pixel_width + 2))

                            # Limit alpha values to range 0-255
                            if alpha > 255:
                                alpha = 255

                            # Blend alpha with black to compensate for using 3 surfaces instead of 1
                            # Repeat it 2 times (2 extra surfaces)
                            alpha = utils.only_alpha_blending(alpha, 0)
                            alpha = utils.only_alpha_blending(alpha, 0)

                            alpha = round(alpha)

                            # Get current alpha's equivalent to counter blend sub
                            # Get the closest corresponding value to dict
                            alpha = utils.sub_values[alpha]

                        else:
                            alpha = 255

                        # Gets rid of left-over alpha subtraction
                        # Inverts in a way inside rect antialiasing too
                        if self.temp_inner_aa or alpha == 255:
                            color = (alpha, alpha, alpha, alpha)
                        else:
                            color = (0, 0, 0, alpha)

                        # Draw pixel to antialiasing surface
                        pygame.gfxdraw.pixel(aa_corner_surface, x, y, color)

            pgmenu.cache.lru_set(cache["aarect_corner"], cache_id, aa_corner_surface)

        aa_corner_surface = pgmenu.cache.lru_get(cache["aarect_corner"], cache_id)

        # Blit corners to correct size corners
        if self.draw_border_top_left_radius:
            self.aa_surface.blit(aa_corner_surface, (0, 0))
        if self.draw_border_top_right_radius:
            # Flip horizontally the surface to match top right corner
            top_right_aa_corners_surface = pygame.transform.flip(aa_corner_surface, True, False)
            self.aa_surface.blit(top_right_aa_corners_surface, (self.temp_rect[2] - border_radius, 0))
        if self.draw_border_bottom_left_radius:
            # Flip vertically the surface to match bottom left corner
            bottom_left_aa_corners_surface = pygame.transform.flip(aa_corner_surface, False, True)
            self.aa_surface.blit(bottom_left_aa_corners_surface, (0, self.temp_rect[3] - border_radius))
        if self.draw_border_bottom_right_radius:
            # Flip horizontally and vertically the surface to match bottom right corner
            bottom_right_aa_corners_surface = pygame.transform.flip(aa_corner_surface, True, True)
            self.aa_surface.blit(bottom_right_aa_corners_surface, (self.temp_rect[2] - border_radius, self.temp_rect[3] - border_radius))

        return self.aa_surface

    # Calculate antialiasing for the outside sides of the rect
    def aa_sides(self):
        aa_pixel_width = self.temp_aa_strength if self.temp_antialiasing else 0

        # Looping through every antialiasing layer
        for alpha_pos in range(1, aa_pixel_width + 1):
            # Calculating alpha value
            alpha = (alpha_pos + 1) * (255 / (aa_pixel_width + 2))

            # Blend alpha with black to compensate for passing by/using 3 surfaces instead of 1
            alpha = utils.only_alpha_blending(alpha, 0)
            alpha = utils.only_alpha_blending(alpha, 0)

            alpha = round(alpha)

            # Get current alpha's equivalent to counter blend sub
            # Get the closest corresponding value to dict
            alpha = utils.sub_values[alpha]

            # Gets rid of left-over alpha subtraction
            # Inverts in a way inside rect antialiasing too
            if self.temp_inner_aa or alpha == 255:
                color = (alpha, alpha, alpha, alpha)
            else:
                color = (0, 0, 0, alpha)

            # Creating vertical line of antialiasing on the left side
            len_aa_side = self.temp_rect[3] - (self.temp_border_top_left_radius + self.temp_border_bottom_left_radius)
            if len_aa_side > 0:
                pygame.gfxdraw.line(self.aa_surface, alpha_pos - 1, self.temp_border_top_left_radius, alpha_pos - 1, self.temp_border_top_left_radius + len_aa_side, color)
            # Creating vertical line of antialiasing on the right side
            len_aa_side = self.temp_rect[3] - (self.temp_border_top_right_radius + self.temp_border_bottom_right_radius)
            if len_aa_side > 0:
                pygame.gfxdraw.line(self.aa_surface, self.temp_rect[2] - alpha_pos, self.temp_border_top_right_radius, self.temp_rect[2] - alpha_pos, self.temp_border_top_right_radius + len_aa_side, color)
            # Creating vertical line of antialiasing on the top side
            len_aa_side = self.temp_rect[2] - (self.temp_border_top_left_radius + self.temp_border_top_right_radius)
            if len_aa_side > 0:
                pygame.gfxdraw.line(self.aa_surface, self.temp_border_top_left_radius, alpha_pos - 1, self.temp_border_top_left_radius + len_aa_side, alpha_pos - 1, color)
            # Creating vertical line of antialiasing on the bottom side
            len_aa_side = self.temp_rect[2] - (self.temp_border_bottom_left_radius + self.temp_border_bottom_right_radius)
            if len_aa_side > 0:
                pygame.gfxdraw.line(self.aa_surface, self.temp_border_bottom_left_radius, self.temp_rect[3] - alpha_pos, self.temp_border_bottom_left_radius + len_aa_side, self.temp_rect[3] - alpha_pos, color)

        return self.aa_surface


def aarect(surface: pygame.Surface | None,
           fill: list | tuple | pygame.Surface | pygame.Color,
           rect: list | tuple | pygame.Rect,
           width: int = 0,
           border_radius: int = 10,
           border_top_left_radius: None = None,
           border_top_right_radius: None = None,
           border_bottom_left_radius: None = None,
           border_bottom_right_radius: None = None,
           antialiasing: bool = True,
           transparency: int = 255,
           aa_strength: int = 1,
           **kwargs):

    rect = AARect(surface, fill, rect, width, border_radius, border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius, antialiasing, transparency, aa_strength, **kwargs)
    rect_surf = rect.aarect()

    return rect_surf
