# 7. Responsive resize

pgmenu rescales widget geometry when the window (or a widget's parent `Frame`) changes size.
The system is implemented in `pgmenu/resize.py` and is driven from inside `pgmenu.update()`.

---

## 7.1 The model in one paragraph

Every widget remembers the geometry it was given by the user (`base_size`, `base_coords`).
The window remembers the size it had on the first frame (`pgmenu.vars.base_window_size`).
When a `pygame.VIDEORESIZE` event arrives, each widget's base geometry is expressed as a
fraction of the *base* master size, and that fraction is re-applied to the *current* master
size. Nothing accumulates, so resizing back to the original dimensions restores the original
layout exactly.

---

## 7.2 Base geometry

`Widget.__setattr__` mirrors assignments:

```python
if key in ("size", "coords") and not pgmenu.vars.videoresized:
    setattr(self, f"base_{key}", value)
```

The guard is the whole trick. During a responsive pass, `pgmenu.vars.videoresized` is `True`,
so the widget's `size` and `coords` change while `base_size` and `base_coords` stay frozen at
the design-time values. The flag is raised in `responsive_resize` and lowered by
`reset_videoresize` at the end of `pgmenu.update()`.

Assigning geometry yourself at any other time therefore **redefines the design layout**:

```python
frame.size = (450, 400)   # this is the new base size, all future scaling is relative to it
```

`pgmenu.vars.base_window_size` is captured lazily on the first call to `pgmenu.update()`.
Create your display surface at its intended design size before entering the loop, or your
proportions will be computed against the wrong reference.

Because scalar sizes exist (`Label.size` is a font size),
`Widget.get_2d_base_size()` normalises the base size to a 2-tuple before any maths.

---

## 7.3 Modes

`responsive_size` and `responsive_coords` each take one of three values:

| Value | Behaviour |
| --- | --- |
| `pgmenu.PROPORTIONAL` | Scale both axes by the smaller of the two factors, preserving aspect ratio |
| `pgmenu.STRETCH` | Scale each axis independently, preserving the fraction of the master it covers |
| any falsy value (`False`, `None`) | Do not touch this property |

Theme defaults: `widget_responsive_size = PROPORTIONAL`, `widget_responsive_coords = STRETCH`.
That combination is the one you usually want: a button keeps its shape while its position
tracks the window.

Per-axis switches allow finer control:

| Attribute | Effect when `False` |
| --- | --- |
| `responsive_size_w` | Width stays at its base value |
| `responsive_size_h` | Height stays at its base value |
| `responsive_coords_x` | X stays at its base value |
| `responsive_coords_y` | Y stays at its base value |

```python
# A top bar: full width, fixed height, pinned to the top
bar = pgmenu.frame.Frame(screen, coords=(0, 0), size=(1080, 48))
bar.responsive_size = pgmenu.STRETCH
bar.responsive_size_h = False
bar.responsive_coords = False
```

---

## 7.4 The scaling function

```python
def _scale(base, master_size, master_base_size, mode, resize_x, resize_y):
    base = max(base[0], 1), max(base[1], 1)

    widget_x_coverage = base[0] / master_base_size[0]
    widget_y_coverage = base[1] / master_base_size[1]

    resized_x = round(master_size[0] * widget_x_coverage)
    resized_y = round(master_size[1] * widget_y_coverage)

    if mode == pgmenu.PROPORTIONAL:
        x_resized_factor = resized_x / base[0]
        y_resized_factor = resized_y / base[1]
        aspect_ratio = base[0] / base[1]

        if x_resized_factor < y_resized_factor:
            resized_y = resized_x / aspect_ratio
        elif y_resized_factor < x_resized_factor:
            resized_x = resized_y * aspect_ratio

    if not resize_x:
        resized_x = base[0]
    if not resize_y:
        resized_y = base[1]

    return resized_x, resized_y
```

Reading it as maths:

* **Coverage** is the fraction of the master the property occupied at design time.
* **STRETCH** simply re-applies that fraction. A button covering 20 percent of the width still
  covers 20 percent of the width.
* **PROPORTIONAL** computes both stretch results, keeps the smaller growth factor and derives
  the other axis from the original aspect ratio. A widget therefore never distorts, and never
  exceeds what the tighter axis allows.
* Base components are floored at `1` to avoid division by zero.
* The per-axis switches are applied last, so they override both modes.

---

## 7.5 The dispatch

```python
def responsive_resize(widget, event):
    if event.type == pygame.VIDEORESIZE:

        if widget.responsive_size or widget.responsive_coords:
            pgmenu.vars.videoresized = True

            if isinstance(widget.master, pgmenu.frame.Frame):
                master_size = widget.master.size
                master_base_size = widget.master.base_size
            else:
                master_size = pygame.display.get_window_size()
                master_base_size = pgmenu.vars.base_window_size

        if widget.responsive_size:
            base_size = widget.get_2d_base_size()
            w, h = _scale(base_size, master_size, master_base_size,
                          widget.responsive_size,
                          widget.responsive_size_w, widget.responsive_size_h)
            widget.resize(w, h)
            widget.on_resize()

        if widget.responsive_coords:
            x, y = _scale(widget.base_coords, master_size, master_base_size,
                          widget.responsive_coords,
                          widget.responsive_coords_x, widget.responsive_coords_y)
            widget.coords = x, y
```

Points worth noting:

* Widgets whose master is a `Frame` scale against the frame, not the window, and their
  coordinates stay frame-relative throughout.
* The whole thing is a no-op for any event other than `VIDEORESIZE`. It is called once per
  widget per event from `pgmenu.update()`.
* `on_resize()` fires only when `responsive_size` is active. If you need a resize
  notification on a widget with fixed size, keep `responsive_size` on and give it
  `responsive_size_w = responsive_size_h = False`.
* Frames are resized as part of the same widget loop. Because `pgmenu.vars.widgets` is in
  creation order, a frame created before its children is resized first and the children see
  the new frame size in the same frame. Create containers before their contents.

`pygame.VIDEORESIZE` is not emitted when you call `pygame.display.set_mode` yourself; post it
manually if you resize the window programmatically:

```python
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE))
```

---

## 7.6 The `resize()` contract

`Widget.resize(w, h)` is a no-op. Every widget that supports responsive sizing overrides it.
Two rules:

**1. Rescale dependent properties before assigning the new size.**
`RectMixin._resize_border_radii(w, h)` computes its factor from
`min(w / base_size[0], h / base_size[1])`, so it must run while `base_size` still holds the
old value.

```python
def resize(self, w, h):
    self._resize_border_radii(w, h)
    self.size = w, h
```

**2. Interpret `w, h` in the widget's own terms.** `Label` treats the height as its font
size:

```python
def resize(self, w, h):
    self.size = h
```

Current implementations:

| Widget | `resize(w, h)` |
| --- | --- |
| `Widget` | no-op |
| `Label` | `size = h` |
| `Surface` | set `size`, then rescale the shadow `_surface` into `surface` |
| `Frame` | rescale radii, set `size` |
| `Button` | rescale radii, set `size` |
| `Checkbox` | rescale radii, set `size` |

---

## 7.7 Fonts, images and radii

* **Fonts** rescale because `Label.resize` changes the point size, and because `Button` draws
  its text through `text.fit_render_animated`, which re-fits to the current box every frame.
* **Images** rescale in the `Surface` widget through `pgmenu.surface.resize`, a cached
  `smoothscale`. Surface fills passed to `aarect` are smoothscaled to the rectangle inside
  `AARect.format_rect`.
* **Corner radii** rescale through `_resize_border_radii`, using the smaller of the two
  factors so corners stay circular.

---

## 7.8 Known rough edges

* If `responsive_size` is disabled but `responsive_coords` is enabled, coordinates scale while
  the widget does not, so a centred widget drifts off centre. This is flagged as a TODO in the
  source.
* `_scale` returns floats in the `PROPORTIONAL` branch (the `round` happens before the aspect
  correction). The values feed into animation objects, which tolerate floats, and
  `int_tuple` rounds at draw time.
* Nothing clamps a widget to its master's bounds. A widget can be scaled outside its frame;
  it will still draw (clipped by the frame surface) but its hit rect is clipped by
  `_update_rect`.
* Sustained resizing generates one new cache key per distinct size. `max_cache_size` bounds
  memory, but a drag-resize does invalidate the caches continuously, which is the expected
  frame-rate dip during the drag.
