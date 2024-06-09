import math
import os
import pygame
import pgmenu
from pgmenu.vars import text_cached_surfaces
from pgmenu.widget import Widget
from pgmenu.constants import THEME


# TODO -> Finish Text widget with animations, setattr, etc.

# TODO -> Library font file should work outside of directory

# FIXME -> Text doesn't resize correctly on the y axis -> Only fit_text?
# FIXME |-> The bigger the Y size, the bigger the text


# Need Widget for default functions
class Text(Widget):

    def __init__(self,
                 surface: pygame.Surface,
                 coords: list | tuple = (20, 20),
                 text: str = "Text",
                 font: str = None,
                 color: list | tuple = (255, 255, 255),
                 size: int = 20,
                 background: list | tuple = None,
                 antialias: bool = True,
                 italic: bool = False,
                 bold: bool = False,
                 strikethrough: bool = False,
                 underline: bool = False,
                 transparency: int = 255,
                 cache: bool = True,
                 center_x: bool = False,
                 center_y: bool = False):

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
        self.transparency = transparency
        self.cache = cache
        self.center_x = center_x
        self.center_y = center_y

        # Don't use border_radius, set it to a dummy value
        super().__init__(1)

        # Add widget to widget list
        pgmenu.vars.widgets.append(self)

    def match_font(self):
        match_font(self.font, self.italic, self.bold)

    def render(self):
        render(self.text, self.font, self.color, self.size, self.background, self.antialias, self.italic, self.bold, self.strikethrough, self.underline, self.cache)

    def write(self):
        write(self.surface, self.coords, self.text, self.font, self.color, self.size, self.background, self.antialias, self.italic, self.bold, self.strikethrough, self.underline, self.transparency, self.cache, self.center_x, self.center_y)

    def draw(self):
        self.write()


def match_font(font, italic=False, bold=False):
    font_path = pygame.font.match_font(font, italic=italic, bold=bold)

    if not font_path:
        font_path = os.path.join(os.getcwd(), font)

        if not os.path.exists(font_path):
            return None

    return font_path


def render(text: str = THEME,
           font: str = THEME,
           color: list | tuple = THEME,
           size: int = THEME,
           background: list | tuple = THEME,
           antialias: bool = THEME,
           italic: bool = THEME,
           bold: bool = THEME,
           strikethrough: bool = THEME,
           underline: bool = THEME,
           transparency: int = THEME,
           cache: bool = THEME):

    text = text if text != THEME else pgmenu.Theme.text_text
    font = font if font != THEME else pgmenu.Theme.text_font
    color = color if color != THEME else pgmenu.Theme.text_color
    size = size if size != THEME else pgmenu.Theme.text_size
    background = background if background != THEME else pgmenu.Theme.text_background
    antialias = antialias if antialias != THEME else pgmenu.Theme.text_antialias
    italic = italic if italic != THEME else pgmenu.Theme.text_italic
    bold = bold if bold != THEME else pgmenu.Theme.text_bold
    strikethrough = strikethrough if strikethrough != THEME else pgmenu.Theme.text_strikethrough
    underline = underline if underline != THEME else pgmenu.Theme.text_underline
    transparency = transparency if transparency != THEME else pgmenu.Theme.text_transparency
    cache = cache if cache != THEME else pgmenu.Theme.text_cache

    # Keep same cache_id in function
    cache_id = (text, font, color, size, background, antialias, italic, bold, strikethrough, underline, transparency)

    # Load from cache if already in cache
    if cache_id in text_cached_surfaces and cache:
        return text_cached_surfaces[cache_id]

    # Format font path to default if None
    if font is None:
        font = os.path.abspath(os.path.join(os.path.dirname(__file__), "VarelaRound.ttf"))

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

    # Add transparency if need be
    if transparency <= 255:
        text_surface.set_alpha(transparency)

    # Cache text surface if cache
    if cache:
        text_cached_surfaces[cache_id] = text_surface

    # Returning copy so any modification done afterward does not modify surface in cache
    return text_surface.copy()


def write(surface,
          coords: list | tuple = THEME,
          text: str = THEME,
          font: str = THEME,
          color: list | tuple = THEME,
          size: int = THEME,
          background: list | tuple = THEME,
          antialias: bool = THEME,
          italic: bool = THEME,
          bold: bool = THEME,
          strikethrough: bool = THEME,
          underline: bool = THEME,
          transparency: int = THEME,
          cache: bool = THEME,
          center_x: bool = THEME,
          center_y: bool = THEME):

    coords = coords if coords != THEME else pgmenu.Theme.text_coords
    text = text if text != THEME else pgmenu.Theme.text_text
    font = font if font != THEME else pgmenu.Theme.text_font
    color = color if color != THEME else pgmenu.Theme.text_color
    size = size if size != THEME else pgmenu.Theme.text_size
    background = background if background != THEME else pgmenu.Theme.text_background
    antialias = antialias if antialias != THEME else pgmenu.Theme.text_antialias
    italic = italic if italic != THEME else pgmenu.Theme.text_italic
    bold = bold if bold != THEME else pgmenu.Theme.text_bold
    strikethrough = strikethrough if strikethrough != THEME else pgmenu.Theme.text_strikethrough
    underline = underline if underline != THEME else pgmenu.Theme.text_underline
    transparency = transparency if transparency != THEME else pgmenu.Theme.text_transparency
    cache = cache if cache != THEME else pgmenu.Theme.text_cache
    center_x = center_x if center_x != THEME else pgmenu.Theme.text_center_x
    center_y = center_y if center_y != THEME else pgmenu.Theme.text_center_y

    text_surface = render(text, font, color, size, background, antialias, italic, bold, strikethrough, underline, transparency, cache)

    if center_x or center_y:
        surface_size = text_surface.get_size()
        coords = pgmenu.position.center_coords(surface_size, (*coords, 0, 0), center_x, center_y)

    surface.blit(text_surface, coords)


# TODO -> Can't be called rect since it doesn't accept coords

# TODO -> Reminder: precise_fit is unfinished, might not be doable or even useful
def fit_text(text: str = THEME,
             font: str = THEME,
             color: list | tuple = THEME,
             rect: list[int, int] | tuple[int, int] = THEME,
             margin: int = THEME,
             background: list | tuple = THEME,
             antialias: bool = THEME,
             italic: bool = THEME,
             bold: bool = THEME,
             strikethrough: bool = THEME,
             underline: bool = THEME,
             transparency: int = THEME,
             cache: bool = THEME,
             precise_fit: bool = False):

    text = text if text != THEME else pgmenu.Theme.text_text
    font = font if font != THEME else pgmenu.Theme.text_font
    color = color if color != THEME else pgmenu.Theme.text_color
    rect = rect if rect != THEME else pgmenu.Theme.text_fit_rect
    margin = margin if margin != THEME else pgmenu.Theme.text_margin
    background = background if background != THEME else pgmenu.Theme.text_background
    antialias = antialias if antialias != THEME else pgmenu.Theme.text_antialias
    italic = italic if italic != THEME else pgmenu.Theme.text_italic
    bold = bold if bold != THEME else pgmenu.Theme.text_bold
    strikethrough = strikethrough if strikethrough != THEME else pgmenu.Theme.text_strikethrough
    underline = underline if underline != THEME else pgmenu.Theme.text_underline
    transparency = transparency if transparency != THEME else pgmenu.Theme.text_transparency
    cache = cache if cache != THEME else pgmenu.Theme.text_cache

    # Cache render with rect instead of size
    # Keep same cache_id in function
    cache_id = (text, font, color, rect, background, antialias, italic, bold, strikethrough, underline, transparency)

    # Load from cache if already in cache
    if cache_id in text_cached_surfaces and cache:
        return text_cached_surfaces[cache_id]

    # Format font path to default if None
    if font is None:
        font = os.path.abspath(os.path.join(os.path.dirname(__file__), "VarelaRound.ttf"))

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

    # Add text margin
    text_size -= margin

    # Render text without cache since already caching
    text_surface = render(text, font, color, text_size, background, antialias, italic, bold, strikethrough, underline, transparency, cache=False)

    # Doesn't seem doable with current syntax
    if precise_fit:
        ...

    # Cache text surface if cache
    if cache:
        text_cached_surfaces[cache_id] = text_surface

    return text_surface
