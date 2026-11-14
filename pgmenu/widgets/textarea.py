import pygame
import pgmenu

from pgmenu.widgets import Frame
from pgmenu.base import Widget, TextMixin, ActionableMixin
from pgmenu.core.animation import Animate, AnimateTuple, AnimateSurface
from pgmenu.core.theme import resolve, resolve_kwarg
from pgmenu.vars.constants import THEME


__all__ = ["TextArea"]


class TextArea(Frame, TextMixin, ActionableMixin):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 coords: list | tuple | AnimateTuple = THEME,
                 size: list | tuple | AnimateTuple = THEME,
                 text: str | None = THEME,
                 text_size: int | Animate = THEME,
                 text_color: tuple[int, int, int] | pygame.Surface | AnimateSurface = THEME,
                 fill: tuple[int, int, int] | pygame.Surface | AnimateSurface = THEME,
                 margin: int | Animate = THEME,
                 width: int | Animate = THEME,
                 border_radius: int | Animate = THEME,
                 **kwargs):

        self.set_type(pgmenu.TEXTAREA)

        # FIXME -> Widget based inheritance doesn't work well with Theme
        super().__init__(master, coords, size, fill, width, border_radius, **kwargs)

        self.border_radius = resolve(border_radius, "border_radius", self.type, round(min(self.size) / 12))

        self.text = resolve(text, "text", self.type)
        self.text_size = resolve(text_size, "text_size", self.type)
        self.text_color = resolve(text_color, "text_color", self.type)

        self.margin = resolve(margin, "margin", self.type)

        self._init_rect(kwargs, "text_cursor_")
        self.text_cursor_fill = resolve_kwarg(kwargs, "text_cursor_fill", self.type)
        self.text_cursor_margin = resolve_kwarg(kwargs, "text_cursor_margin", self.type)
        self.text_cursor_thickness = resolve_kwarg(kwargs, "text_cursor_thickness", self.type)
        # Text Cursor text array position
        self.text_cursor_pos = resolve_kwarg(kwargs, "text_cursor_pos", self.type, len(self.text))

    def add(self, *widgets):
        for widget in widgets:
            if isinstance(widget, pgmenu.widgets.Scrollbar):
                self.widgets += (widget,)
            else:
                raise TypeError(f"Only Scrollbar widgets can be added to the TextArea.")

    def _get_line_col(self):
        """Converts absolute cursor pos to (line_idx, col_idx)."""
        lines = self.text.split("\n")
        current_pos = 0
        for i, line in enumerate(lines):
            line_len = len(line)
            if self.text_cursor_pos <= current_pos + line_len:
                return i, self.text_cursor_pos - current_pos
            current_pos += line_len + 1  # +1 for '\n'
        return max(0, len(lines) - 1), len(lines[-1]) if lines else 0

    def _get_abs_pos(self, line_idx, col_idx):
        """Converts (line_idx, col_idx) back to an absolute cursor pos."""
        lines = self.text.split("\n")
        line_idx = max(0, min(line_idx, len(lines) - 1))

        pos = 0
        for i in range(line_idx):
            pos += len(lines[i]) + 1
        return pos + min(col_idx, len(lines[line_idx]))

    def draw(self):
        Widget.draw(self)

        self.surface = pgmenu.draw.aarect(None, self.fill, (0, 0, *self.size.int_tuple), self.width, self.border_radius,
                                          self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius,
                                          self.antialiasing, self.transparency, self.aa_strength, inner_fill=self.inner_fill,
                                          inner_transparency=self.inner_transparency, inner_aa_strength=self.inner_aa_strength, inner_antialiasing=self.inner_antialiasing)

        text_surface = pgmenu.text.render(self.text, self.text_color, self.text_size, self.text_font, self.text_background, self.text_antialias,
                                          self.text_italic, self.text_bold, self.text_strikethrough, self.text_underline, self.text_transparency, self.text_line_spacing)

        x, y = self.scroll_offset
        self.blit(text_surface, (self.margin - x, self.margin - y))

        # Render text before cursor to know where to place the cursor
        if self.state == pgmenu.ACTIVE:
            font = pgmenu.text.format_font(self.text_font, self.text_italic, self.text_bold)
            text_font = pygame.font.Font(font, self.text_size)

            current_line, current_col = self._get_line_col()
            line_text = self.text.split("\n")[current_line][:current_col]

            w_text, h_text = text_font.size(line_text)

            text_cursor_rect = (w_text, current_line * (h_text + self.text_line_spacing), self.text_cursor_thickness, h_text)

            text_cursor_surface = pgmenu.draw.aarect(None, self.text_cursor_fill, text_cursor_rect, self.text_cursor_width, self.text_cursor_border_radius,
                                                self.text_cursor_border_top_left_radius, self.text_cursor_border_top_right_radius, self.text_cursor_border_bottom_left_radius, self.text_cursor_border_bottom_right_radius,
                                                self.text_cursor_antialiasing, self.text_cursor_transparency, self.text_cursor_aa_strength, inner_fill=self.text_cursor_inner_fill,
                                                inner_transparency=self.text_cursor_inner_transparency, inner_aa_strength=self.text_cursor_inner_aa_strength, inner_antialiasing=self.text_cursor_inner_antialiasing)

            self.blit(text_cursor_surface, (text_cursor_rect[0] + self.margin - x, text_cursor_rect[1] + self.margin - y))

        self.draw_widgets()

        self.blit_to_master()

    def _on_press(self):
        self.set_active()

    def _on_release(self):
        ...

    def update(self, event):
        Widget.update(self, event)

        if self.state == pgmenu.HOVERED or self.state == pgmenu.ACTIVE:

            # Scrolling
            if pygame.key.get_pressed()[pygame.K_LCTRL]:

                if event.type == pygame.MOUSEWHEEL:
                    scroll_travel_x = max(min(event.precise_x * self.scroll_step, self.scroll_step), -1 * self.scroll_step)
                    scroll_travel_y = max(min(event.precise_y * -1 * self.scroll_step, self.scroll_step), -1 * self.scroll_step)

                    # Left Shift inverts x,y movement between themselves -> x becomes y and y becomes x
                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        scroll_travel_x, scroll_travel_y = scroll_travel_y, scroll_travel_x

                    self.scroll_by(scroll_travel_x, scroll_travel_y, animate=True)

        def action_key_down(key):
            self.on_key_press(key)
            self.animation_on_key_press(key)

        def action_key_hold(key):
            self.on_key_hold(key)
            self.animation_on_key_hold(key)

        def action_key_up(key):
            self.on_key_release(key)
            self.animation_on_key_release(key)

        if self.state == pgmenu.ACTIVE:

            if event.type == pygame.KEYDOWN:
                action_key_down(event.key)

                current_line, current_col = self._get_line_col()

                if event.key == pygame.K_BACKSPACE:
                    if self.text_cursor_pos > 0:
                        self.text = self.text[:self.text_cursor_pos - 1] + self.text[self.text_cursor_pos:]
                        self.text_cursor_pos -= 1

                if event.key == pygame.K_DELETE:
                        self.text = self.text[:self.text_cursor_pos] + self.text[self.text_cursor_pos + 1:]

                elif event.key == pygame.K_RETURN:
                    self.text = self.text[:self.text_cursor_pos] + "\n" + self.text[self.text_cursor_pos:]
                    self.text_cursor_pos += 1

                elif event.key == pygame.K_LEFT:
                    self.text_cursor_pos = max(0, self.text_cursor_pos - 1)

                elif event.key == pygame.K_RIGHT:
                    self.text_cursor_pos = min(len(self.text), self.text_cursor_pos + 1)

                elif event.key == pygame.K_UP:
                    if current_line > 0:
                        target_line = current_line - 1
                        self.text_cursor_pos = self._get_abs_pos(target_line, current_col)

                elif event.key == pygame.K_DOWN:
                    if current_line < len(self.text.split("\n")) - 1:
                        target_line = current_line + 1
                        self.text_cursor_pos = self._get_abs_pos(target_line, current_col)

            if event.type == pygame.KEYUP:
                action_key_up(event.key)

            if event.type == pygame.TEXTINPUT:
                self.text = self.text[:self.text_cursor_pos] + event.text + self.text[self.text_cursor_pos:]
                self.text_cursor_pos += len(event.text)  # Safe in case event.text has multiple chars

            if event.type == pgmenu.IDLE_EVENT:
                key_held = pygame.key.get_pressed()
                if key_held:
                    action_key_hold(key_held)