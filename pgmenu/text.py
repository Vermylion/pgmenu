import math
import os
import pygame
import pgmenu
from pgmenu.animation import *
from pgmenu.vars import cache
from pgmenu.widget import Widget
from pgmenu.constants import THEME
from pgmenu.theme import resolve


def match_font(font, italic=False, bold=False):
    # Remove file extention in case since match_font only takes in names
    font_name = os.path.splitext(font)[0]

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

    if '\n' not in text:
        text_surface = text_font.render(text, antialias, color, background)
    else:
        text_lines_surf = [
            text_font.render(line, antialias, color, background)
            for line in text.split('\n')
        ]

        width = max(surf.get_width() for surf in text_lines_surf)
        height = sum(surf.get_height() for surf in text_lines_surf)

        text_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        y = 0
        for line_surf in text_lines_surf:
            text_surface.blit(line_surf, (0, y))
            y += line_surf.get_height()

    if transparency <= 255:
        text_surface.set_alpha(transparency)

    pgmenu.cache.lru_set(cache["text"], cache_id, text_surface)

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


def fit_width(dest_width: int = THEME,
              text: str = THEME,
              margin: int = THEME,
              font: str = THEME,
              italic: bool = THEME,
              bold: bool = THEME):
    """
    Returns the int size of the text that would fit into the given width, ignoring height
    :param dest_width: width of the area the text is going to be fit into
    :param text:
    :param margin:
    :param font:
    :param italic:
    :param bold:
    :return: Returns the int size of the text that would fit into the given width
    """

    dest_width = resolve(dest_width, pgmenu.Theme.text_dest_width)
    text = resolve(text, pgmenu.Theme.text_text)
    margin = resolve(margin, pgmenu.Theme.text_margin)
    font = resolve(font, pgmenu.Theme.text_font)
    italic = resolve(italic, pgmenu.Theme.text_italic)
    bold = resolve(bold, pgmenu.Theme.text_bold)

    # Cache render with width instead of size
    # Keep same cache_id in function
    cache_id = (text, dest_width, margin, font, italic, bold)

    # Load from cache if already in cache
    cached = pgmenu.cache.lru_get(cache["text"], cache_id)
    if cached is not None:
        return cached

    font = format_font(font, italic, bold)

    # Starting guess for text size, using dest_width as it's the only dimension we care about
    text_size = dest_width

    text_surf = pgmenu.text.render(text, size=text_size, font=font, italic=italic, bold=bold)

    # Catch when the text is too big/doesn't fit
    size_x = text_surf.get_size()[0]
    if size_x > dest_width:
        # math.floor to make sure it doesn't go out of bounds
        text_size = math.floor(text_size * dest_width / size_x)

    # Add text margin
    text_size -= margin

    # Cached text size
    pgmenu.cache.lru_set(cache["text"], cache_id, text_size)

    return text_size


def fit_height(dest_height: int = THEME,
              text: str = THEME,
              margin: int = THEME,
              font: str = THEME,
              italic: bool = THEME,
              bold: bool = THEME):
    """
    Returns the int size of the text that would fit into the given height, ignoring width
    :param dest_height: height of the area the text is going to be fit into
    :param text:
    :param margin:
    :param font:
    :param italic:
    :param bold:
    :return: Returns the int size of the text that would fit into the given height
    """

    dest_height = resolve(dest_height, pgmenu.Theme.text_dest_height)
    text = resolve(text, pgmenu.Theme.text_text)
    margin = resolve(margin, pgmenu.Theme.text_margin)
    font = resolve(font, pgmenu.Theme.text_font)
    italic = resolve(italic, pgmenu.Theme.text_italic)
    bold = resolve(bold, pgmenu.Theme.text_bold)

    # Cache render with height instead of size
    # Keep same cache_id in function
    cache_id = (text, dest_height, margin, font, italic, bold)

    # Load from cache if already in cache
    cached = pgmenu.cache.lru_get(cache["text"], cache_id)
    if cached is not None:
        return cached

    font = format_font(font, italic, bold)

    # Starting guess for text size, using dest_height as it's the only dimension we care about
    text_size = dest_height

    text_surf = pgmenu.text.render(text, size=text_size, font=font, italic=italic, bold=bold)

    # Catch when the text is too big/doesn't fit
    size_y = text_surf.get_size()[1]
    if size_y > dest_height:
        # math.floor to make sure it doesn't go out of bounds
        text_size = math.floor(text_size * dest_height / size_y)

    # Add text margin
    text_size -= margin

    # Cached text size
    pgmenu.cache.lru_set(cache["text"], cache_id, text_size)

    return text_size


def fit_size(dest_rect: list[int, int] | tuple[int, int] = THEME,
             text: str = THEME,
             margin: int = THEME,
             font: str = THEME,
             italic: bool = THEME,
             bold: bool = THEME):
    """
        Returns the int size of the text that would fit into the given area
        :param dest_rect: main rect where text is going to be fit in
        :param text:
        :param margin:
        :param font:
        :param italic:
        :param bold:
        :return: Returns the int size of the text that would fit into the given area
        """

    dest_rect = resolve(dest_rect, pgmenu.Theme.text_dest_rect)
    text = resolve(text, pgmenu.Theme.text_text)
    margin = resolve(margin, pgmenu.Theme.text_margin)
    font = resolve(font, pgmenu.Theme.text_font)
    italic = resolve(italic, pgmenu.Theme.text_italic)
    bold = resolve(bold, pgmenu.Theme.text_bold)

    # Cache render with rect instead of size
    # Keep same cache_id in function
    cache_id = (text, dest_rect, margin, font, italic, bold)

    # Load from cache if already in cache
    cached = pgmenu.cache.lru_get(cache["text"], cache_id)
    if cached is not None:
        return cached

    font = format_font(font, italic, bold)

    # Minimum size of rect for text surface
    text_size = min(dest_rect)

    text_surf = pgmenu.text.render(text, size=text_size, font=font, italic=italic, bold=bold)

    # Catch when the text is too big/doesn't fit
    size_x = text_surf.get_size()[0]
    if size_x > dest_rect[0]:
        # math.floor to make sure it doesn't go out of bounds
        text_size = math.floor(text_size * dest_rect[0] / size_x)
        # Create new text surface for min size check afterward
        text_surf = pgmenu.text.render(text, size=text_size, font=font, italic=italic, bold=bold)

    size_y = text_surf.get_size()[1]
    if size_y > dest_rect[1]:
        # math.floor to make sure it doesn't go out of bounds
        text_size = math.floor(text_size * dest_rect[1] / size_y)

    # Add text margin
    text_size -= margin

    # Cached text size
    pgmenu.cache.lru_set(cache["text"], cache_id, text_size)

    return text_size


def fit_width_render(dest_width: int = THEME,
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
    Returns a surface of the rendered text fitted to the given width, ignoring height
    :param dest_width: width of the area the text is going to be fit into
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

    dest_width = resolve(dest_width, pgmenu.Theme.text_dest_width)
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

    text_size = fit_width(dest_width, text, margin, font, italic, bold)

    # Render text; caching is done in render
    text_surface = render(text, color, text_size, font, background, antialias, italic, bold, strikethrough, underline, transparency)

    return text_surface.copy()


def fit_height_render(dest_height: int = THEME,
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
    Returns a surface of the rendered text fitted to the given height, ignoring width
    :param dest_height: height of the area the text is going to be fit into
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

    dest_height = resolve(dest_height, pgmenu.Theme.text_dest_height)
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

    text_size = fit_height(dest_height, text, margin, font, italic, bold)

    # Render text; caching is done in render
    text_surface = render(text, color, text_size, font, background, antialias, italic, bold, strikethrough, underline, transparency)

    return text_surface.copy()


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

    text_size = fit_size(dest_rect, text, margin, font, italic, bold)

    # Render text; caching is done in render
    text_surface = render(text, color, text_size, font, background, antialias, italic, bold, strikethrough, underline, transparency)

    return text_surface.copy()


# TODO -> Check that this function has correct functionality; written by Claude
def fit_width_render_smoothscale(dest_width: int = THEME,
                                 max_dest_width: int = THEME,
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
    Fits rendered text to a destination width which can be animated, fitting text with per-pixel precision using
    smoothscale instead of per font size as is with regular fit_width_render. Height is scaled proportionally.
    Returns a surface of the fitted text (by smoothscale) and a text_rect[int, int, int, int].
    :param dest_width: width the text is going to be fit into
    :param max_dest_width: Sets maximum width for rendered text, for cleaner scaling since it does only down scaling
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

    dest_width = resolve(dest_width, pgmenu.Theme.text_dest_width)
    max_dest_width = resolve(max_dest_width, pgmenu.Theme.text_max_dest_width, dest_width)
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

    if max_dest_width is None:
        max_dest_width = dest_width

    # Get rendered text fitted to max width
    # In case margin is animated, it has to be passed as a whole number into fit_width_render
    text_surface = pgmenu.text.fit_width_render(max_dest_width, text, color, round(margin), font, background,
                                                 antialias, italic, bold, strikethrough, underline, transparency)

    # Target width for the smoothscale step, matching fit_render_smoothscale's margin handling
    target_width = max(1, round(dest_width - margin))

    orig_width, orig_height = text_surface.get_size()

    # Scale height proportionally to keep the text from stretching/squashing
    scale = target_width / orig_width if orig_width else 1
    new_size = (target_width, max(1, round(orig_height * scale)))

    # Fit text surface to current width for smooth scaling with cache
    text_surface = pgmenu.surface.cached_smoothscale(text_surface, new_size)

    # FIXME -> Slight jitteriness is caused by dynamic dest_width used to center coords
    text_pos = pgmenu.position.center_coords(text_surface.get_size(), (0, 0, dest_width, new_size[1]))
    text_rect = (*text_pos, *new_size)

    return text_surface, text_rect


# TODO -> Check that this function has correct functionality; written by Claude
def fit_height_render_smoothscale(dest_height: int = THEME,
                                  max_dest_height: int = THEME,
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
    Fits rendered text to a destination height which can be animated, fitting text with per-pixel precision using
    smoothscale instead of per font size as is with regular fit_height_render. Width is scaled proportionally.
    Returns a surface of the fitted text (by smoothscale) and a text_rect[int, int, int, int].
    :param dest_height: height the text is going to be fit into
    :param max_dest_height: Sets maximum height for rendered text, for cleaner scaling since it does only down scaling
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

    dest_height = resolve(dest_height, pgmenu.Theme.text_dest_height)
    max_dest_height = resolve(max_dest_height, pgmenu.Theme.text_max_dest_height, dest_height)
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

    if max_dest_height is None:
        max_dest_height = dest_height

    # Get rendered text fitted to max height
    # In case margin is animated, it has to be passed as a whole number into fit_height_render
    text_surface = pgmenu.text.fit_height_render(max_dest_height, text, color, round(margin), font, background,
                                                  antialias, italic, bold, strikethrough, underline, transparency)

    # Target height for the smoothscale step, matching fit_render_smoothscale's margin handling
    target_height = max(1, round(dest_height - margin))

    orig_width, orig_height = text_surface.get_size()

    # Scale width proportionally to keep the text from stretching/squashing
    scale = target_height / orig_height if orig_height else 1
    new_size = (max(1, round(orig_width * scale)), target_height)

    # Fit text surface to current height for smooth scaling with cache
    text_surface = pgmenu.surface.cached_smoothscale(text_surface, new_size)

    # FIXME -> Slight jitteriness is caused by dynamic dest_height used to center coords
    text_pos = pgmenu.position.center_coords(text_surface.get_size(), (0, 0, new_size[0], dest_height))
    text_rect = (*text_pos, *new_size)

    return text_surface, text_rect


def fit_render_smoothscale(dest_rect: tuple[int, int] = THEME,
                           max_dest_rect: tuple[int, int] | None = THEME,
                           text: str = THEME,
                           color: tuple = THEME,
                           margin: int = THEME,
                           font: str = THEME,
                           background: tuple = THEME,
                           antialias: bool = THEME,
                           italic: bool = THEME,
                           bold: bool = THEME,
                           strikethrough: bool = THEME,
                           underline: bool = THEME,
                           transparency: int = THEME) -> tuple[pygame.Surface, tuple[int, int, int, int]]:
    """
    Fits rendered text to a destination area which can be animated, fitting text with per-pixel precision using smoothscale instead of per font size as is with regular fit_render.
    Returns a surface of the fitted text (by smoothscale) and a text_rect[int, int, int, int].
    :param dest_rect: main rect where text is going to be fit in
    :param max_dest_rect: Sets maximum size for rendered text, for cleaner scaling since it does only down scaling
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
    max_dest_rect = resolve(max_dest_rect, pgmenu.Theme.text_max_dest_rect, dest_rect)
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

    if max_dest_rect is None:
        max_dest_rect = dest_rect

    # Get rendered text fitted to max button size
    # In case margin is animated, it has to be passed as a whole number into fit_text
    text_surface = pgmenu.text.fit_render(max_dest_rect, text, color, round(margin), font, background,
                                          antialias, italic, bold, strikethrough, underline, transparency)

    # Text rect is found to smoothscale text surface to correct dimensions
    text_rect = pgmenu.rect.fit_rects(dest_rect, text_surface.get_size(), margin=margin)

    # Fit text surface to current text rect for smooth scaling with cache
    text_surface = pgmenu.surface.cached_smoothscale(text_surface, text_rect[2:])

    # FIXME -> Slight jitteriness is caused by dynamic dest_rect used to center coords
    text_pos = pgmenu.position.center_coords(text_surface.get_size(), (0, 0, *dest_rect))
    text_rect = (*text_pos, *text_rect[2:])

    return text_surface, text_rect