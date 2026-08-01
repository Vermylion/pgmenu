# 3. Architecture

This chapter describes what actually happens inside pgmenu during one frame, and why the
pieces are arranged the way they are.

---

## 3.1 The global registry

pgmenu has no root widget and no scene graph object. Instead, `pgmenu.widget.add(widget)` is
called at the end of every widget's `__init__` and appends the widget to two global lists in
`pgmenu.vars`:

| List | Purpose |
| --- | --- |
| `pgmenu.vars.widgets` | Iteration order for `pgmenu.update()` (hit testing, callbacks) |
| `pgmenu.vars.widgets_draw_order` | Iteration order for `pgmenu.draw_all()` |

Keeping the two lists separate is what allows draw order and update order to diverge, which
matters for containers: a `Frame` must be *drawn* after its children (so their surfaces have
been queued onto it) but there is no such constraint on update order.

`add()` special-cases frames:

```python
def add(widget):
    def frame_handling():
        for i in range(len(pgmenu.vars.widgets_draw_order)):
            if pgmenu.vars.widgets_draw_order[i].type == pgmenu.FRAME:
                pgmenu.vars.widgets_draw_order.insert(i, widget)
                return
        pgmenu.vars.widgets_draw_order.append(widget)

    if widget.type == pgmenu.FRAME:
        frame_handling()
    else:
        pgmenu.vars.widgets_draw_order.append(widget)

    pgmenu.vars.widgets.append(widget)
```

A new frame is inserted *before* the first frame already in the list; everything else is
appended. The stated intent in the source comment is the opposite (frames at the end). See
[Known issues](13-known-issues.md#k2-frame-draw-order) for the discrepancy and the effect it
has on nested frames.

There is currently no `remove()` counterpart. A widget lives for the lifetime of the process
unless you mutate `pgmenu.vars.widgets` and `pgmenu.vars.widgets_draw_order` yourself, or set
its state to `HIDDEN` (skipped by both passes) or `DISABLED` (skipped by update only).

---

## 3.2 The draw pass

```python
pgmenu.draw_all()      # -> lib._draw(*pgmenu.vars.widgets_draw_order)
```

`_draw` implements a two-tier ordering: normal widgets first, then a `top_widgets` list drawn
afterwards so it lands on top. Membership in the second tier is meant to be decided by

* being a `Frame` (so children can queue their surfaces first), or
* being `HOVERED`/`ACTIVE` while `pgmenu.system.widget_draw_priority` is on and the widget
  sets `has_draw_priority`.

`HIDDEN` widgets are skipped entirely.

> **Current behaviour.** The condition is written `if pgmenu.FRAME or (...)`, and
> `pgmenu.FRAME` is the non-empty string `"frame"`, so it is always true. Every widget is
> therefore promoted to `top_widgets` and drawn in registration order, and the priority
> mechanism is inert. See [Known issues](13-known-issues.md#k3-draw-priority-condition-always-true).

`Widget.draw()` itself does one thing: it sets `self._drawn = True`. Subclasses call
`super().draw()` first and then render. That flag is the gate for the update pass.

---

## 3.3 The blit tree

pgmenu does not composite through a tree of surfaces automatically. Instead:

* A widget whose master is the **display surface** blits straight onto it:
  `self.master.blit(self.surface, coords)`.
* A widget whose master is a **`Frame`** calls `Frame.blit(surface, coords)`, which is *not*
  a real blit. It stores the pair in `frame._widgets_to_blit`.
* When the frame is later drawn, it renders its own rounded rectangle, blits every queued
  child surface onto it, blits itself onto *its* master, and clears the queue.

```
Label.draw()  -> frame._widgets_to_blit[label_surface]  = (20, 20)
Button.draw() -> frame._widgets_to_blit[button_surface] = (20, 150)
Frame.draw()  -> build own surface
              -> blit both queued surfaces
              -> screen.blit(frame.surface, frame.coords)
              -> clear queue
```

This is why the frame must be drawn last, and why child coordinates are frame-relative.
`Widget._update_rect` compensates on the hit-testing side: it converts frame-relative
coordinates into screen coordinates and clips the widget's rect to the frame's bounds, so a
child that overflows its frame is not clickable outside it.

```python
def _update_rect(self, size, coords):
    if isinstance(self.master, pgmenu.frame.Frame):
        size = (min(self.master.size[0] - coords[0], size[0]),
                min(self.master.size[1] - coords[1], size[1]))
        coords = (self.master.coords[0] + coords[0],
                  self.master.coords[1] + coords[1])
    self.rect = pygame.Rect(*coords, *size)
```

Frames nest: a `Frame` can be another `Frame`'s master, and the same queueing mechanism
applies one level up.

---

## 3.4 The update pass

`pgmenu.update(events)` in `lib.py`:

```
1. If vars.base_window_size is None: capture pygame.display.get_window_size()
2. Normalise `events` into a list; if empty, append a dummy Event(123)
3. Cache mouse position into vars.mouse_x / vars.mouse_y
4. For each widget in vars.widgets:
       skip if state is DISABLED or HIDDEN, or if widget._drawn is False
       if widget.rect collides with the mouse:
           if state != ACTIVE: state = HOVERED; on_hover(); animation_on_hover()
           widget.request_cursor()
       elif state != ACTIVE:
           state = NORMAL; on_standby(); animation_on_standby()
       for event in events:
           resize.responsive_resize(widget, event)
           widget.update(event)
       widget._drawn = False
5. resize.reset_videoresize()
6. Apply cursor: user_cursor if set, otherwise widget_cursor
7. Reset user_cursor to None and widget_cursor to the arrow
```

Three details are worth internalising:

**Hover is evaluated once per frame, not once per event.** Only the `widget.update(event)`
and `responsive_resize(widget, event)` calls are inside the per-event loop. This is why the
dummy event is appended when the queue is empty: without it, widgets whose per-frame logic
lives in `update()` would stall on idle frames.

**`ACTIVE` is sticky.** Neither the hover branch nor the standby branch will overwrite an
`ACTIVE` state. Only the widget's own `update()` can leave `ACTIVE`. `Button` does so on
`MOUSEBUTTONUP`.

**`_drawn` gates everything.** A widget skipped by `draw_all` (because it is inside a
`Menu` you did not show, for example) has `_drawn == False` and receives no hover, no
callbacks and no resize handling that frame.

### The default `Widget.update`

```python
def update(self, event):
    self.surface_size = self.surface.get_size()
    self._update_rect(self.surface_size, self.coords)
```

Hit testing therefore uses the size of what the widget *actually rendered* last frame, not
its declared `size`. This matters for `Label`, whose `size` is a font size rather than a
pixel box, and it introduces a deliberate one-frame lag between rendering and hit testing.

---

## 3.5 `size` versus `surface_size`

Two size attributes exist on every widget:

| Attribute | Meaning | Set by |
| --- | --- | --- |
| `size` | The declared, animated, resizable size of the widget | The user and `resize()` |
| `surface_size` | The measured size of the last rendered surface | `Widget.update` |

For `Button` and `Frame` the two agree. For `Label` they do not: `size` is a font point size
(a scalar), while `surface_size` is the rendered text box in pixels. `Label.draw` uses
`surface_size` for centring and `Widget.update` uses it for the hit rect.

The rule of thumb from the project notes: `surface_size` is the fallback for a widget whose
rendering is not representative of its `size` attribute.

`Widget._make_2d` / `_get_2d` / `get_2d_size` / `get_2d_base_size` exist for the same reason:
they normalise a scalar `size` (or a scalar `base_size`) into a 2-tuple so that the resize
maths in `pgmenu.resize` can treat every widget identically.

---

## 3.6 The attribute pipeline

`Widget.__setattr__` is the most important method in the library. Every assignment to a
widget attribute passes through it, in this order:

```
1. Idempotence guard
   If the attribute already holds an AnimateType whose base_value equals the new value,
   return immediately. Re-assigning the same value never restarts an animation.

2. Animation wrapping (only when the incoming value is not already an AnimateType)
   a. If animation_scale / animation_duration / animation_curve are not initialised yet,
      skip wrapping (this is the case during Widget.__init__ itself).
   b. If key == "surface" and the widget is not a Surface widget, skip wrapping.
   c. int or float (but not bool)      -> Animate(value, value * animation_scale, ...)
   d. tuple/list of numbers            -> AnimateTuple((v, v * scale) for each v, ...)
   e. pygame.Surface and key != master -> AnimateSurface(value, brightened copy, ...)

3. Actual assignment via super().__setattr__

4. master validation
   Must be the display surface or a Frame, otherwise ValueError.
   If it is a Frame, the widget registers itself with frame.add(self).

5. Base geometry tracking
   If key is "size" or "coords" and we are not inside a responsive resize
   (pgmenu.vars.videoresized is False), mirror the value into base_size / base_coords.

6. Mixin hooks
   Walk type(self).__mro__ and call every _mixin_setattr_hook found in a class __dict__.
```

Two consequences that surprise people:

* Assigning a plain `bool` is safe (bools are excluded from numeric wrapping) but assigning
  an `int` to something you intended to keep constant still produces an `Animate`. It behaves
  like the number, so this is usually invisible.
* Because step 1 compares against `base_value`, `widget.size = widget.size.base_tuple` is a
  no-op, while `widget.size = (new_w, new_h)` builds a fresh `AnimateTuple` and resets any
  in-flight animation on that attribute.

The `videoresized` flag in step 5 is the mechanism that lets the responsive system change
`size` and `coords` without destroying the base geometry it is computing from. It is raised
in `resize.responsive_resize` and lowered in `resize.reset_videoresize` at the end of
`pgmenu.update`.

---

## 3.7 Mixin dispatch

```python
def _init_mixins(self, **kwargs):
    for cls in type(self).__mro__[1:]:
        init = getattr(cls, "_mixin_init", None)
        if init:
            init(self, **kwargs)
```

Called as the very first statement of `Widget.__init__`, so mixin attributes exist before the
widget body runs. Note two properties:

* `self.type` must be assigned **before** `super().__init__()` in a widget's `__init__`,
  because mixins resolve theme keys of the form `{type}_{attribute}`.
* `getattr` follows inheritance, so a mixin that subclasses another mixin will cause the
  parent's `_mixin_init` to be invoked more than once. Keep mixins flat.

The `__setattr__` hook uses `cls.__dict__.get("_mixin_setattr_hook")` instead of `getattr`,
which correctly avoids the duplicate-invocation problem for hooks.

---

## 3.8 Caching

`pgmenu.vars.cache` holds five independent `Cache` instances:

| Key | Cached artefact | Written by |
| --- | --- | --- |
| `aarect` | Finished rounded-rectangle surfaces | `AARect.create_rect` |
| `aarect_corner` | Single antialiased corner masks | `AARect.aa_corners` |
| `text` | Rendered text surfaces and fitted font sizes | `text.render`, `text.fit_size` |
| `surface` | Smoothscaled surfaces | `surface.resize` |
| `rect` | Layout results | `rect.fit_rects`, `rect.center_rects` |

`Cache` subclasses `OrderedDict` and overrides `_normalize` so that any `AnimateType` inside
a tuple key is replaced by its current `.value`. Without this, an animated size would be an
unhashable, ever-changing key and nothing would ever hit.

`lru_get` moves a hit to the end; `lru_set` inserts and evicts the least recently used entry
once the cache exceeds `pgmenu.system.max_cache_size` (default 300, applied *per cache*).

Cache-friendliness is why `Animate` has a `precision` argument. Rounding the animated value
to a fixed number of decimals collapses thousands of near-identical keys into a handful.
`animation_precision` defaults to `0` in `DEFAULT.json`, meaning animated values are rounded
to whole numbers.

Both `text.render` and `AARect.aarect` return `surface.copy()`, so callers can mutate what
they receive without corrupting the cached original.

> `pgmenu.cache.clear_cache()` is currently broken; see
> [Known issues](13-known-issues.md#k4-clear_cache-iterates-the-wrong-thing).

---

## 3.9 Cursor arbitration

Three variables cooperate:

| Variable | Set by | Lifetime |
| --- | --- | --- |
| `vars.widget_cursor` | `widget.request_cursor()` during update | One frame |
| `vars.user_cursor` | `pgmenu.request_cursor(cursor)` | One frame |
| Applied cursor | End of `pgmenu.update` | Until next frame |

The user request wins if present. Both are reset at the end of every update, so a widget must
re-request its cursor on every frame it wants it, which happens naturally because
`request_cursor()` is called from the hover branch.

`Button` and `Checkbox` implement `request_cursor` as
`pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_HAND`.

---

## 3.10 Frame lifecycle in full

```
construction
    Frame(master, coords, size, fill, width, border_radius, **kwargs)
    -> Widget.__init__ (mixins, animation attrs, callbacks, responsive flags)
    -> attributes resolved from theme frame_*
    -> widgets = [] ; _widgets_to_blit = {}
    -> widget.add(self)

child construction
    Label(frame, ...) -> Widget.__setattr__("master", frame) -> frame.add(label)

per frame
    child.draw()  -> frame.blit(child_surface, child_coords)   [queued]
    frame.draw()  -> aarect surface
                  -> blit queued surfaces in insertion order
                  -> master.blit(self.surface, self.coords)
                  -> _widgets_to_blit.clear()
    child.update(event) -> _update_rect offsets by frame.coords, clips to frame.size

resize
    responsive_resize(frame, VIDEORESIZE) -> frame.resize(w, h)
        -> _resize_border_radii(w, h)  (radii scale with the smaller axis factor)
        -> size = w, h
    responsive_resize(child, VIDEORESIZE) uses frame.size / frame.base_size as reference
```

Because `_widgets_to_blit` is keyed by surface object, a child that blits the same surface
object twice in one frame only appears once, at the last position given.
