# Code review

Findings from reading the library end to end. **Nothing here has been applied**; every code
block is a proposal. Items are ordered by severity within each section, and the
identifiers match [docs/13-known-issues.md](docs/13-known-issues.md).

---

## 1. Bugs with proposed fixes

### K1. `import pgmenu` can fail on non-Windows platforms

`display.py` line 5:

```python
import ctypes
from ctypes import wintypes
```

`__init__.py` imports `pgmenu.display` unconditionally, so a platform where
`ctypes.wintypes` cannot be imported loses the entire library.

```python
# proposed
import ctypes

# and inside each of the two functions:
def set_transparent_window(transparency):
    from ctypes import wintypes
    ...
```

Or a module-level guard:

```python
import sys
if sys.platform == "win32":
    from ctypes import wintypes
```

with an early raise inside the two functions on other platforms, which keeps the failure at
the point of use and makes the platform requirement explicit.

### K3. The draw priority condition is always true

`lib.py`, `_draw`:

```python
# current
if pgmenu.FRAME or ((widget.state == pgmenu.HOVERED or widget.state == pgmenu.ACTIVE)
                    and pgmenu.system.widget_draw_priority and widget.has_draw_priority):

# proposed
if widget.type == pgmenu.FRAME or ((widget.state == pgmenu.HOVERED or widget.state == pgmenu.ACTIVE)
                                   and pgmenu.system.widget_draw_priority and widget.has_draw_priority):
```

`pgmenu.FRAME` is the truthy string `"frame"`. As written, every widget is promoted to the
second tier, `widget_draw_priority` and `has_draw_priority` have no effect, and frames are
drawn in registration order rather than after their children, which introduces a one-frame lag
in frame content.

This is probably the single highest-value fix in the list: it silently disables two features
at once.

### K7. Global `widgets_` theme attributes raise `TypeError`

`theme.py`, `Theme.set`:

```python
if any_attr.startswith(pgmenu.vars.widget_types):
```

`str.startswith` requires a string or a tuple. Either change the declaration:

```python
# vars.py, proposed
widget_types = ("label", "surface", "frame", "button", "checkbox", "radiobutton")
```

or convert at the call site:

```python
if any_attr.startswith(tuple(pgmenu.vars.widget_types)):
```

The tuple form is preferable: `widget_types` is a constant, and `Theme.set` is on the hot path
of every theme load.

While there, the loop currently also re-visits the `widgets_` key itself. Skipping it avoids
setting an attribute nothing reads:

```python
if attr.startswith("widgets_"):
    suffix = attr[len("widgets_"):]
    for any_attr in attrs:
        if any_attr.startswith(widget_types) and any_attr.endswith(suffix):
            setattr(self, any_attr, value)
```

Note that the current implementation applies the global value to *every* widget-prefixed key
rather than only to keys with the matching suffix, which means `widgets_border_radius` would
overwrite `button_fill` as well. The suffix check above fixes that too.

### K4. `clear_cache` raises `AttributeError`

`cache.py`:

```python
# current
def clear_cache():
    for cache_var in pgmenu.vars.cache:
        getattr(pgmenu.vars, cache_var).clear()

# proposed
def clear_cache():
    for cache_dict in pgmenu.vars.cache.values():
        cache_dict.clear()
```

### K6. The `exec` theme type never assigns

`theme.py`, `Theme.set`:

```python
# current
elif value['type'] == "exec":
    exec("value = " + value["code"])

# proposed
elif value['type'] == "exec":
    namespace = {"self": self, "pgmenu": pgmenu, "pygame": pygame}
    exec("value = " + value["code"], namespace)
    value = namespace["value"]
```

`eval` would be simpler still, given the documented contract is an expression:

```python
elif value['type'] == "exec":
    value = eval(value["code"], {"self": self, "pgmenu": pgmenu, "pygame": pygame})
```

### K10. `match_font` passes a tuple to pygame

`text.py`:

```python
# current
font_name = os.path.splitext(font)

# proposed
font_name = os.path.splitext(font)[0]
```

### K12. `FULL-DEFAULT.json` is missing a key

Add, in the Animation block, to match `DEFAULT.json`:

```json
"animation_precision": 0,
```

Longer term, the duplication itself is the problem; see section 3.

### K11. `AARect` cache identity for surface fills

`aarect.py`, `format_rect`:

```python
self.object_cache_id = (str(self.fill), ...)
```

`str(surface)` yields `<Surface(200x60x32 SW)>`, identical for any two surfaces of the same
dimensions and format. Two different gradients of the same size collide.

```python
# proposed helper
def _fill_id(fill):
    if isinstance(fill, pygame.Surface):
        return id(fill)
    return str(fill)
```

`id()` is stable for the lifetime of the object and cheap. It over-invalidates if a caller
rebuilds an identical surface each frame, which is already a pattern to avoid.

### K8. `fit_render_animated` returns a malformed rect

`text.py`:

```python
# current
text_rect = (*text_pos, text_rect[2:])

# proposed
text_rect = (*text_pos, *text_rect[2:])
```

No caller is affected today, which is exactly why it should be fixed before one is.

### K5 and K9. Leftover debugging

`frame.py`, `Frame.draw`: remove `debug=True` from the `pgmenu.draw.aarect` call, or make it
`debug=pgmenu.Theme.aarect_debug`.

`button.py`, `m_on_release`: replace the `print` with `...` so the default is a genuine no-op,
matching every other `m_on_*`.

### K13. `Menu.__init__` forwards to `object`

```python
# current
def __init__(self, *widgets, **kwargs):
    self.widgets = list(widgets)
    super().__init__(**kwargs)

# proposed
def __init__(self, *widgets, **kwargs):
    self.widgets = list(widgets)
    super().__init__()
```

Or drop `**kwargs` from the signature until there is something to put in it.

---

## 2. Robustness suggestions

### 2.1 Compare sentinels by identity

`theme.py`, `resolve`:

```python
# current
if value != pgmenu.THEME and value != pgmenu.UNSET:

# proposed
if value is not pgmenu.THEME and value is not pgmenu.UNSET:
```

`!=` invokes the value's own `__ne__`. For pgmenu's own types this is harmless, but a
`pygame.Color`, a numpy array or any user type with an unusual comparison can raise or return
something ambiguous inside what should be a trivial sentinel check. Since both sentinels are
module-level string constants, identity is both correct and faster.

The same applies to the state comparisons in `lib.update` and `Button.update`, though those
compare a widget's own attribute and are lower risk.

### 2.2 Use `isinstance` for the theme special-type check

`theme.py`, `Theme.set`:

```python
# current
if type(value) == dict:
    if value['type'] == "method":

# proposed
if isinstance(value, dict):
    kind = value.get("type")
    if kind is None:
        raise ValueError(f"theme attribute {attr!r} is an object without a 'type' key")
    if kind == "method":
```

Today a nested JSON object without a `"type"` key raises a bare `KeyError` with no indication
of which attribute caused it.

### 2.3 Do not mutate the caller's event list

`lib.py`, `update`:

```python
# current
events = [events] if isinstance(events, pygame.event.Event) else events
if len(events) == 0:
    events.append(pygame.event.Event(123))

# proposed
events = [events] if isinstance(events, pygame.event.Event) else list(events)
if not events:
    events.append(pygame.event.Event(pygame.USEREVENT))
```

Two improvements: the copy leaves the caller's list untouched, and `pygame.USEREVENT` is a
documented type rather than the arbitrary `123`. A dedicated module constant would be clearer
still:

```python
# constants.py
IDLE_EVENT = pygame.USEREVENT + 100
```

### 2.4 Deep-normalise cache keys

`cache.py`, `Cache._normalize` only walks one level:

```python
# proposed
def _normalize(self, key):
    if isinstance(key, pgmenu.animation.AnimateType):
        return key.value
    if isinstance(key, tuple):
        return tuple(self._normalize(k) for k in key)
    return key
```

`rect.fit_rects` builds a key containing a tuple of tuples. It happens to work today because
the inner tuples are always plain, but nothing enforces that.

### 2.5 Clamp animated colours

The colour overflow described in the animation documentation could be handled centrally in
`Widget.__setattr__`, where the wrapping happens:

```python
elif isinstance(value, (tuple, list)) and all(isinstance(v, (int, float)) for v in value):
    if key in ("color", "fill", "text_color", "background", "check_fill"):
        pairs = [(v, min(max(v * self.animation_scale, 0), 255)) for v in value]
    else:
        pairs = [(v, v * self.animation_scale) for v in value]
```

A name-based check is inelegant. A cleaner alternative is a class-level declaration each
widget can extend:

```python
class Widget:
    COLOR_ATTRIBUTES = ("color", "fill", "text_color", "background")
```

This also opens the door to a per-attribute animation scale, which would address the second
half of the colour problem (not being able to choose the destination colour) without forcing
users to build the `AnimateTuple` by hand.

### 2.6 Guard `_init_mixins` against duplicate calls

```python
# proposed
def _init_mixins(self, **kwargs):
    seen = set()
    for cls in type(self).__mro__[1:]:
        init = cls.__dict__.get("_mixin_init")
        if init and init not in seen:
            seen.add(init)
            init(self, **kwargs)
```

Using `cls.__dict__` rather than `getattr` matches what `__setattr__` already does for
`_mixin_setattr_hook` and removes the "keep mixins flat" caveat entirely.

---

## 3. Structural suggestions

### 3.1 A widget removal API

The most conspicuous missing piece. Widgets are registered in two lists and never leave them.

```python
# widget.py, proposed
def remove(widget):
    """Unregister a widget from the engine."""
    if widget in pgmenu.vars.widgets:
        pgmenu.vars.widgets.remove(widget)
    if widget in pgmenu.vars.widgets_draw_order:
        pgmenu.vars.widgets_draw_order.remove(widget)
    if isinstance(widget.master, pgmenu.frame.Frame):
        widget.master.remove(widget)


class Widget:
    def destroy(self):
        """Remove this widget from the engine."""
        pgmenu.widget.remove(self)
```

`Frame.destroy` would additionally destroy its children. Without this, any dynamic UI leaks
widgets, and `Menu` cannot really own its members.

### 3.2 Replace the `AARect` `temp_*` block with a dataclass

The in-source FIXME already calls for this, and it is the single biggest readability win
available. `draw_rects` currently sets fourteen `temp_*` attributes three times over, and
`draw_rect`, `get_corners`, `aa_corners` and `aa_sides` all read that shared implicit state.

```python
# proposed
from dataclasses import dataclass

@dataclass
class _Pass:
    fill: object
    rect: tuple
    border_radius: int
    border_top_left_radius: int
    border_top_right_radius: int
    border_bottom_left_radius: int
    border_bottom_right_radius: int
    transparency: int
    antialiasing: bool
    aa_strength: int
    inner_borders: bool = False
    inner_aa: bool = False

    @property
    def aa_pixel_width(self):
        return self.aa_strength if self.antialiasing else 0
```

`draw_rect(self, p)`, `get_corners(self, p)`, `aa_corners(self, p, radius)` and
`aa_sides(self, p)` then take the pass explicitly. The three pass constructions become three
readable `_Pass(...)` literals, and the `aa_pixel_width` recomputation currently repeated in
five methods (and unused in two of them) collapses into one property.

### 3.3 Separate state transitions from continuous state

`on_hover` and `on_standby` firing every frame, and `on_hold` firing once per queued event,
are both surprising. A small addition to `Widget` would give both semantics:

```python
class Widget:
    def _set_state(self, state):
        """Change state, firing enter and exit hooks only on an actual transition."""
        if state == self.state:
            return
        previous, self.state = self.state, state
        self.on_state_change(previous, state)
```

with `lib.update` calling `_set_state` and then the continuous hooks, and `on_hold` moved out
of the per-event loop into the per-frame section. This addresses the existing TODO in `lib.py`
about limiting repeated actions.

### 3.4 One source of truth for the default theme

`DEFAULT.json` and `FULL-DEFAULT.json` are 99 percent identical and have already diverged by
one key. Either delete one, or generate `FULL-DEFAULT.json` from `DEFAULT.json` as part of a
release step, or make `FULL-DEFAULT.json` the source and have `DEFAULT.json` be a thin theme
loaded on top of it.

A validation helper would also catch drift early:

```python
def validate(self, required_keys):
    """Return the theme keys the library reads but this theme does not define."""
    return [k for k in required_keys if not hasattr(self, k)]
```

### 3.5 Reconsider the `Frame` blit queue key

`_widgets_to_blit` is a `dict` keyed by surface object. Two children that happen to blit the
same surface object collapse into one entry, and the draw order is dictionary insertion order
rather than the frame's child order.

```python
# proposed
self._widgets_to_blit = []          # list of (surface, coords)

def blit(self, surface, coords):
    self._widgets_to_blit.append((surface, coords))
```

A list is also marginally faster and expresses "a queue" rather than "a mapping".

### 3.6 Avoid a per-frame copy of every cached surface

`AARect.aarect` and `text.render` both end with `.copy()`. That is correct and safe, but it
means every widget allocates and copies its full surface every frame even when nothing has
changed, which undercuts the caching. Two options:

* return the cached surface directly from a `*_shared()` variant and have callers copy only
  when they intend to mutate (`Button` does, `Frame` does, `Label` does not),
* or cache the *composed* widget surface one level higher, keyed on the widget's full visual
  state, so that a static widget re-blits a single unchanged surface.

The second is the larger win and would make a static UI nearly free.

### 3.7 Consistent use of `int_tuple` at blit sites

`Button.draw` uses `self.size.int_tuple` and `self.coords.int_tuple`; `Frame.draw` and
`Surface.draw` pass the `AnimateTuple` itself. Both work, but the inconsistency invites
sub-pixel positioning differences between widgets. Standardising on `int_tuple` for every
blit destination would be a one-line change per widget.

### 3.8 Packaging and typing

* There is no `setup.py`, `pyproject.toml` or `requirements.txt`. Adding a `pyproject.toml`
  with `pygame` as a dependency and package data for `themes/*.json` and `VarelaRound.ttf`
  would make the library installable and would fix the implicit assumption that the working
  directory contains the package.
* `__init__.py` carries a FIXME about `from pgmenu import *`. Defining `__all__` explicitly
  would resolve it and document the public surface at the same time.
* Type annotations are used in widget constructors but not on methods. Annotating return
  types, particularly on `resolve`, `_scale`, `fit_rects` and `center_rects`, would let a type
  checker catch mistakes such as K8 and K10 automatically.

### 3.9 Tests

The three `Debug*.py` scripts are effectively manual tests. The pieces most worth covering
automatically, in order of value per line of test code:

1. `theme.resolve` / `resolve_kwarg` / `resolve_widget` truth tables, which are pure functions.
2. `resize._scale` for both modes, both axes disabled, and the round-trip property that
   scaling to a new size and back restores the base exactly.
3. `Animate.update` step, direction reversal and `reach` clamping, driven by a fake clock.
4. `Cache` key normalisation and LRU eviction.
5. `rect.fit_rects` and `rect.center_rects` geometry.

None of these need a display surface, except that importing `pgmenu` currently requires
`pygame.display` for widget master validation only, so the first four are testable headless.

---

## 4. Documentation-side observations

Corrections already folded into the new documentation, listed here so the source notes can be
updated to match:

* `New Widget Creation.md` documents a `RectWidget` superclass that no longer exists. The
  current pattern is `Widget` plus `RectMixin` and `TextMixin`, and the old note's
  `__setattr__` override is no longer needed for ordinary widgets.
* `../tests/docs-archive/Widget.md` describes animation attribution and callback assignment accurately, but predates
  `disable_animation`, the responsive attributes, `surface_size` and `_drawn`.
* `../tests/docs-archive/Theme.md` is accurate, with two caveats now documented: the `exec` type does not work
  (K6) and the `widgets_` global prefix raises (K7).
* `../tests/docs-archive/Surface.md` is accurate. The `on_resize` example takes no arguments in the current code
  (`DebugWindow.py` closes over the widget with a lambda), which is worth showing explicitly.
* `../tests/docs-archive/Animation.md` is accurate and its colour-argument guidance is the recommended workaround.
* `../tests/docs-archive/info.md`'s note on `surface_size` is correct and has been folded into the architecture
  chapter.
