# 13. Known issues and roadmap

Everything in this chapter is a description of current behaviour, not a request. Proposed
fixes are collected with more context in [REVIEW.md](../REVIEW.md). 

---

## Sharp edges (working as written, easy to trip over)

### S1. One-frame lag in measurement

`Widget.update` measures `surface_size` *after* drawing, so hit rects and `Label` centring use
the previous frame's metrics. Visible when text or size changes abruptly.

### S2. Actions fire per event, not per transition

`Button.update` runs once per event in the queue. Holding the mouse button down over a button
during a busy frame fires `on_hold` several times. `on_hover` and `on_standby` fire once per
frame while the condition holds, not only on entry and exit. The source carries a TODO about
rate-limiting these.

### S3. `ACTIVE` is sticky across a drag-out

Pressing a button, dragging off it and releasing still fires `on_release`, because nothing
clears `ACTIVE` except the button's own mouse-up branch.

### S4. `pgmenu.update` mutates the caller's event list

When the queue is empty, a dummy `pygame.event.Event(123)` is appended to the list you passed
in. Reusing that list afterwards exposes an event with an arbitrary type number.

### S5. Colour animation can exceed the valid range

Automatic wrapping multiplies each component by `animation_scale`, with no clamping to
`0..255`. See [Animation 5.8](05-animation.md#the-colour-argument-problem) for the workaround.

### S6. No widget removal API

Widgets live in `vars.widgets` and `vars.widgets_draw_order` for the lifetime of the process.
`Frame.remove` only detaches from the frame's own list. Use `state = pgmenu.HIDDEN` to
neutralise a widget.

### S7. `pgmenu.vars.Theme` is always `None`

`lib.init` assigns to `pgmenu.Theme` (the package attribute). `pgmenu.vars.Theme`, which
`__init__.py` also imports, remains `None`. Always use `pgmenu.Theme`.

### S8. Mixed use of animated tuples in blit calls

`Button.draw` uses `self.size.int_tuple` and `self.coords.int_tuple`; `Frame.draw` and
`Surface.draw` pass the `AnimateTuple` itself. Both work, but the integer form is the
intended one and avoids sub-pixel positioning surprises.

### S9. `Label.resize` ignores the width

Only the height drives the font size, so a label inside a `STRETCH`-width container can
overflow horizontally. Fit the text with `pgmenu.text.fit_size` if that matters.

### S10. Theme loading is additive and cannot be undone

`Theme.load` never clears. A key set by a previous theme survives unless the new theme
declares it. Reload `DEFAULT` first to get a clean base.

### S11. `Theme.set` assumes well-formed special types

Any dict value is treated as a special type and `value['type']` is read without a guard, so a
plain nested object in a theme file raises `KeyError`.

### S12. `save_all` serialises non-JSON values

`vars(self)` includes function objects and loaded surfaces, which `json.dump` cannot encode.

### S13. `AnimateSurface` sizing uses a lexicographic max

`max(base.get_size(), final.get_size())` compares tuples, not axes. `(100, 10)` beats
`(90, 400)`. Give both layers identical dimensions.

### S14. `Animate.__getattr__` masks attribute errors

Unknown attributes are forwarded to `float(self.num)`, so a typo may silently resolve to a
float method. The source already contains the stricter alternative, commented out.

### S15. Cache keys are only normalised one level deep

`Cache._normalize` replaces `AnimateType` elements of a top-level tuple key. Animation objects
nested inside a sub-tuple are not normalised and would make the key unhashable or unstable.
Current call sites are all flat, so this is latent rather than active.

### S16. Known rendering artifact

Corner artifacts can appear where an outline meets the inner overlay, acknowledged by a TODO
in `aarect.py`. Reducing `aa_strength` or drawing a filled shape with a separate outline
avoids it.

---

## Incomplete or missing

| Item | State |
| --- | --- |
| `Checkbox` | Constructor done; `draw`, `update`, `check`, `uncheck`, `toggle`, `is_checked` are stubs; not imported by `__init__.py`; most `checkbox_*` theme keys undefined |
| `RadioButton` | Constant and `widget_types` entry only |
| `draw.gradient` | Stub |
| `position.place` | Stub |
| `projects.modern_ui` | Stub |
| `MODERN` theme | Keys are unprefixed and therefore unread; asset paths are relative |
| Keyboard hooks | `on_key_*` and `animation_on_key_*` exist but no widget dispatches them |
| Text input, sliders, dropdowns, scroll areas, tooltips | Not present |
| Frame clipping of drawn content | Only hit rects are clipped |
| Layout managers | Manual positioning only; `place()`/`grid()` noted as a TODO |
| Light and dark mode | TODO in `theme.py` |
| `AnimateEvent` | Noted in `lib.py` as a way to avoid `lambda: func(widget)` in animation hooks |

---

## Roadmap suggestions

Ordered by the ratio of value to effort, based on the current state of the code.

1. **Fix K1, K3, K4, K7, K9.** Five small edits that between them restore cross-platform
   import, container draw order, cache clearing, global theme attributes, and silence stdout.
2. **Finish `Checkbox`**, then generalise it into `RadioButton`. The `check_*` attribute
   family it introduces is the pattern every future multi-part widget will copy, so it is
   worth getting right before there are five copies of it.
3. **Add a widget removal API** (`pgmenu.widget.remove(widget)` clearing both registries),
   which `Menu` and any future dynamic UI needs.
4. **Introduce an event or transition layer** so `on_hover` and `on_press` fire on
   transitions, with `on_hold` rate-limited to once per frame. This addresses S2 and the
   existing TODO.
5. **Replace the `temp_*` block in `AARect` with a dataclass**, as the in-source FIXME
   suggests. It would make the three passes explicit instead of implicit shared state.
6. **A layout helper** (`position.place`, or a simple anchor and grid system) is the largest
   remaining usability gap for building real menus.
7. **Text input**, which is the widget most often needed after buttons and checkboxes.
