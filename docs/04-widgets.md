# 4. Widgets

---

## 4.1 Widget states

Every widget carries a `state` attribute holding one of five constants.

| Constant | Value | Drawn | Updated | Meaning |
| --- | --- | --- | --- | --- |
| `pgmenu.NORMAL` | `"normal"` | yes | yes | Default resting state |
| `pgmenu.HOVERED` | `"hovered"` | yes | yes | Cursor is over the widget's rect |
| `pgmenu.ACTIVE` | `"active"` | yes | yes | Widget has taken control, set by its own `update()` |
| `pgmenu.DISABLED` | `"disabled"` | yes | no | Rendered but inert |
| `pgmenu.HIDDEN` | `"hidden"` | no | no | Not rendered and not updated |

State transitions are driven by `pgmenu.update()`:

* Mouse inside `widget.rect` and state is not `ACTIVE`: set `HOVERED`, call `on_hover()` and
  `animation_on_hover()`, call `request_cursor()`.
* Mouse outside and state is not `ACTIVE`: set `NORMAL`, call `on_standby()` and
  `animation_on_standby()`.
* `ACTIVE` is never cleared by the engine. The widget itself must leave it (`Button` returns
  to `NORMAL` on mouse button up).

The hover and standby hooks fire **every frame** the condition holds, not only on the
transition. Animation objects are written to tolerate this: calling `update(FORWARD)` on an
already-finished animation is a cheap no-op because of its `done` flag.

Setting a state directly is allowed and is the intended way to disable a control:

```python
button.state = pgmenu.DISABLED
```

---

## 4.2 The `Widget` base class

`pgmenu.widget.Widget` is the base every widget inherits. It provides the animation
machinery, the callback table, responsive flags, geometry bookkeeping and the default
`draw`/`update`/`resize` behaviour.

### Constructor

```python
Widget(**kwargs)
```

`Widget` takes no positional arguments. Subclasses declare their own signature and forward
the remaining keyword arguments with `super().__init__(**kwargs)`.

`self.type` must be set **before** calling `super().__init__()`. It defaults to
`pgmenu.WIDGET` if absent, and it is the prefix used for every per-widget theme lookup.

### Attributes set by `Widget.__init__`

| Attribute | Default source | Notes |
| --- | --- | --- |
| `type` | `self.type` or `pgmenu.WIDGET` | Widget kind constant |
| `animation_scale` | `{type}_animation_scale`, else `widget_animation_scale` (1.2) | Final value multiplier |
| `animation_duration` | `{type}_animation_duration`, else `widget_animation_duration` (0.15) | Seconds |
| `animation_curve` | `{type}_animation_curve`, else `widget_animation_curve` (`circ`) | Easing function |
| `disable_animation` | `{type}_disable_animation`, else `widget_disable_animation` (False) | Checked by the built-in `m_animation_*` hooks |
| `animation_on_standby` ... `animation_on_key_release` | theme, else the matching `m_animation_on_*` bound method | See 4.4 |
| `on_standby` ... `on_resize` | theme, else the matching `m_on_*` bound method | See 4.4 |
| `responsive_size` | `widget_responsive_size` (`PROPORTIONAL`) | `PROPORTIONAL`, `STRETCH`, or falsy to disable |
| `responsive_size_w` / `responsive_size_h` | `True` / `True` | Per-axis size scaling |
| `responsive_coords` | `widget_responsive_coords` (`STRETCH`) | Same value space as `responsive_size` |
| `responsive_coords_x` / `responsive_coords_y` | `True` / `True` | Per-axis coordinate scaling |
| `state` | `widget_state` (`NORMAL`) | See 4.1 |
| `rect` | `pygame.Rect(0, 0, 0, 0)` | Hit-test rect, recomputed in `update()` |
| `size` | `(0, 0)` | Overwritten by the subclass |
| `coords` | `(0, 0)` | Overwritten by the subclass |
| `surface` | empty `SRCALPHA` surface | Rebuilt each `draw()` |
| `surface_size` | `(0, 0)` | Measured in `update()` |
| `base_size` / `base_coords` | `None` | Mirrors of user-assigned geometry |
| `has_draw_priority` | `False` | Opt-in to top-tier drawing |
| `_drawn` | `False` | Per-frame flag, gates the update pass |

Note the difference in resolution style: the animation and callback attributes go through
`resolve_widget` (theme-aware with a per-type key), while the responsive and state attributes
use a plain `kwargs.get(...)` with the global theme value. Responsive behaviour is therefore
uniform across widget types by design.

### Methods

| Method | Purpose |
| --- | --- |
| `get_*()` | One accessor per public attribute; all are trivial getters |
| `__setattr__(key, value)` | The animation/base-tracking/validation pipeline of [3.6](03-architecture.md#36-the-attribute-pipeline) |
| `_update_rect(size, coords)` | Recomputes `self.rect`, converting frame-relative coordinates and clipping to the frame |
| `_init_mixins(**kwargs)` | Calls `_mixin_init` on every class in the MRO that defines one |
| `_make_2d(value)` | Turns a scalar (or an `AnimateType`) into a 2-tuple |
| `_get_2d(key)` | `_make_2d` applied to an attribute, or `None` if absent |
| `get_2d_size()` / `get_2d_base_size()` | Normalised current/base size for resize maths |
| `modify(**kwargs)` | Assign several attributes in one call |
| `draw()` | Sets `_drawn = True`; subclasses call it first |
| `update(event)` | Measures `surface_size` and refreshes `rect` |
| `resize(w, h)` | No-op; subclasses implement the responsive contract |
| `m_animation_on_*` / `m_on_*` | Default no-op hook implementations |
| `request_cursor()` | No-op; override to claim a cursor while hovered |

### `modify`

```python
button.modify(size=(140, 40), text="Continue", fill=(200, 60, 60))
```

Equivalent to three assignments, each of which goes through `__setattr__` and therefore
through the animation pipeline.

---

## 4.3 Mixins

### `RectMixin`

Adds the rounded-rectangle attribute family to a widget. Inherited by `Frame`, `Button` and
`Checkbox`.

| Attribute | Theme key | Default |
| --- | --- | --- |
| `border_radius` | `{type}_border_radius` | Set by the widget, usually a fraction of its size |
| `border_top_left_radius` | `{type}_border_top_left_radius` | `None`, falls back to `border_radius` |
| `border_top_right_radius` | `{type}_border_top_right_radius` | `None` |
| `border_bottom_left_radius` | `{type}_border_bottom_left_radius` | `None` |
| `border_bottom_right_radius` | `{type}_border_bottom_right_radius` | `None` |
| `antialiasing` | `{type}_antialiasing`, else `rectmixin_antialiasing` | `True` |
| `transparency` | `{type}_transparency`, else `rectmixin_transparency` | `255` |
| `aa_strength` | `{type}_aa_strength`, else `rectmixin_aa_strength` | `1` |
| `inner_fill` | `{type}_inner_fill` | `pgmenu.UNSET` |
| `inner_transparency` | `{type}_inner_transparency` | `pgmenu.UNSET` |
| `inner_aa_strength` | `{type}_inner_aa_strength` | `pgmenu.UNSET` |
| `inner_antialiasing` | `{type}_inner_antialiasing` | `pgmenu.UNSET` |

The `UNSET` defaults are deliberate. `UNSET` is ignored by `resolve`, so passing these
straight through to `pgmenu.draw.aarect` lets the drawing layer apply its own defaults
(`inner_fill` falls back to `fill`, `inner_transparency` to `transparency`, and so on).

It also maintains `base_border_*_radius` mirrors through `_mixin_setattr_hook`, and provides:

* `_resize_border_radii(w, h)`: rescales all five radii by
  `min(w / base_size[0], h / base_size[1])`. Every `resize()` implementation calls this
  first, before assigning the new size, because the factor depends on the *old* base size.
* `_animation_update_border_radii(direction, reach)`: forwards an animation update to every
  non-`None` radius.

### `TextMixin`

Adds the text styling family, inherited by `Button` and `Checkbox`. All values default to
`pgmenu.UNSET` so that `pgmenu.text` applies its own `text_*` theme defaults.

| Attribute | Theme key |
| --- | --- |
| `text_font` | `{type}_text_font` |
| `text_background` | `{type}_text_background` |
| `text_antialias` | `{type}_text_antialias` |
| `text_italic` | `{type}_text_italic` |
| `text_bold` | `{type}_text_bold` |
| `text_strikethrough` | `{type}_text_strikethrough` |
| `text_underline` | `{type}_text_underline` |
| `text_transparency` | `{type}_text_transparency` |

Note that `text` itself and `text_color` are *not* part of the mixin; they are declared by
the widget, because they are semantic content rather than styling.

---

## 4.4 Callbacks

Two parallel families exist. They are called at the same moments; the split is a convention
that keeps visual behaviour separable from application logic.

| Action hook | Animation hook | Fired when |
| --- | --- | --- |
| `on_standby` | `animation_on_standby` | Every frame the cursor is not over the widget and it is not `ACTIVE` |
| `on_hover` | `animation_on_hover` | Every frame the cursor is over the widget and it is not `ACTIVE` |
| `on_press` | `animation_on_press` | Mouse button down on the widget (`Button`) |
| `on_hold` | `animation_on_hold` | Mouse button held on the widget (`Button`) |
| `on_release` | `animation_on_release` | Mouse button up on the widget (`Button`) |
| `on_key_press` | `animation_on_key_press` | Reserved, not yet emitted by any widget |
| `on_key_hold` | `animation_on_key_hold` | Reserved |
| `on_key_release` | `animation_on_key_release` | Reserved |
| `on_resize` | (none) | After a responsive resize has been applied |

Each defaults to the widget's bound `m_<name>` method, which is a no-op on `Widget` and is
overridden by concrete widgets to implement their stock behaviour. Three ways to change one:

```python
# 1. constructor keyword
button = pgmenu.button.Button(screen, on_release=save)

# 2. attribute assignment
button.on_release = save

# 3. theme key, applied to every widget of that type
#    "button_on_release": {"type": "method", "module": "...", "object": "...", "method": "..."}
```

Because the default is a *bound method of that widget*, an overriding function receives no
arguments and must close over the widget it targets:

```python
def grow():
    label.color.update(pgmenu.FORWARD)

label = pgmenu.label.Label(screen, animation_on_hover=grow)
```

The keyboard hooks are declared with a `key` parameter on `Widget` (`m_on_key_press(self, key)`)
in anticipation of keyboard-driven widgets. No widget dispatches them yet.

---

## 4.5 `Label`

```python
pgmenu.label.Label(master, coords=THEME, text=THEME, color=THEME, size=THEME,
                   font=THEME, background=THEME, antialias=THEME, italic=THEME,
                   bold=THEME, strikethrough=THEME, underline=THEME,
                   transparency=THEME, center_x=THEME, center_y=THEME, **kwargs)
```

Renders a line (or several, `\n` is supported) of text.

| Parameter | Theme key | Default | Notes |
| --- | --- | --- | --- |
| `master` | none | required | Display surface or `Frame` |
| `coords` | `label_coords` | `(20, 20)` | Top-left, or centre anchor when centring is on |
| `text` | `label_text` | `"Label"` | `\n` produces multiple lines |
| `color` | `label_color` | `(255, 255, 255)` | Becomes an `AnimateTuple` |
| `size` | `label_size` | `20` | Font point size; becomes an `Animate` |
| `font` | `label_font` | `None` | Path or system font name; `None` uses the bundled VarelaRound |
| `background` | `label_background` | `None` | Solid background colour behind the glyphs |
| `antialias` | `label_antialias` | `True` | |
| `italic` / `bold` / `strikethrough` / `underline` | `label_*` | `False` | |
| `transparency` | `label_transparency` | `255` | Surface alpha |
| `center_x` / `center_y` | `label_center_x` / `label_center_y` | `False` | Treat `coords` as a centre |

**Behaviour**

* `draw()` renders through `pgmenu.text.render` (cached) and assigns the result to
  `self.surface`. Because `Label.type != pgmenu.SURFACE`, `__setattr__` does *not* wrap it in
  an `AnimateSurface`.
* When centring is enabled it uses `self.surface_size`, which is measured during the previous
  `update()`. The first frame of a text change is therefore positioned with the previous
  text's metrics.
* `resize(w, h)` sets `self.size = h`. A label's responsive size is its font size, driven by
  the vertical factor.
* `size` is a scalar, so `get_2d_base_size()` returns `(size, size)` and the responsive maths
  treats it as a square.
* `Label` has no `update()` override and no `request_cursor()`; it uses `Widget`'s.

**Animating a label's colour**

Colour attributes are scaled by `animation_scale` like everything else, which can push
components past 255 and does not let you choose the destination colour. Declare the
animation explicitly instead:

```python
color = pgmenu.animation.AnimateTuple((250, 50), (50, 50), (50, 250),
                                      duration=0.5,
                                      curve=pgmenu.animation.circ)
label = pgmenu.label.Label(screen, (250, 150), color=color, size=100)
```

See [Animation](05-animation.md#57-the-colour-argument-problem).

---

## 4.6 `Surface`

```python
pgmenu.surface.Surface(master, surface, coords=THEME, **kwargs)
```

Wraps an arbitrary `pygame.Surface` as a widget so it participates in hit testing,
callbacks, animation and responsive resizing.

| Parameter | Theme key | Default | Notes |
| --- | --- | --- | --- |
| `master` | none | required | |
| `surface` | none | required | `pygame.Surface` or `AnimateSurface` |
| `coords` | `surface_coords` | `(20, 20)` | |

**Behaviour**

* `Surface` is the **only** widget whose `surface` attribute is animated by `__setattr__`.
  Assigning a plain `pygame.Surface` produces an `AnimateSurface` that cross-fades to a
  brightened copy of itself, giving a free hover highlight.
* `_surface` is a shadow attribute holding the last surface assigned by the user.
  `__setattr__` keeps it in sync. `resize()` scales `_surface` rather than the already-scaled
  `surface`, so repeated resizes do not compound quality loss:

  ```python
  def resize(self, w, h):
      self.size = w, h
      original_surface = self._surface
      self.surface = resize(self._surface, self.size)
      self._surface = original_surface
  ```

* `update(event)` refreshes `self.size` from the current surface each frame.
* `size` is derived, never declared.

**Keeping animations across a resize.** The default resize path replaces `surface` with a
`smoothscale` result, which discards any `AnimateSurface` you supplied. For crisper results
and to keep the animation, rebuild the surface yourself in `on_resize`:

```python
def make_animated_surface(size):
    base  = pgmenu.draw.aarect(None, (63, 68, 72), (0, 0, *size))
    hover = pgmenu.draw.aarect(None, (68, 72, 77), (0, 0, *size))
    return pgmenu.animation.AnimateSurface(base, hover, 0, 255, 0.3,
                                           pgmenu.animation.circ)


def on_resize():
    widget.surface = make_animated_surface(widget.size)


widget = pgmenu.surface.Surface(frame, make_animated_surface((200, 100)), (10, 150),
                                on_resize=on_resize)
```

`on_resize` is called by the responsive system immediately after `resize(w, h)`, so
`widget.size` already holds the new size when it runs.

---

## 4.7 `Frame`

```python
pgmenu.frame.Frame(master, coords=THEME, size=THEME, fill=THEME,
                   width=THEME, border_radius=THEME, **kwargs)
```

A container: an antialiased rounded rectangle that other widgets draw into.

| Parameter | Theme key | Default | Notes |
| --- | --- | --- | --- |
| `master` | none | required | Display surface or another `Frame` |
| `coords` | `frame_coords` | `(20, 20)` | |
| `size` | `frame_size` | `(200, 200)` | |
| `fill` | `frame_fill` | `(47, 51, 54)` | Colour, animated tuple, or a `pygame.Surface` |
| `width` | `frame_width` | `0` | Outline width; `0` means filled |
| `border_radius` | `frame_border_radius` | `null`, falls back to `round(min(size) / 7)` | |

Plus every `RectMixin` attribute.

**Extra attributes**

| Attribute | Purpose |
| --- | --- |
| `widgets` | Children that named this frame as master |
| `_widgets_to_blit` | Per-frame queue of `{surface: coords}` filled by children |

**Methods**

| Method | Purpose |
| --- | --- |
| `add(*widgets)` | Register children (called automatically by `Widget.__setattr__`) |
| `remove(*widgets)` | Unregister children |
| `blit(surface, coords)` | Queue a child surface; the frame is a blit target, not a real surface |
| `draw()` | Render the rectangle, flush the queue, blit onto the master, clear the queue |
| `resize(w, h)` | `_resize_border_radii(w, h)` then set `size` |

**Notes**

* Children use frame-relative coordinates.
* A child's hit rect is clipped to the frame, so overflow is not clickable.
* `Frame.draw` currently passes `debug=True` down to `pgmenu.draw.aarect`, which prints a
  timing line whenever the rectangle is regenerated. See
  [Known issues](13-known-issues.md#k5-frame-draws-with-debug-on).
* Frames have no scrolling, clipping of drawn content (only of hit rects), or automatic
  layout. Children are positioned manually.

---

## 4.8 `Button`

```python
pgmenu.button.Button(master, coords=THEME, size=THEME, fill=THEME, text=THEME,
                     text_color=THEME, icon=THEME, margin=THEME, width=THEME,
                     border_radius=THEME, **kwargs)
```

The reference widget: rounded rectangle, auto-fitted label, optional icon, hover growth,
press feedback and a hand cursor.

| Parameter | Theme key | Default | Notes |
| --- | --- | --- | --- |
| `master` | none | required | |
| `coords` | `button_coords` | `(20, 20)` | |
| `size` | `button_size` | `(100, 30)` | |
| `fill` | `button_fill` | `(42, 120, 205)` | Colour, animated tuple, or `pygame.Surface` |
| `text` | `button_text` | `"Button"` | |
| `text_color` | `button_text_color` | `(255, 255, 255)` | |
| `icon` | `button_icon` | `None` | A `pygame.Surface`, drawn left of the text |
| `margin` | `button_margin` | `3` | Inner padding used by the text/icon fit |
| `width` | `button_width` | `0` | Outline width |
| `border_radius` | `button_border_radius` | `null`, falls back to `round(min(size) / 3)` | |

Plus every `RectMixin` and `TextMixin` attribute.

**Draw pipeline**

1. Centre the animated size inside the base rect, so growth expands around the centre rather
   than the top-left:
   `coords = position.center_coords(size.int_tuple, (*coords.int_tuple, *size.base_tuple))`
2. Build the background with `pgmenu.draw.aarect(None, ...)` (surface `None` means "return
   the surface, do not blit").
3. Fit the text with `pgmenu.text.fit_render_animated`, which renders once at the button's
   *final* size and smoothscales to the current animated size. This is what keeps text
   scaling smooth rather than jumping from one font size to the next.
4. If an icon is set, split the interior with `pgmenu.rect.fit_rects`, scale the icon with
   `pgmenu.surface.resize`, and centre the icon/text pair with `pgmenu.rect.center_rects`.
5. Blit the text, then blit the whole button onto the master.

**Update**

Only while `HOVERED` or `ACTIVE`:

| Event | Effect |
| --- | --- |
| `MOUSEBUTTONDOWN` (left) | `state = ACTIVE`, `on_press()`, `animation_on_press()` |
| `MOUSEBUTTONUP` (left) | `state = NORMAL`, `on_release()`, `animation_on_release()` |
| left button held | `on_hold()`, `animation_on_hold()` |

Because `ACTIVE` is sticky, a press followed by dragging off the button and releasing still
fires `on_release`. This is intentional for keyboard-free UIs but differs from the common
desktop convention.

**Stock animation hooks**

| Hook | Effect |
| --- | --- |
| `m_animation_on_standby` | `size`, `fill` and radii run backwards |
| `m_animation_on_hover` | `size`, `fill` and radii run forwards |
| `m_animation_on_hold` | `size` and radii run backwards with `reach = 0.15`, producing a small press-in |
| `m_on_release` | Prints `"Button pressed"` (placeholder, override it) |

All three animation hooks check `self.disable_animation` first, so
`Button(..., disable_animation=True)` gives a completely static button.

**`resize(w, h)`**: `_resize_border_radii(w, h)` then `size = w, h`.

**`request_cursor()`**: hand cursor.

---

## 4.9 `Checkbox` (in development)

```python
pgmenu.checkbox.Checkbox(master, coords=THEME, size=THEME, fill=THEME, text=THEME,
                         text_color=THEME, check_fill=THEME, margin=THEME,
                         width=THEME, border_radius=THEME, checked=THEME, **kwargs)
```

The constructor, attribute resolution, size normalisation and cursor are implemented.
`draw`, `update`, `is_checked`, `check`, `uncheck` and `toggle` are stubs, and the module is
**not imported** by `pgmenu/__init__.py`, so `pgmenu.checkbox` does not exist until you
uncomment that line.

Design decisions already committed to in the source:

* `size` accepts a scalar and is normalised to a square by `_format_size`, including when an
  `Animate` is passed.
* The check mark gets its own `check_*` styling family (`check_fill`, `check_antialiasing`,
  `check_transparency`, `check_aa_strength`, `check_inner_*`), resolved via `resolve_widget`
  against `checkbox_*` theme keys with `rectmixin_*` fallbacks. This is the template for any
  widget that draws more than one rectangle.
* `check_border_radius` is deliberately omitted for now.
* Only `checkbox_fill` is defined in `DEFAULT.json`; the remaining `checkbox_*` keys still
  need to be added before the widget can be used.

`RADIOBUTTON` exists only as a constant in `constants.py` and an entry in
`vars.widget_types`; there is no module.

---

## 4.10 Attribute cheat sheet

| Attribute | Label | Surface | Frame | Button | Checkbox |
| --- | :---: | :---: | :---: | :---: | :---: |
| `master` | yes | yes | yes | yes | yes |
| `coords` | yes | yes | yes | yes | yes |
| `size` | font size | derived | yes | yes | square |
| `fill` | no | no | yes | yes | yes |
| `text` / `text_color` | `text` / `color` | no | no | yes | yes |
| `icon` | no | no | no | yes | no |
| `margin` | no | no | no | yes | yes |
| `width` | no | no | yes | yes | yes |
| `RectMixin` family | no | no | yes | yes | yes |
| `TextMixin` family | no | no | no | yes | yes |
| `center_x` / `center_y` | yes | no | no | no | no |
| Hand cursor | no | no | no | yes | yes |
