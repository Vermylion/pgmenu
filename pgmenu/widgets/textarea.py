import math
import pygame
import pgmenu

from pgmenu.widgets import Frame
from pgmenu.base import Widget, TextMixin, ActionableMixin
from pgmenu.core.animation import Animate, AnimateTuple, AnimateSurface, AnimateType
from pgmenu.core.theme import resolve, resolve_kwarg
from pgmenu.vars.constants import THEME


__all__ = ["TextArea"]


# TODO -> Add maybe Scroll Lock?
#  -> Add Ctrl Z -> Needs limited memory


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

        self.content_size = resolve_kwarg(kwargs, "content_size", self.type, self.size)
        self.fit_content = resolve_kwarg(kwargs, "fit_content", self.type)

        self._init_rect(kwargs, "text_cursor_")
        self.text_cursor_fill = resolve_kwarg(kwargs, "text_cursor_fill", self.type)
        self.text_cursor_margin = resolve_kwarg(kwargs, "text_cursor_margin", self.type)
        self.text_cursor_thickness = resolve_kwarg(kwargs, "text_cursor_thickness", self.type)
        # Text Cursor text array position
        self.text_cursor_pos = resolve_kwarg(kwargs, "text_cursor_pos", self.type, len(self.text))

        self.text_cursor_final_transparency = resolve_kwarg(kwargs, "text_cursor_final_transparency", self.type)
        # Setting base custom animation
        if not isinstance(kwargs.get("text_cursor_transparency"), AnimateType):
            self.text_cursor_transparency = pgmenu.animation.Animate(self.text_cursor_transparency, self.text_cursor_final_transparency, 0.4, self.animation_curve, self.animation_precision)

        self._init_rect(kwargs, "text_selection_")
        self.text_selection_fill = resolve_kwarg(kwargs, "text_selection_fill", self.type)

        self.select_pasted_text = resolve_kwarg(kwargs, "select_pasted_text", self.type)
        # Saves the start of text selection
        self._selection_start = None
        # Saves the time and place of last left mouse click
        self._prev_left_mouse_click = 0, 0, 0
        # Delimits if a whole word is selected (from double click)
        self._word_anchor = None
        #
        self._cursor_scroll_key = None

    def add(self, *widgets):
        for widget in widgets:
            if isinstance(widget, pgmenu.widgets.Scrollbar):
                self.widgets += (widget,)
            else:
                raise TypeError(f"Only Scrollbar widgets can be added to the TextArea.")

    def _get_split_idx(self, text, chr_idx, delimiter=" "):
        """
        Takes an absolute character index and returns:
        (item_index_in_split_list, offset_inside_that_item)
        """
        items = text.split(delimiter)

        curr_pos = 0
        for i, item in enumerate(items):
            item_end_pos = curr_pos + len(item)

            # Check if the character index falls inside this item (or right on the edge of its trailing delimiter)
            if chr_idx <= item_end_pos:
                return i, chr_idx - curr_pos

            # Move past the item and its delimiter
            curr_pos = item_end_pos + len(delimiter)

        # Fallback for empty text
        return len(items) - 1, len(items[-1]) if items else 0, 0

    def _get_abs_pos(self, text, item_idx, offset, delimiter=" "):
        """Converts (item_idx, offset) back to an absolute cursor pos."""
        items = text.split(delimiter)
        item_idx = max(0, min(item_idx, len(items) - 1))

        pos = 0
        for i in range(item_idx):
            # Add the length of the item plus the delimiter that followed it
            pos += len(items[i]) + len(delimiter)

        # Add the offset, clamped to the length of the target item
        max_offset = len(items[item_idx]) if items else 0
        return pos + min(offset, max_offset)

    def _get_pos_from_coords(self, text_x, text_y):
        """point in TextArea -> absolute cursor pos"""
        font = pgmenu.text.Font(self.text_font, self.text_size, self.text_italic, self.text_bold)
        lines = self.text.split("\n")

        line_step = max(1, font.get_height() + self.text_line_spacing)
        line_idx = max(0, min(int(text_y // line_step), len(lines) - 1))
        line = lines[line_idx]

        # Largest column whose prefix is <= text_x
        # Binary search
        lo, hi = 0, len(line)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if font.size(line[:mid])[0] <= text_x:
                lo = mid
            else:
                hi = mid - 1

        # Snap to the closer of the two neighboring characters
        if lo < len(line):
            w_here = font.size(line[:lo])[0]
            w_next = font.size(line[:lo + 1])[0]

            if abs(text_x - w_next) < abs(text_x - w_here):
                lo += 1

        return self._get_abs_pos(self.text, line_idx, lo, "\n")

    def _scroll_to_cursor(self, cursor_rect):
        """Scroll the minimum distance needed to bring the cursor into view."""
        cx, cy, cw, ch = cursor_rect

        # Where we are heading, not where the animation currently is
        target_x, target_y = self.scroll_offset.final_value

        # Text is drawn at (margin - scroll), so the cursor stays inside the frame
        # padding while  scroll <= cursor_left  and  cursor_right <= scroll + size - 2*margin
        view_w = self.size.int_tuple[0] - self.margin * 2
        view_h = self.size.int_tuple[1] - self.margin * 2

        if cx < target_x:
            target_x = cx
        elif cx + cw > target_x + view_w:
            target_x = cx + cw - view_w

        if cy < target_y:
            target_y = cy
        elif cy + ch > target_y + view_h:
            target_y = cy + ch - view_h

        # scroll_to clamps to the content size and ignores a target it is already heading to
        self.scroll_to(target_x, target_y, animate=True)

    def draw(self):
        Widget.draw(self)

        x, y = self.scroll_offset

        self.surface = pgmenu.draw.aarect(None, self.fill, (0, 0, *self.size.int_tuple), self.width, self.border_radius,
                                          self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius,
                                          self.antialiasing, self.transparency, self.aa_strength, inner_fill=self.inner_fill,
                                          inner_transparency=self.inner_transparency, inner_aa_strength=self.inner_aa_strength, inner_antialiasing=self.inner_antialiasing)

        # Draw the selection underneath the text
        # Draw the selection underneath the text
        if self._selection_start is not None:
            start = min(self._selection_start, self.text_cursor_pos)
            end = max(self._selection_start, self.text_cursor_pos)

            start_line_idx, start_offset = self._get_split_idx(self.text, start, "\n")
            end_line_idx, end_offset = self._get_split_idx(self.text, end, "\n")

            lines = self.text.split("\n")
            text_font = pgmenu.text.Font(self.text_font, self.text_size, self.text_italic, self.text_bold)
            newline_width, line_height = text_font.size(" ")
            line_pitch = max(line_height + self.text_line_spacing, 1)

            # Visible window in text space
            ox, oy = round(x), round(y)
            vis_left = ox - self.margin
            vis_top = oy - self.margin
            vis_right = vis_left + self.size.int_tuple[0]
            vis_bottom = vis_top + self.size.int_tuple[1]

            # Padding so clipped edges (and their rounded corners) fall outside the visible area
            pad = round(line_height/2) + 2

            # Only the lines that intersect the window (line i spans [i*pitch, (i+1)*pitch))
            first_line = max(start_line_idx, vis_top // line_pitch)
            last_line = min(end_line_idx, (vis_bottom - 1) // line_pitch)

            for line_idx in range(first_line, last_line + 1):
                line = lines[line_idx]

                sel_start = start_offset if line_idx == start_line_idx else 0
                sel_end = end_offset if line_idx == end_line_idx else len(line)

                x_sel, _ = text_font.size(line[:sel_start])
                w_sel, _ = text_font.size(line[sel_start:sel_end])

                # A selection spanning the line break also highlights the "\n"
                if line_idx != end_line_idx:
                    w_sel += newline_width

                if w_sel < 1:
                    continue

                left, right = x_sel, x_sel + w_sel

                # Entirely outside horizontally
                if right < vis_left or left > vis_right:
                    continue

                # Intersect with the (padded) window; edges that are already inside stay as they are
                left = max(left, vis_left - pad)
                right = min(right, vis_right + pad)

                rect = (left, line_idx * line_pitch, right - left, line_pitch)

                surface = pgmenu.draw.aarect(None, self.text_selection_fill, rect, self.text_selection_width, self.text_selection_border_radius,
                                             self.text_selection_border_top_left_radius, self.text_selection_border_top_right_radius,
                                             self.text_selection_border_bottom_left_radius, self.text_selection_border_bottom_right_radius,
                                             self.text_selection_antialiasing, self.text_selection_transparency, self.text_selection_aa_strength,
                                             inner_fill=self.text_selection_inner_fill, inner_transparency=self.text_selection_inner_transparency,
                                             inner_aa_strength=self.text_selection_inner_aa_strength,
                                             inner_antialiasing=self.text_selection_inner_antialiasing)

                self.blit(surface, (rect[0] + self.margin - ox, rect[1] + self.margin - oy))

        # Render text
        text_surface = pgmenu.text.render(self.text, self.text_color, self.text_size, self.text_font, self.text_background, self.text_antialias,
                                          self.text_italic, self.text_bold, self.text_strikethrough, self.text_underline, self.text_transparency, self.text_line_spacing)

        self.blit(text_surface, (self.margin - x, self.margin - y))

        # Render text before cursor to know where to place the cursor
        if self.state == pgmenu.ACTIVE:
            text_font = pgmenu.text.Font(self.text_font, self.text_size, self.text_italic, self.text_bold)

            line_idx, col_idx = self._get_split_idx(self.text, self.text_cursor_pos, "\n")
            line_text = self.text.split("\n")[line_idx][:col_idx]

            w_text, h_text = text_font.size(line_text)

            text_cursor_rect = (w_text, line_idx * (h_text + self.text_line_spacing), self.text_cursor_thickness, h_text)

            # Only auto scroll when the cursor or text changed, so manual scrolling isn't fought every frame
            cursor_key = (self.text_cursor_pos.int, self.text)
            if cursor_key != self._cursor_scroll_key:
                self._cursor_scroll_key = cursor_key
                self._scroll_to_cursor(text_cursor_rect)

            text_cursor_surface = pgmenu.draw.aarect(None, self.text_cursor_fill, text_cursor_rect, self.text_cursor_width, self.text_cursor_border_radius,
                                                self.text_cursor_border_top_left_radius, self.text_cursor_border_top_right_radius, self.text_cursor_border_bottom_left_radius, self.text_cursor_border_bottom_right_radius,
                                                self.text_cursor_antialiasing, self.text_cursor_transparency, self.text_cursor_aa_strength, inner_fill=self.text_cursor_inner_fill,
                                                inner_transparency=self.text_cursor_inner_transparency, inner_aa_strength=self.text_cursor_inner_aa_strength, inner_antialiasing=self.text_cursor_inner_antialiasing)

            self.blit(text_cursor_surface, (text_cursor_rect[0] + self.margin - x, text_cursor_rect[1] + self.margin - y))

        self.draw_widgets()

        self.blit_to_master()

    def _get_mouse_text_pos(self):
        """Text index under the mouse, or None if the mouse is over a child (scrollbar)."""
        mouse = (pgmenu.vars.mouse_x, pgmenu.vars.mouse_y)

        if any(w.rect.collidepoint(mouse) for w in self.widgets):
            return None

        x = mouse[0] - self.rect.topleft[0] - self.margin + self.scroll_offset.float_tuple[0]
        y = mouse[1] - self.rect.topleft[1] - self.margin + self.scroll_offset.float_tuple[1]

        return self._get_pos_from_coords(x, y)

    def _word_bounds(self, pos):
        """(start, end) of the word around pos, delimited by spaces and newlines."""
        n = len(self.text)
        pos = max(0, min(pos, n))

        start = pos
        while start > 0 and self.text[start - 1] not in (" ", "\n"):
            start -= 1

        end = pos
        while end < n and self.text[end] not in (" ", "\n"):
            end += 1

        return start, end

    def _on_press(self):
        self.set_state(pgmenu.ACTIVE)

    def _on_hold(self):
        if pygame.key.get_pressed()[pygame.K_RETURN] or self.state != pgmenu.ACTIVE:
            return

        pos = self._get_mouse_text_pos()
        if pos is None:
            return

        if self._word_anchor is not None:
            # Dragging after a double click: extend by whole words
            a_start, a_end = self._word_anchor
            w_start, w_end = self._word_bounds(pos)

            if pos < a_start:  # dragging left of the original word
                self._selection_start, self.text_cursor_pos = a_end, w_start
            else:  # on or right of it
                self._selection_start, self.text_cursor_pos = a_start, w_end
        else:
            self.text_cursor_pos = pos

    def _on_release(self):
        self._word_anchor = None  # always end word-drag mode first

        if not pygame.key.get_pressed()[pygame.K_RETURN]:
            if self._selection_start == self.text_cursor_pos:
                self._selection_start = None

    def update(self, event):
        Widget.update(self, event)

        if self.state == pgmenu.HOVERED or self.state == pgmenu.ACTIVE:

            keys = pygame.key.get_pressed()

            # Special actions with LEFT CTRL
            if not isinstance(self.master, pgmenu.widgets.Frame) or keys[pygame.K_LCTRL] or \
                    (self.rect.collidepoint(pgmenu.vars.mouse_x, pgmenu.vars.mouse_y) and self.state == pgmenu.ACTIVE):
                # Scrolling
                if event.type == pygame.MOUSEWHEEL:
                    scroll_travel_x = max(min(event.precise_x * self.scroll_step, self.scroll_step), -1 * self.scroll_step)
                    scroll_travel_y = max(min(event.precise_y * -1 * self.scroll_step, self.scroll_step), -1 * self.scroll_step)

                    # Left Shift inverts x,y movement between themselves -> x becomes y and y becomes x
                    if keys[pygame.K_LSHIFT]:
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

            self.animation_on_active()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    # Get text array position
                    pos = self._get_mouse_text_pos()
                    if pos is None:
                        return

                    # Double click detection
                    current_time = pygame.time.get_ticks()
                    mouse_x, mouse_y = (pgmenu.vars.mouse_x, pgmenu.vars.mouse_y)
                    prev_time, prev_x, prev_y = self._prev_left_mouse_click

                    if current_time - prev_time < pgmenu.system.DOUBLE_CLICK_DELAY and \
                            prev_x-5<=mouse_x<=prev_x+5 and prev_y-5<=mouse_y<=prev_y+5:

                        self._word_anchor = self._word_bounds(pos)
                        self._selection_start, self.text_cursor_pos = self._word_anchor
                    else:
                        self._word_anchor = None

                        # Mouse text selection logic
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                            if self._selection_start is None:
                                self._selection_start = self.text_cursor_pos
                        else:
                            self._selection_start = pos
                        self.text_cursor_pos = pos

                    self._prev_left_mouse_click = current_time, mouse_x, mouse_y

            elif event.type == pygame.KEYDOWN:
                action_key_down(event.key)

                line_idx, col_idx = self._get_split_idx(self.text, self.text_cursor_pos, "\n")

                start = min(self._selection_start if self._selection_start is not None else self.text_cursor_pos, self.text_cursor_pos)
                end = max(self._selection_start if self._selection_start is not None else self.text_cursor_pos, self.text_cursor_pos)
                has_selection = start != end

                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    if self._selection_start is None:
                        self._selection_start = self.text_cursor_pos

                if self._selection_start is not None and keys[pygame.K_c] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                    # FIXME -> This is pygame-ce specific syntax
                    pygame.scrap.put_text(self.text[start:end])

                if keys[pygame.K_v] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                    # FIXME -> This is pygame-ce specific syntax
                    scrap_text = pygame.scrap.get_text()

                    if has_selection:
                        self.text = self.text[:start] + self.text[end:]
                        self.text_cursor_pos = start
                        self._selection_start = None

                    if self.select_pasted_text:
                        self._selection_start = self.text_cursor_pos

                    self.text = self.text[:self.text_cursor_pos] + scrap_text + self.text[self.text_cursor_pos:]
                    self.text_cursor_pos += len(scrap_text)

                if self._selection_start is not None and keys[pygame.K_x] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                    # FIXME -> This is pygame-ce specific syntax
                    pygame.scrap.put_text(self.text[start:end])

                    self.text = self.text[:start] + self.text[end:]
                    self.text_cursor_pos -= max(self.text_cursor_pos - self._selection_start, 0)
                    self._selection_start = None

                if keys[pygame.K_a] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                    self._selection_start = 0
                    self.text_cursor_pos = len(self.text)

                elif event.key == pygame.K_BACKSPACE:
                    if self._selection_start is not None:
                        self.text = self.text[:start] + self.text[end:]
                        self.text_cursor_pos -= max(self.text_cursor_pos - self._selection_start, 0)

                    elif self.text_cursor_pos > 0:
                        self.text = self.text[:self.text_cursor_pos - 1] + self.text[self.text_cursor_pos:]
                        self.text_cursor_pos -= 1

                elif event.key == pygame.K_DELETE:
                    if self._selection_start is not None:
                        self.text = self.text[:start] + self.text[end:]
                        self.text_cursor_pos -= max(self.text_cursor_pos - self._selection_start, 0)
                    else:
                        self.text = self.text[:self.text_cursor_pos] + self.text[self.text_cursor_pos + 1:]

                elif event.key == pygame.K_RETURN:
                    if self._selection_start is not None:
                        self.text = self.text[:start] + self.text[end:]
                        self.text_cursor_pos -= max(self.text_cursor_pos - self._selection_start, 0)

                    self.text = self.text[:self.text_cursor_pos] + "\n" + self.text[self.text_cursor_pos:]
                    self.text_cursor_pos += 1

                elif event.key == pygame.K_LEFT:
                    # Move by words and not characters
                    if keys[pygame.K_LCTRL]:
                        pos = self.text_cursor_pos

                        # skip spaces/tabs behind the cursor, so we can detect the start of the line
                        while pos > 0 and self.text[pos - 1] in " \t":
                            pos -= 1

                        if pos > 0 and self.text[pos - 1] == "\n":
                            if pos == self.text_cursor_pos:
                                # already at the start of the line: go to the end of the previous line
                                pos -= 1
                            # otherwise we only skipped indentation, so stay at the start of the line
                        else:
                            # normal case: move to the start of the word behind the cursor
                            while pos > 0 and not self.text[pos - 1].isspace():
                                pos -= 1

                        self.text_cursor_pos = pos
                    else:
                        self.text_cursor_pos = max(0, self.text_cursor_pos - 1)

                elif event.key == pygame.K_RIGHT:
                    # Move by words and not characters
                    if keys[pygame.K_LCTRL]:
                        n = len(self.text)
                        pos = self.text_cursor_pos

                        # skip the rest of the current word
                        while pos < n and not self.text[pos].isspace():
                            pos += 1
                        # skip spaces/tabs only, so we can detect the end of the line
                        while pos < n and self.text[pos] in " \t":
                            pos += 1

                        # hit a line break
                        if pos < n and self.text[pos] == "\n" and pos == self.text_cursor_pos:
                            # already at the end of the line: cross it and land on the next word
                            pos += 1
                            while pos < n and self.text[pos].isspace():
                                pos += 1
                        # otherwise we moved, so stay at the end of the line
                        self.text_cursor_pos = pos
                    else:
                        self.text_cursor_pos = min(len(self.text), self.text_cursor_pos + 1)

                elif event.key == pygame.K_UP:
                    if line_idx > 0:
                        target_line = line_idx - 1
                        self.text_cursor_pos = self._get_abs_pos(self.text, target_line, col_idx, "\n")

                elif event.key == pygame.K_DOWN:
                    if line_idx < len(self.text.split("\n")) - 1:
                        target_line = line_idx + 1
                        self.text_cursor_pos = self._get_abs_pos(self.text, target_line, col_idx, "\n")

                elif event.key == pygame.K_HOME:
                    self.text_cursor_pos = 0

                elif event.key == pygame.K_END:
                    self.text_cursor_pos = len(self.text)

                elif event.key == pygame.K_PAGEUP:
                    text_font = pgmenu.text.Font(self.text_font, self.text_size, self.text_italic, self.text_bold)
                    line_height = text_font.get_height()

                    new_line_idx = line_idx - round(self.size[1] / line_height)

                    self.text_cursor_pos = self._get_abs_pos(self.text, new_line_idx, col_idx, "\n")

                elif event.key == pygame.K_PAGEDOWN:
                    text_font = pgmenu.text.Font(self.text_font, self.text_size, self.text_italic, self.text_bold)
                    line_height = text_font.get_height()

                    new_line_idx = line_idx + round(self.size[1] / line_height)

                    self.text_cursor_pos = self._get_abs_pos(self.text, new_line_idx, col_idx, "\n")

                # Reset selection
                if not (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and not (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and not (event.unicode and event.unicode.isprintable()):
                    self._selection_start = None

            elif event.type == pygame.KEYUP:
                action_key_up(event.key)

            elif event.type == pygame.TEXTINPUT:
                if self._selection_start is not None and self._selection_start != self.text_cursor_pos:
                    start = min(self._selection_start, self.text_cursor_pos)
                    end = max(self._selection_start, self.text_cursor_pos)

                    self.text = self.text[:start] + self.text[end:]
                    self.text_cursor_pos = start

                self.text = self.text[:self.text_cursor_pos] + event.text + self.text[self.text_cursor_pos:]
                self.text_cursor_pos += len(event.text)  # Safe in case event.text has multiple chars
                self._selection_start = None

            elif event.type == pgmenu.IDLE_EVENT:
                if keys:
                    action_key_hold(keys)
