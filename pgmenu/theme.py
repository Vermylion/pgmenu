import pygame


class Theme:

    def __init__(self):

        self.fill = (45, 120, 205) # 50, 135, 235
        self.text_font = "VarelaRound.ttf"
        self.text_color = (255, 255, 255)
        self.width = 0
        self.outline_fill = (40, 105, 185)
        self.border_radius = 10

    def inherit_theme(self,
                      obj: object | None,
                      *var_names):
        ...
