import os
import pygame
from widget import Widget


class Text(Widget):

    def __init__(self,
                 surface,
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
                 underline: bool = False):

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

    def match_font(self):
        match_font(self.font, self.italic, self.bold)

    def render(self):
        render(self.text, self.font, self.color, self.size, self.background, self.antialias, self.italic, self.bold, self.strikethrough, self.underline)

    def write(self):
        write(self.surface, self.coords, self.text, self.font, self.color, self.size, self.background, self.antialias, self.italic, self.bold, self.strikethrough, self.underline)


def match_font(font, italic = False, bold = False):
    font_path = pygame.font.match_font(font, italic = italic, bold = bold)

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
           underline: bool = False):

    font = match_font(font, italic, bold)
    # Raise error if font cannot be found -> match_font() output is None
    if not font: raise 'Cannot find font file'

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
    text_surf = pygame.Surface((max_line_size[0], max_line_size[1] * (len(text_lines))), pygame.SRCALPHA)
    # Loop through lines
    for i in range(text.count('\n') + 1):
        # Render each line
        line_surf = text_font.render(text_lines[i], antialias, color, background)
        text_surf.blit(line_surf, (0, max_line_size[1] * i))

    return text_surf


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
          underline: bool = False):

    text_surf = render(text, font, color, size, background, antialias, italic, bold, strikethrough, underline)

    surface.blit(text_surf, coords)