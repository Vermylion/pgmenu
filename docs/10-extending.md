# 10. Extending pgmenu

> This chapter supersedes the earlier `New Widget Creation.md` note, which was written against
> a `RectWidget` superclass. The current architecture uses `Widget` plus opt-in mixins
> (`RectMixin`, `TextMixin`).

---

## 10.1 Checklist for a new widget

| Step | File | What to do |
| --- | --- | --- |
| 1 | `constants.py` | Add a widget type constant, for example `SLIDER = "slider"` |
| 2 | `vars.py` | Append `"slider"` to `widget_types` |
| 3 | `slider.py` | Write the widget class |
| 4 | `__init__.py` | `import pgmenu.slider as slider`, after the other widgets |
| 5 | `themes/DEFAULT.json` | Add a `slider_*` block with every default the widget reads |
| 6 | Docs | Add the attribute table to [Widgets](04-widgets.md) |

Steps 1 and 2 matter more than they look. The type constant is the prefix used by
`resolve_widget` for every theme lookup, and `vars.widget_types` is what the theme engine uses
to recognise widget-prefixed keys when expanding a global `widgets_` attribute.

---

## 10.2 Template

```python
import pygame
import pgmenu
from pgmenu.widget import Widget, RectMixin, TextMixin
from pgmenu.constants import THEME
from pgmenu.theme import resolve, resolve_widget
from pgmenu.animation import *


class Slider(Widget, RectMixin, TextMixin):

    def __init__(self,
                 master: pygame.Surface | Widget,
                 coords: list | tuple | AnimateTuple = THEME,
                 size: list | tuple | AnimateTuple = THEME,
                 fill: tuple | AnimateTuple | pygame.Surface | AnimateSurface = THEME,
                 handle_fill: tuple | AnimateTuple = THEME,
                 value: int | float | Animate = THEME,
                 width: int | Animate = THEME,
                 border_radius: int | Animate = THEME,
                 **kwargs):

        # 1. type MUST be set before super().__init__(), the mixins resolve
        #    theme keys of the form f"{self.type}_{attribute}"
        self.type = pgmenu.SLIDER

        # 2. Widget.__init__ runs the mixins, the animation attributes and the callbacks
        super().__init__(**kwargs)

        # 3. Declared attributes, each resolved against its theme key
        self.master = master
        self.coords = resolve(coords, pgmenu.Theme.slider_coords)
        self.size = resolve(size, pgmenu.Theme.slider_size)
        self.fill = resolve(fill, pgmenu.Theme.slider_fill)
        self.handle_fill = resolve(handle_fill, pgmenu.Theme.slider_handle_fill)
        self.value = resolve(value, pgmenu.Theme.slider_value)
        self.width = resolve(width, pgmenu.Theme.slider_width)

        # A theme value of null falls through to the third argument
        self.border_radius = resolve(border_radius,
                                     pgmenu.Theme.slider_border_radius,
                                     round(min(self.size) / 2))

        # 4. Optional sub-part styling, resolved per widget type with a shared fallback
        self.handle_antialiasing = resolve_widget(kwargs, 'handle_antialiasing',
                                                  self.type,
                                                  pgmenu.Theme.rectmixin_antialiasing)

        # 5. Register with the engine, always last
        pgmenu.widget.add(self)

    # One accessor per public attribute, matching the library convention
    def get_master(self):
        return self.master

    def get_handle_fill(self):
        return self.handle_fill

    def get_value(self):
        return self.value

    def draw(self):
        super().draw()          # sets _drawn, required

        # Build the widget's own surface, never blit directly to the master
        self.surface = pgmenu.draw.aarect(None, self.fill, (0, 0, *self.size.int_tuple),
                                          self.width, self.border_radius,
                                          self.border_top_left_radius,
                                          self.border_top_right_radius,
                                          self.border_bottom_left_radius,
                                          self.border_bottom_right_radius,
                                          self.antialiasing, self.transparency,
                                          self.aa_strength,
                                          inner_fill=self.inner_fill,
                                          inner_transparency=self.inner_transparency,
                                          inner_aa_strength=self.inner_aa_strength,
                                          inner_antialiasing=self.inner_antialiasing)

        handle_x = round(self.size[0] * float(self.value))
        handle = pgmenu.draw.aarect(None, self.handle_fill,
                                    (0, 0, 12, round(self.size[1])),
                                    border_radius=6)
        self.surface.blit(handle, (handle_x, 0))

        # master is either the display surface or a Frame, both expose blit()
        self.master.blit(self.surface, self.coords.int_tuple)

    def update(self, event):
        super().update(event)   # measures surface_size and refreshes rect, required

        if self.state == pgmenu.HOVERED or self.state == pgmenu.ACTIVE:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                self.state = pgmenu.ACTIVE
                self.on_press()
                self.animation_on_press()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                self.state = pgmenu.NORMAL
                self.on_release()
                self.animation_on_release()

        if self.state == pgmenu.ACTIVE:
            local_x = pgmenu.vars.mouse_x - self.rect.x
            self.value = max(0.0, min(1.0, local_x / max(self.rect.width, 1)))

    def resize(self, w, h):
        self._resize_border_radii(w, h)   # before assigning the new size
        self.size = w, h

    def m_animation_on_hover(self):
        if not self.disable_animation:
            self.size.update(pgmenu.FORWARD)
            self.fill.update(pgmenu.FORWARD)
            self._animation_update_border_radii(pgmenu.FORWARD)

    def m_animation_on_standby(self):
        if not self.disable_animation:
            self.size.update(pgmenu.BACKWARD)
            self.fill.update(pgmenu.BACKWARD)
            self._animation_update_border_radii(pgmenu.BACKWARD)

    def request_cursor(self):
        pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_HAND
```

And the theme block:

```json
"#": "Slider",
"slider_coords": [20, 20],
"slider_size": [180, 12],
"slider_fill": [63, 68, 72],
"slider_handle_fill": [42, 120, 205],
"slider_value": 0.5,
"slider_width": 0,
"slider_border_radius": null,
```

---

## 10.3 Contracts a widget must honour

| Contract | Why |
| --- | --- |
| `self.type` before `super().__init__()` | Mixins and `resolve_widget` need it |
| `pgmenu.widget.add(self)` at the end of `__init__` | Registers with the draw and update passes |
| `super().draw()` first in `draw()` | Sets `_drawn`, without which the widget is never updated |
| `super().update(event)` first in `update()` | Measures `surface_size` and refreshes the hit rect |
| Assign to `self.surface`, then blit it to `self.master` | `surface_size` and hit testing derive from it |
| `_resize_border_radii(w, h)` before `self.size = w, h` | The factor is computed from the old `base_size` |
| Use `pgmenu.THEME` as every parameter default | Keeps the widget themeable |
| Guard stock animation hooks with `self.disable_animation` | Lets users switch animation off |

Optional but conventional:

* One `get_<attribute>()` accessor per public attribute.
* `request_cursor()` when the widget is interactive.
* `has_draw_priority = True` when the widget should be drawn on top while hovered.

---

## 10.4 Overriding `__setattr__`

Only do this when an attribute needs to keep a shadow copy, as `Surface` does:

```python
def __setattr__(self, key, value):
    super().__setattr__(key, value)   # ALWAYS first, the base class does the real work

    if key == "surface":
        self._surface = value
```

Never bypass `Widget.__setattr__`: it is where animation wrapping, base geometry tracking,
master validation and mixin hooks live.

---

## 10.5 Writing a mixin

A mixin contributes a family of attributes and helpers to any widget that inherits it. Two
hooks are recognised:

```python
class ShadowMixin:

    def _mixin_init(self, **kwargs):
        # Called by Widget._init_mixins before the widget body runs.
        # self.type already exists; nothing else does.
        self.shadow_offset  = resolve_widget(kwargs, 'shadow_offset',  self.type, (0, 2))
        self.shadow_fill    = resolve_widget(kwargs, 'shadow_fill',    self.type, (0, 0, 0, 80))
        self.base_shadow_offset = None

    def _mixin_setattr_hook(self, key, value):
        # Called by Widget.__setattr__ after every assignment.
        if key == "shadow_offset" and not pgmenu.vars.videoresized:
            self.base_shadow_offset = value

    def get_shadow_offset(self):
        return self.shadow_offset
```

Then:

```python
class Card(Widget, RectMixin, ShadowMixin):
    ...
```

Rules:

* Keep mixins flat. `_init_mixins` uses `getattr`, which follows inheritance, so a mixin that
  subclasses another mixin causes the parent's `_mixin_init` to run twice.
* `_mixin_setattr_hook` is looked up in each class `__dict__`, so it does not suffer from the
  same problem.
* Resolve everything through `resolve_widget(kwargs, key, self.type, fallback)` so a theme can
  override per widget type, with a shared `<mixin>_<attribute>` key as the fallback (the
  pattern `rectmixin_antialiasing` follows).

---

## 10.6 Adding an easing curve

Add a one-argument or two-argument callable anywhere importable:

```python
# my_curves.py
import math

def ease_in_wobble(x):
    return x * x * (1 + 0.15 * math.sin(x * math.pi * 6))

def ease_out_wobble(x):
    return 1 - ease_in_wobble(1 - x)

def ease_in_out_wobble(x):
    return ease_in_wobble(2 * x) / 2 if x < 0.5 else (1 + ease_out_wobble(2 * x - 1)) / 2

def wobble(x, direction):
    return globals()[f"ease_{direction}_wobble"](x)
```

Use it directly:

```python
import my_curves
anim = pgmenu.animation.Animate(0, 100, 0.4, my_curves.wobble)
```

Or from a theme, as long as the module is imported before the theme is loaded:

```json
"widget_animation_curve": {"type": "function", "module": "my_curves", "function": "wobble"}
```

Following the `family(x, direction)` plus `ease_{in,out,in_out}_{name}(x)` naming convention
lets pgmenu choose the direction automatically. A plain one-argument callable also works and
is never given a direction.

---

## 10.7 Adding a theme

See [Theming](06-theming.md#611-writing-your-own-theme). In short: create
`pgmenu/themes/NAME.json` with a single top-level key matching the file name, declare only the
keys you want to change, and load it after import. Loading is additive on top of `DEFAULT`.

---

## 10.8 Hooking into the loop without a widget

You do not have to build a widget to participate. Three lighter options:

**A drawn-only object.** Call `pgmenu.draw.aarect` and `pgmenu.text.write` yourself between
`screen.fill` and `pgmenu.draw_all()`. You get the drawing quality and caching without the
widget machinery.

**A bare animation.** Instantiate `Animate` or `AnimateTuple` and update it from your own
loop. Nothing in `pgmenu.animation` depends on the widget system.

**A `Surface` widget.** Render whatever you like into a `pygame.Surface` and wrap it, to get
hit testing, callbacks and responsive resizing for free.
