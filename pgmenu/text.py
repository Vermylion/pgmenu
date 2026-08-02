import math
import os
import pygame
import pgmenu
from pgmenu.animation import AnimateTuple
from pgmenu.vars import cache
from pgmenu.widget import Widget
from pgmenu.constants import THEME
from pgmenu.theme import resolve


def match_font(font, italic=False, bold=False):
    # Remove file extention in case since match_font only takes in names
    font_name = os.path.splitext(font)

    font_path = pygame.font.match_font(font_name, italic=italic, bold=bold)

    if not font_path:
        font_path = os.path.join(os.getcwd(), font)

        if not os.path.exists(font_path):
            return None

    return font_path


def format_font(font, italic=False, bold=False):
    # Format font path to default if None
    if font is None or font.lower() == "VarelaRound.ttf".lower():
        font = os.path.abspath(os.path.join(os.path.dirname(__file__), "VarelaRound.ttf"))

    # Check with system fonts if we still don't have a path
    sys_font_path = match_font(font, italic, bold)
    if sys_font_path is not None:
        font = sys_font_path

    return font


def render(text: str = THEME,
           color: list | tuple = THEME,
           size: int = THEME,
           font: str = THEME,
           background: list | tuple = THEME,
           antialias: bool = THEME,
           italic: bool = THEME,
           bold: bool = THEME,
           strikethrough: bool = THEME,
           underline: bool = THEME,
           transparency: int = THEME):

    text = resolve(text, pgmenu.Theme.text_text)
    color = resolve(color, pgmenu.Theme.text_color)
    size = resolve(size, pgmenu.Theme.text_size)
    font = resolve(font, pgmenu.Theme.text_font)
    background = resolve(background, pgmenu.Theme.text_background)
    antialias = resolve(antialias, pgmenu.Theme.text_antialias)
    italic = resolve(italic, pgmenu.Theme.text_italic)
    bold = resolve(bold, pgmenu.Theme.text_bold)
    strikethrough = resolve(strikethrough, pgmenu.Theme.text_strikethrough)
    underline = resolve(underline, pgmenu.Theme.text_underline)
    transparency = resolve(transparency, pgmenu.Theme.text_transparency)

    # Keep same cache_id in function
    cache_id = (text, color, size, font, background, antialias, italic, bold, strikethrough, underline, transparency)

    # Load from cache if already in cache
    cached = pgmenu.cache.lru_get(cache["text"], cache_id)
    if cached is not None:
        return cached

    font = format_font(font, italic, bold)

    text_font = pygame.font.Font(font, size)

    text_font.italic = italic
    text_font.bold = bold
    text_font.strikethrough = strikethrough
    text_font.underline = underline

    # Render each line to enable \n characters
    # Separate text in lines
    text_lines = text.split('\n')
    # Save each line surface in a list to add them together, keep real size
    text_lines_surf = []

    # Loop through lines
    for i in range(text.count('\n') + 1):
        # Render each line
        line_surf = text_font.render(text_lines[i], antialias, color, background)
        text_lines_surf.append(line_surf)

    # Create main text surface
    line_surf_max_x = max([surf.get_width() for surf in text_lines_surf])
    line_surf_sum_y = sum([surf.get_height() for surf in text_lines_surf])
    text_surface = pygame.Surface((line_surf_max_x, line_surf_sum_y), pygame.SRCALPHA)

    # Blit line surfaces together
    x, y = 0, 0
    for i in range(len(text_lines_surf)):
        if i != 0:
            y += text_lines_surf[i-1].get_height()

        text_surface.blit(text_lines_surf[i], (x, y))

    # Add transparency if need be
    if transparency <= 255:
        text_surface.set_alpha(transparency)

    # Cache text surface if cache
    pgmenu.cache.lru_set(cache["text"], cache_id, text_surface)

    # Returning copy so any modification done afterward does not modify surface in cache
    return text_surface.copy()


def write(surface,
          coords: list | tuple = THEME,
          text: str = THEME,
          color: list | tuple = THEME,
          size: int = THEME,
          font: str = THEME,
          background: list | tuple = THEME,
          antialias: bool = THEME,
          italic: bool = THEME,
          bold: bool = THEME,
          strikethrough: bool = THEME,
          underline: bool = THEME,
          transparency: int = THEME,
          center_x: bool = THEME,
          center_y: bool = THEME):

    coords = resolve(coords, pgmenu.Theme.text_coords)
    text = resolve(text, pgmenu.Theme.text_text)
    color = resolve(color, pgmenu.Theme.text_color)
    size = resolve(size, pgmenu.Theme.text_size)
    font = resolve(font, pgmenu.Theme.text_font)
    background = resolve(background, pgmenu.Theme.text_background)
    antialias = resolve(antialias, pgmenu.Theme.text_antialias)
    italic = resolve(italic, pgmenu.Theme.text_italic)
    bold = resolve(bold, pgmenu.Theme.text_bold)
    strikethrough = resolve(strikethrough, pgmenu.Theme.text_strikethrough)
    underline = resolve(underline, pgmenu.Theme.text_underline)
    transparency = resolve(transparency, pgmenu.Theme.text_transparency)
    center_x = resolve(center_x, pgmenu.Theme.text_center_x)
    center_y = resolve(center_y, pgmenu.Theme.text_center_y)

    text_surface = render(text, color, size, font, background, antialias, italic, bold, strikethrough, underline, transparency)

    if center_x or center_y:
        surface_size = text_surface.get_size()
        coords = pgmenu.position.center_coords(surface_size, (*coords, 0, 0), center_x, center_y)

    surface.blit(text_surface, coords)


# FIXME -> Can't be called rect since it doesn't accept coords -> Change name or change input to tuple[int, int, int, int]?

# TODO -> Make fit_width and fit_height counterparts


def fit_width():
    ...


def fit_height():
    ...


def fit_size(dest_rect: list[int, int] | tuple[int, int] = THEME,
             text: str = THEME,
             color: list | tuple = THEME,
             margin: int = THEME,
             font: str = THEME,
             background: list | tuple = THEME,
             antialias: bool = THEME,
             italic: bool = THEME,
             bold: bool = THEME,
             strikethrough: bool = THEME,
             underline: bool = THEME,
             transparency: int = THEME):
    """
        Returns the int size of the text that would fit into the given area
        :param dest_rect: main rect where text is going to be fit in
        :param text:
        :param color:
        :param margin:
        :param font:
        :param background:
        :param antialias:
        :param italic:
        :param bold:
        :param strikethrough:
        :param underline:
        :param transparency:
        :return: Returns the int size of the text that would fit into the given area
        """

    dest_rect = resolve(dest_rect, pgmenu.Theme.text_dest_rect)
    text = resolve(text, pgmenu.Theme.text_text)
    color = resolve(color, pgmenu.Theme.text_color)
    margin = resolve(margin, pgmenu.Theme.text_margin)
    font = resolve(font, pgmenu.Theme.text_font)
    background = resolve(background, pgmenu.Theme.text_background)
    antialias = resolve(antialias, pgmenu.Theme.text_antialias)
    italic = resolve(italic, pgmenu.Theme.text_italic)
    bold = resolve(bold, pgmenu.Theme.text_bold)
    strikethrough = resolve(strikethrough, pgmenu.Theme.text_strikethrough)
    underline = resolve(underline, pgmenu.Theme.text_underline)
    transparency = resolve(transparency, pgmenu.Theme.text_transparency)

    # Cache render with rect instead of size
    # Keep same cache_id in function
    cache_id = (text, color, dest_rect, margin, font, background, antialias, italic, bold, strikethrough, underline, transparency)

    # Load from cache if already in cache
    cached = pgmenu.cache.lru_get(cache["text"], cache_id)
    if cached is not None:
        return cached

    font = format_font(font, italic, bold)

    # Minimum size of rect for text font
    text_size = min(dest_rect)

    text_font = pygame.font.Font(font, text_size)

    # Catch when the text is too big/doesn't fit
    size_x = text_font.size(text)[0]
    if size_x > dest_rect[0]:
        # math.floor to make sure it doesn't go out of bounds
        text_size = math.floor(text_size * dest_rect[0] / size_x)
        # Create new text font for min size check afterward
        text_font = pygame.font.Font(font, text_size)

    size_y = text_font.size(text)[1]
    if size_y > dest_rect[1]:
        # math.floor to make sure it doesn't go out of bounds
        text_size = math.floor(text_size * dest_rect[1] / size_y)

    # Add text margin
    text_size -= margin

    # Cached text size
    pgmenu.cache.lru_set(cache["text"], cache_id, text_size)

    return text_size


def fit_width_render():
    ...


def fit_height_render():
    ...


def fit_render(dest_rect: list[int, int] | tuple[int, int] = THEME,
               text: str = THEME,
               color: list | tuple = THEME,
               margin: int = THEME,
               font: str = THEME,
               background: list | tuple = THEME,
               antialias: bool = THEME,
               italic: bool = THEME,
               bold: bool = THEME,
               strikethrough: bool = THEME,
               underline: bool = THEME,
               transparency: int = THEME):
    """
    Returns a surface of the rendered text
    :param dest_rect: main rect where text is going to be fit in
    :param text:
    :param color:
    :param margin:
    :param font:
    :param background:
    :param antialias:
    :param italic:
    :param bold:
    :param strikethrough:
    :param underline:
    :param transparency:
    :return: Returns a surface of the rendered text
    """

    dest_rect = resolve(dest_rect, pgmenu.Theme.text_dest_rect)
    text = resolve(text, pgmenu.Theme.text_text)
    color = resolve(color, pgmenu.Theme.text_color)
    margin = resolve(margin, pgmenu.Theme.text_margin)
    font = resolve(font, pgmenu.Theme.text_font)
    background = resolve(background, pgmenu.Theme.text_background)
    antialias = resolve(antialias, pgmenu.Theme.text_antialias)
    italic = resolve(italic, pgmenu.Theme.text_italic)
    bold = resolve(bold, pgmenu.Theme.text_bold)
    strikethrough = resolve(strikethrough, pgmenu.Theme.text_strikethrough)
    underline = resolve(underline, pgmenu.Theme.text_underline)
    transparency = resolve(transparency, pgmenu.Theme.text_transparency)

    text_size = fit_size(dest_rect, text, color, margin, font, background, antialias, italic, bold, strikethrough, underline, transparency)

    # Render text; caching is done in render
    text_surface = render(text, color, text_size, font, background, antialias, italic, bold, strikethrough, underline, transparency)

    return text_surface.copy()


def fit_width_render_animated():
    ...


def fit_height_render_animated():
    ...


def fit_render_animated(dest_rect: AnimateTuple[int, int] = THEME,
                        text: str = THEME,
                        color: list | tuple = THEME,
                        margin: int = THEME,
                        font: str = THEME,
                        background: list | tuple = THEME,
                        antialias: bool = THEME,
                        italic: bool = THEME,
                        bold: bool = THEME,
                        strikethrough: bool = THEME,
                        underline: bool = THEME,
                        transparency: int = THEME) -> tuple[pygame.Surface, tuple[int, int, int, int]]:
    """
    Fits rendered text to a destination area which is animated, fitting text with per-pixel precision using smoothscale instead of per font size as is with regular fit-render.
    Returns a surface of the fitted text (by smoothscale) and a text_rect[int, int, int, int].
    :param dest_rect: main rect where text is going to be fit in
    :param text:
    :param color:
    :param margin:
    :param font:
    :param background:
    :param antialias:
    :param italic:
    :param bold:
    :param strikethrough:
    :param underline:
    :param transparency:
    :return: Returns a surface of the fitted text (by smoothscale) and a text_rect[int, int, int, int]
    """

    dest_rect = resolve(dest_rect, pgmenu.Theme.text_dest_rect)
    text = resolve(text, pgmenu.Theme.text_text)
    color = resolve(color, pgmenu.Theme.text_color)
    margin = resolve(margin, pgmenu.Theme.text_margin)
    font = resolve(font, pgmenu.Theme.text_font)
    background = resolve(background, pgmenu.Theme.text_background)
    antialias = resolve(antialias, pgmenu.Theme.text_antialias)
    italic = resolve(italic, pgmenu.Theme.text_italic)
    bold = resolve(bold, pgmenu.Theme.text_bold)
    strikethrough = resolve(strikethrough, pgmenu.Theme.text_strikethrough)
    underline = resolve(underline, pgmenu.Theme.text_underline)
    transparency = resolve(transparency, pgmenu.Theme.text_transparency)

    # Get rendered text fitted to max button size
    final_dest_rect = (round(dest_rect.final_tuple[0]), round(dest_rect.final_tuple[1]))
    text_surface = pgmenu.text.fit_render(final_dest_rect, text, color, round(margin), font, background,  # In case margin is animated, it has to be passed as a whole number into fit_text
                                          antialias, italic, bold, strikethrough, underline, transparency)

    # Text rect is found to smoothscale text surface to correct dimensions
    text_rect = pgmenu.rect.fit_rects(dest_rect.int_tuple, text_surface.get_size(), margin=margin)

    # Fit text surface to current text rect for smooth scaling
    text_surface = pygame.transform.smoothscale(text_surface, text_rect[2:])

    # FIXME -> Slight jitteriness is caused by dynamic dest_rect used to center coords
    text_pos = pgmenu.position.center_coords(text_surface.get_size(), (0, 0, *dest_rect))
    text_rect = (*text_pos, text_rect[2:])

    return text_surface, text_rect