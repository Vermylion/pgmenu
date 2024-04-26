import math
import os
import pygame
from pgmenu.widget import Widget
from pgmenu.vars import text_cached_surfaces


# TODO -> Keep cache argument? Is it useful?


class Text(Widget):

    def __init__(self,
                 surface: pygame.Surface,
                 coords: list | tuple,
                 text: str,
                 font: str,
                 color: list | tuple,
                 size: int,
                 background: list | tuple = None,
                 antialias: bool = True,
                 italic: bool = False,
                 bold: bool = False,
                 strikethrough: bool = False,
                 underline: bool = False,
                 cache: bool = True):
        super().__init__()

        self.surface = surface
        self.coords = coords
        self.text = text
        self.font = font
        self.color = color
        self.background = background
        self.size = size
        self.antialias = antialias
        self.italic = italic
        self.bold = bold
        self.strikethrough = strikethrough
        self.underline = underline
        self.cache = cache

    def match_font(self):
        match_font(self.font, self.italic, self.bold)

    def render(self):
        render(self.text, self.font, self.color, self.size, self.background, self.antialias, self.italic, self.bold, self.strikethrough, self.underline, self.cache)

    def write(self):
        write(self.surface, self.coords, self.text, self.font, self.color, self.size, self.background, self.antialias, self.italic, self.bold, self.strikethrough, self.underline, self.cache)


def match_font(font, italic=False, bold=False):
    font_path = pygame.font.match_font(font, italic=italic, bold=bold)

    if not font_path:
        font_path = os.path.join(os.getcwd(), font)

        if not os.path.exists(font_path):
            return None

    return font_path


def render(text: str,
           font: str,
           color: list | tuple,
           size: int,
           background: list | tuple = None,
           antialias: bool = True,
           italic: bool = False,
           bold: bool = False,
           strikethrough: bool = False,
           underline: bool = False,
           cache: bool = True):
    # Keep same cache_id in function
    cache_id = (text, font, color, size, background, antialias, italic, bold, strikethrough, underline)

    # Load from cache if already in cache
    if cache_id in text_cached_surfaces and cache:
        return text_cached_surfaces[cache_id]

    font = match_font(font, italic, bold)
    # Raise error if font cannot be found -> match_font() output is None
    if not font: raise FileNotFoundError('Cannot find font file')
    text_font = pygame.font.Font(font, size)

    text_font.italic = italic
    text_font.bold = bold
    text_font.strikethrough = strikethrough
    text_font.underline = underline

    # Render each line to enable \n characters
    # Separate text in lines
    text_lines = text.split('\n')
    text_lines_by_len = {len(line): line for line in text_lines}
    max_line_size = text_font.size(text_lines_by_len[max(list(text_lines_by_len.keys()))])

    # Final surf to blit to
    text_surface = pygame.Surface((max_line_size[0], max_line_size[1] * (len(text_lines))), pygame.SRCALPHA)
    # Loop through lines
    for i in range(text.count('\n') + 1):
        # Render each line
        line_surf = text_font.render(text_lines[i], antialias, color, background)
        text_surface.blit(line_surf, (0, max_line_size[1] * i))

    # Cache text surface if cache
    if cache:
        text_cached_surfaces[cache_id] = text_surface

    # Returning copy so any modification done afterward does not modify surface in cache
    return text_surface.copy()


def write(surface,
          coords,
          text: str,
          font: str,
          color: list | tuple,
          size: int,
          background: list | tuple = None,
          antialias: bool = True,
          italic: bool = False,
          bold: bool = False,
          strikethrough: bool = False,
          underline: bool = False,
          cache: bool = True):
    text_surface = render(text, font, color, size, background, antialias, italic, bold, strikethrough, underline, cache)

    surface.blit(text_surface, coords)


# TODO -> Can't be called rect since it doesn't accept coords

# TODO -> Reminder: precise_fit is unfinished, might not be doable or even useful
def fit_text(text: str,
             font: str,
             color: list | tuple,
             rect: list[int, int] | tuple[int, int],
             margin: int = 0,
             background: list | tuple = None,
             antialias: bool = True,
             italic: bool = False,
             bold: bool = False,
             strikethrough: bool = False,
             underline: bool = False,
             cache: bool = True,
             precise_fit: bool = False):
    # Cache render with rect instead of size
    # Keep same cache_id in function
    cache_id = (text, font, color, rect, background, antialias, italic, bold, strikethrough, underline)

    # Load from cache if already in cache
    if cache_id in text_cached_surfaces and cache:
        return text_cached_surfaces[cache_id]

    font = match_font(font, italic, bold)
    # Raise error if font cannot be found -> match_font() output is None
    if not font: raise FileNotFoundError('Cannot find font file')

    # Minimum size of rect for text font
    text_size = min(rect)
    text_font = pygame.font.Font(font, text_size)

    # Catch when the text is too big/doesn't fit
    max_size = max(text_font.size(text))
    if max_size > max(rect):
        # math.floor to make sure it doesn't go out of bounds
        text_size = math.floor(text_size * max(rect) / max_size)
        # Create new text font for min size check afterward
        text_font = pygame.font.Font(font, text_size)

    min_size = min(text_font.size(text))
    if min_size > min(rect):
        # math.floor to make sure it doesn't go out of bounds
        text_size = math.floor(text_size * min(rect) / min_size)

    test_font = pygame.font.Font(font, text_size)
    print(rect, test_font.size(text), text_size, test_font.get_ascent(), test_font.get_descent(), test_font.get_height())

    # Add text margin
    text_size -= margin

    # Render text without cache since already caching
    text_surface = render(text, font, color, text_size, background, antialias, italic, bold, strikethrough, underline, cache=False)

    # Doesn't seem doable with current syntax
    if precise_fit:
        ...

    # Cache text surface if cache
    if cache:
        text_cached_surfaces[cache_id] = text_surface

    return text_surface
