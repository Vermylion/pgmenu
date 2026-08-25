# 12. API reference

Exhaustive listing of every public name in the package. `THEME` denotes `pgmenu.THEME`.

Names re-exported at package level: everything in `constants.py` and `lib.py`, plus each
submodule as an attribute (`pgmenu.text`, `pgmenu.draw`, `pgmenu.button`, ...), plus
`pgmenu.Theme` (the live theme instance).

---

## 12.1 `pgmenu` (package level)

| Name | Kind | Description |
| --- | --- | --- |
| `Theme` | instance | The live `pgmenu.theme.Theme`, created and loaded by `lib.init()` |
| `draw_all()` | function | Draw every registered widget |
| `update(events)` | function | Run the full update pass |
| `request_cursor(cursor)` | function | Claim the cursor for this frame; `None` releases |
| `init()` | function | Build and load the theme, set the starting cursor. Runs on import |
| All constants | str | See 12.2 |

---

## 12.2 `pgmenu.constants`

| Group | Constants |
| --- | --- |
| States | `NORMAL`, `HOVERED`, `ACTIVE`, `DISABLED`, `HIDDEN` |
| Animation directions | `FORWARD`, `BACKWARD` |
| Curve directions | `IN`, `OUT`, `IN_OUT` |
| Widget types | `WIDGET`, `LABEL`, `SURFACE`, `FRAME`, `BUTTON`, `CHECKBOX`, `RADIOBUTTON` |
| Sentinels | `THEME`, `UNSET` |
| Responsive modes | `PROPORTIONAL`, `STRETCH` |

Each constant's value is its lowercase name (`NORMAL == "normal"`).

---

## 12.3 `pgmenu.vars`

Module-level mutable state. See [9.6](09-menus-and-utilities.md#96-pgmenuvars) for the table.

`widgets`, `widgets_draw_order`, `widget_types`, `cache`, `Theme`, `widget_cursor`,
`user_cursor`, `base_window_size`, `videoresized`, `fs_window_size`, `mouse_x`, `mouse_y`,
`current_menu_showed`.

---

## 12.4 `pgmenu.system`

| Name | Type | Default |
| --- | --- | --- |
| `widget_draw_priority` | bool | `True` |
| `max_cache_size` | int | `300` |

---

## 12.5 `pgmenu.cache`

| Name | Signature | Description |
| --- | --- | --- |
| `Cache` | `class Cache(OrderedDict)` | Dict whose tuple keys have `AnimateType` elements replaced by their current value |
| `Cache._normalize` | `(self, key)` | Returns the normalised key; non-tuple keys pass through |
| `Cache.__setitem__` | `(self, key, value)` | Normalising insert |
| `Cache.__getitem__` | `(self, key)` | Normalising lookup |
| `Cache.__contains__` | `(self, key)` | Normalising membership test |
| `Cache.get` | `(self, key, default=None)` | Normalising `get` |
| `Cache.move_to_end` | `(self, key, last=True)` | Normalising `move_to_end` |
| `lru_get` | `(cache, key)` | Value and recency bump, or `None` |
| `lru_set` | `(cache, key, value)` | Insert and evict past `system.max_cache_size` |
| `clear_cache` | `()` | Intended to clear all caches (currently broken, see K4) |

---

## 12.6 `pgmenu.utils`

| Name | Signature | Description |
| --- | --- | --- |
| `sub_values` | `dict[int, int]` | Desired subtracted alpha to the alpha that must be written |
| `only_alpha_blending` | `(source_alpha, dest_alpha)` | Alpha-only blend result |
| `div` | `(a, b, round_num=None)` | Division returning `float('inf')` on divide by zero |

---

## 12.7 `pgmenu.theme`

| Name | Signature | Description |
| --- | --- | --- |
| `Theme` | `class Theme` | Attribute bag holding every default |
| `Theme.set` | `(self, **attrs)` | Apply an attribute map, handling `"#"`, special types and list conversion |
| `Theme.save` | `(self, theme, **attrs)` | Write the given attributes to `themes/<theme>.json` |
| `Theme.save_all` | `(self, theme)` | Write every attribute currently held |
| `Theme.load` | `(self, theme="DEFAULT")` | Read and apply a theme file |
| `_format_theme_path` | `(theme)` | `(name, absolute_path)` for a theme name with or without extension |
| `resolve` | `(value, theme_attr, default=None)` | Sentinel resolution |
| `resolve_kwarg` | `(kwargs, key, theme_attr, default=None)` | `resolve` sourcing from `kwargs` |
| `resolve_widget` | `(kwargs, key, widget_type, default=None)` | `resolve_kwarg` against `{widget_type}_{key}` |

---

## 12.8 `pgmenu.animation`

### Easing functions

| Family (`(x, direction)`) | Concrete (`(x)`) |
| --- | --- |
| `linear(x, direction=None)` | none |
| `sine` | `ease_in_sine`, `ease_out_sine`, `ease_in_out_sine` |
| `quad` | `ease_in_quad`, `ease_out_quad`, `ease_in_out_quad` |
| `cubic` | `ease_in_cubic`, `ease_out_cubic`, `ease_in_out_cubic` |
| `quart` | `ease_in_quart`, `ease_out_quart`, `ease_in_out_quart` |
| `quint` | `ease_in_quint`, `ease_out_quint`, `ease_in_out_quint` |
| `expo` | `ease_in_expo`, `ease_out_expo`, `ease_in_out_expo` |
| `circ` | `ease_in_circ`, `ease_out_circ`, `ease_in_out_circ` |
| `back` | `ease_in_back`, `ease_out_back`, `ease_in_out_back` |
| `elastic` | `ease_in_elastic`, `ease_out_elastic`, `ease_in_out_elastic` |
| `bounce` | `ease_in_bounce`, `ease_out_bounce`, `ease_in_out_bounce` |

### `AnimateType`

Abstract base. Properties `value`, `base_value`, `final_value`; methods `init()`, `reset()`,
`update(direction=FORWARD, reach=1)`.

### `Animate(base_num, final_num, duration=THEME, curve=THEME, precision=THEME)`

| Member | Kind | Description |
| --- | --- | --- |
| `base_num`, `final_num` | attr | Endpoints |
| `duration` | attr | Seconds, clamped to at least `sys.float_info.epsilon` |
| `curve` | attr | Easing callable |
| `precision` | attr | Decimal places for rounding, or `None` |
| `start_time` | attr | Timestamp of the current run |
| `diff_num` | attr | `final_num - base_num` |
| `num` | attr | Current value |
| `step` | attr | Current normalised progress |
| `last_step` | attr | Step at the moment of the last forward-to-backward switch |
| `direction`, `reach`, `curve_direction`, `done` | attr | Current run state |
| `value`, `int`, `float`, `base_value`, `final_value` | property | Value views |
| `__int__`, `__float__`, `__round__`, `__index__`, `__repr__` | dunder | Numeric conversions |
| `__eq__`, `__lt__` plus `total_ordering` | dunder | Comparisons against numbers or other animations |
| `__add__`/`__radd__`, `__sub__`/`__rsub__`, `__mul__`/`__rmul__`, `__truediv__`/`__rtruediv__`, `__floordiv__`/`__rfloordiv__`, `__mod__`/`__rmod__` | dunder | Arithmetic returning plain numbers |
| `__hash__` | dunder | Identity based |
| `__getattr__` | dunder | Forwards unknown attributes to `float(self.num)` |
| `_coerce(other)` | method | Unwrap an `AnimateType` for comparison |
| `init()`, `reset()`, `update(direction=FORWARD, reach=1)` | method | Animation control |

### `AnimateTuple(*pairs, duration=THEME, curve=THEME, precision=THEME)`

| Member | Kind | Description |
| --- | --- | --- |
| `items` | attr | The component `Animate` objects |
| `base_tuple`, `final_tuple`, `int_tuple`, `float_tuple` | attr | Derived tuples kept in sync by `update` |
| `duration`, `curve`, `precision` | attr | Construction parameters |
| `value`, `tuple`, `base_value`, `final_value` | property | Value views |
| `__len__`, `__iter__`, `__getitem__`, `__repr__`, `__hash__` | dunder | Tuple protocol |
| `__add__`, `__radd__` | dunder | Concatenation with plain tuples |
| `__eq__`, `__lt__` plus `total_ordering` | dunder | Comparisons |
| `init()`, `reset()`, `update(direction=FORWARD, reach=1)` | method | Forwarded to every item |

### `AnimateSurface(base_surface, final_surface, base_alpha=THEME, final_alpha=THEME, duration=THEME, curve=THEME, precision=THEME)`

Subclass of `pygame.Surface` and `AnimateType`.

| Member | Kind | Description |
| --- | --- | --- |
| `base_surface`, `final_surface` | attr | The two layers |
| `base_alpha`, `final_alpha` | attr | Alpha endpoints of the top layer |
| `duration`, `curve`, `precision` | attr | Construction parameters |
| `animation_alpha` | attr | The `Animate` driving the blend |
| `value`, `surface`, `base_value`, `final_value` | property | `self`, `self`, base, final |
| `__repr__`, `__hash__` | dunder | |
| `init()`, `reset()`, `update(direction=FORWARD, reach=1)` | method | Recomposites its own pixels |

### `AnimateMultiple(*animations)`

| Member | Kind | Description |
| --- | --- | --- |
| `animations` | attr | `{id: animation}` |
| `value`, `base_value`, `final_value` | property | Lists of member values |
| `modify(*animations)` | method | Add or replace members |
| `reset()`, `update(direction=FORWARD, reach=1)` | method | Applied to every member |

---

## 12.9 `pgmenu.widget`

### `add(widget)`

Registers a widget in `vars.widgets` and `vars.widgets_draw_order`, applying the frame
insertion rule.

### `Widget(**kwargs)`

**Attributes**: `type`, `animation_scale`, `animation_duration`, `animation_curve`,
`disable_animation`, `animation_on_standby`, `animation_on_hover`, `animation_on_press`,
`animation_on_hold`, `animation_on_release`, `animation_on_key_press`,
`animation_on_key_hold`, `animation_on_key_release`, `on_standby`, `on_hover`, `on_press`,
`on_hold`, `on_release`, `on_key_press`, `on_key_hold`, `on_key_release`, `on_resize`,
`responsive_size`, `responsive_size_w`, `responsive_size_h`, `responsive_coords`,
`responsive_coords_x`, `responsive_coords_y`, `state`, `rect`, `size`, `coords`, `surface`,
`surface_size`, `base_size`, `base_coords`, `has_draw_priority`, `_drawn`.

**Methods**

| Method | Description |
| --- | --- |
| `__setattr__(key, value)` | Animation wrapping, master validation, base tracking, mixin hooks |
| `_update_rect(size, coords)` | Recompute `rect`, offsetting and clipping inside a frame |
| `_init_mixins(**kwargs)` | Call `_mixin_init` on every MRO class that defines one |
| `_make_2d(value)` | Scalar or `AnimateType` to a 2-tuple |
| `_get_2d(key)` | `_make_2d` of an attribute, or `None` |
| `get_2d_size()` | Current size as a 2-tuple |
| `get_2d_base_size()` | Base size as a 2-tuple |
| `modify(**kwargs)` | Bulk attribute assignment |
| `draw()` | Set `_drawn` |
| `update(event)` | Measure `surface_size`, refresh `rect` |
| `resize(w, h)` | No-op |
| `m_animation_on_standby/hover/press/hold/release()` | Default no-op animation hooks |
| `m_animation_on_key_press(key)` / `m_animation_on_key_hold()` / `m_animation_on_key_release(key)` | Default no-op key animation hooks |
| `m_on_standby/hover/press/hold/release()` | Default no-op action hooks |
| `m_on_key_press(key)` / `m_on_key_hold(key)` / `m_on_key_release(key)` | Default no-op key hooks |
| `m_on_resize()` | Default no-op resize hook |
| `request_cursor()` | No-op |

### `RectMixin`

**Attributes**: `border_radius`, `border_top_left_radius`, `border_top_right_radius`,
`border_bottom_left_radius`, `border_bottom_right_radius`, `base_border_radius` and the four
`base_border_*_radius`, `antialiasing`, `transparency`, `aa_strength`, `inner_fill`,
`inner_transparency`, `inner_aa_strength`, `inner_antialiasing`. .

**Methods**

| Method | Description |
| --- | --- |
| `_mixin_init(**kwargs)` | Resolve the whole family from kwargs and theme |
| `_mixin_setattr_hook(key, value)` | Mirror radii into `base_border_*` outside a resize |
| `_resize_border_radii(w, h)` | Rescale all radii by `min(w / base_w, h / base_h)` |
| `_animation_update_border_radii(direction=FORWARD, reach=1)` | Update every non-`None` radius |

### `TextMixin`

**Attributes**: `text_font`, `text_background`, `text_antialias`, `text_italic`, `text_bold`,
`text_strikethrough`, `text_underline`, `text_transparency`, all defaulting to `UNSET`.

**Methods**: `_mixin_init(**kwargs)`.

---

## 12.10 `pgmenu.label`

```python
Label(master, coords=THEME, text=THEME, color=THEME, size=THEME, font=THEME,
      background=THEME, antialias=THEME, italic=THEME, bold=THEME,
      strikethrough=THEME, underline=THEME, transparency=THEME,
      center_x=THEME, center_y=THEME, **kwargs)
```

**Methods**: `draw()`, `resize(w, h)` (sets `size = h`).

---

## 12.11 `pgmenu.surface`

```python
Surface(master, surface, coords=THEME, **kwargs)
```

**Attributes**: `master`, `surface`, `_surface` (shadow of the last user-assigned surface),
`coords`, `size` (derived from the surface).

**Methods**: `get_master()`, `__setattr__(key, value)`, `draw()`, `resize(w, h)`,
`update(event)`.

**Module function**

```python
resize(surface, size)
```

Cached `pygame.transform.smoothscale`.

---

## 12.12 `pgmenu.frame`

```python
Frame(master, coords=THEME, size=THEME, fill=THEME, width=THEME,
      border_radius=THEME, **kwargs)
```

Inherits `Widget` and `RectMixin`.

**Attributes**: `master`, `coords`, `size`, `fill`, `width`, `border_radius`, `widgets`,
`_widgets_to_blit`.

**Methods**: `add(*widgets)`, `remove(*widgets)`, `blit(surface, coords)`, `draw()`,
`resize(w, h)`.

---

## 12.13 `pgmenu.button`

```python
Button(master, coords=THEME, size=THEME, fill=THEME, text=THEME, text_color=THEME,
       icon=THEME, margin=THEME, width=THEME, border_radius=THEME, **kwargs)
```

Inherits `Widget`, `RectMixin` and `TextMixin`.

**Methods**: `draw()`, `update(event)`, `resize(w, h)`, `m_animation_on_standby()`,
`m_animation_on_hover()`, `m_animation_on_hold()`, `m_on_release()`, `request_cursor()`.

---

## 12.14 `pgmenu.checkbox` (in development, not imported by default)

```python
Checkbox(master, coords=THEME, size=THEME, fill=THEME, text=THEME, text_color=THEME,
         check_fill=THEME, margin=THEME, width=THEME, border_radius=THEME,
         checked=THEME, **kwargs)
```

**Extra attributes**: `check_antialiasing`, `check_transparency`, `check_aa_strength`,
`check_inner_fill`, `check_inner_transparency`, `check_inner_aa_strength`,
`check_inner_antialiasing`.

**Methods**: `_format_size(size)` (implemented), `resize(w, h)` (implemented),
`request_cursor()` (implemented), `is_checked()`, `check()`, `uncheck()`, `toggle()`,
`draw()`, `update(event)` (all stubs).

---

## 12.15 `pgmenu.draw`

| Function | Signature |
| --- | --- |
| `aarect` | `(surface=None, fill=THEME, rect=THEME, width=THEME, border_radius=THEME, border_top_left_radius=THEME, border_top_right_radius=THEME, border_bottom_left_radius=THEME, border_bottom_right_radius=THEME, antialiasing=THEME, transparency=THEME, aa_strength=THEME, **kwargs)` |
| `gradient` | `(color1, color2, angle, curve)` (stub) |

Recognised `kwargs`: `inner_fill`, `inner_transparency`, `inner_aa_strength`,
`inner_antialiasing`, `debug`.

---

## 12.16 `pgmenu.aarect`

### `AARect(surface, fill, rect, width=0, border_radius=10, border_top_left_radius=None, border_top_right_radius=None, border_bottom_left_radius=None, border_bottom_right_radius=None, antialiasing=True, transparency=255, aa_strength=1, **kwargs)`

**Attributes**: the constructor arguments, plus `inner_fill`, `inner_transparency`,
`inner_aa_strength`, `inner_antialiasing`, `debug`, `force_only_overlay`, `aa_pixels`,
`aa_surface`, `object_cache_id`, the `temp_*` mirror of every visual parameter, the four
`draw_border_*_radius` flags, and `border_radius_values`.

| Method | Description |
| --- | --- |
| `aarect()` | Format, build if not cached, blit if a destination was given, return a copy |
| `format_rect()` | Validate, split alpha, scale surface fills, clamp width and radii, build the cache id |
| `create_rect()` | Compose the three passes and store the result |
| `draw_rects()` | Run up to three `draw_rect` passes with the appropriate `temp_*` state |
| `draw_rect()` | Render one rectangle and subtract its antialiasing mask |
| `get_corners()` | Group equal radii and drive `aa_corners` once per distinct radius |
| `aa_corners(border_radius)` | Build (and cache) one corner mask, mirror it to the flagged corners |
| `aa_sides()` | Paint the edge antialiasing lines |

### `aarect(...)` module function

Same signature as `AARect`'s constructor; builds and returns the surface without theme
resolution.

---

## 12.17 `pgmenu.text`

| Function | Signature |
| --- | --- |
| `match_font` | `(font, italic=False, bold=False)` |
| `format_font` | `(font, italic=False, bold=False)` |
| `render` | `(text=THEME, color=THEME, size=THEME, font=THEME, background=THEME, antialias=THEME, italic=THEME, bold=THEME, strikethrough=THEME, underline=THEME, transparency=THEME)` |
| `write` | `(surface, coords=THEME, text=THEME, color=THEME, size=THEME, font=THEME, background=THEME, antialias=THEME, italic=THEME, bold=THEME, strikethrough=THEME, underline=THEME, transparency=THEME, center_x=THEME, center_y=THEME)` |
| `fit_size` | `(dest_rect=THEME, text=THEME, color=THEME, margin=THEME, font=THEME, background=THEME, antialias=THEME, italic=THEME, bold=THEME, strikethrough=THEME, underline=THEME, transparency=THEME)` |
| `fit_render` | Same parameters as `fit_size`, returns a surface |
| `fit_render_animated` | Same parameters, `dest_rect` is an `AnimateTuple`; returns `(surface, rect)` |

---

## 12.18 `pgmenu.rect`

| Function | Signature | Returns |
| --- | --- | --- |
| `fit_rects` | `(dest_rect, *rects, margin=0)` | `(x, y, w, h)` per input, unwrapped when there is one |
| `center_rects` | `(dest_rect, *rects, center_x=THEME, center_y=THEME)` | Shifted rects, unwrapped when there is one |

---

## 12.19 `pgmenu.position`

| Function | Signature | Returns |
| --- | --- | --- |
| `center_coords` | `(size, rect, center_x=THEME, center_y=THEME)` | `(x, y)` |
| `place` | `()` | Stub |

---

## 12.20 `pgmenu.resize`

| Function | Signature | Description |
| --- | --- | --- |
| `_scale` | `(base, master_size, master_base_size, mode, resize_x, resize_y)` | Coverage-based scaling with optional aspect preservation |
| `responsive_resize` | `(widget, event)` | Apply size and coordinate scaling on `VIDEORESIZE` |
| `reset_videoresize` | `()` | Lower the `vars.videoresized` flag |

---

## 12.21 `pgmenu.display`

| Function | Signature | Description |
| --- | --- | --- |
| `fullscreen_controls` | `(screen, event)` | F11 toggle; returns the current display surface |
| `set_transparent_window` | `(transparency)` | Windows layered-window alpha |
| `set_transparent_colorkey` | `(colorkey)` | Windows layered-window colour key |

---

## 12.22 `pgmenu.menu`

| Name | Signature | Description |
| --- | --- | --- |
| `Menu` | `(*widgets, **kwargs)` | Widget group |
| `Menu.modify` | `(self, **kwargs)` | Set on the menu and on every member |
| `Menu.add` | `(self, *widgets)` | Append members |
| `Menu.remove` | `(self, *widgets)` | Remove members |
| `Menu.draw` | `(self)` | Draw only this menu |
| `show` | `(menu)` | Set the currently shown menu |
| `draw` | `()` | Draw the currently shown menu |

---

## 12.23 `pgmenu.simple`

| Name | Signature | Description |
| --- | --- | --- |
| `PgmenuWindow` | `(size=(230, 210), title="pgmenu", fps=60, flags=pygame.RESIZABLE)` | Window and loop wrapper |
| `PgmenuWindow.blit` | `(self, surface, dest)` | Register a surface drawn under the widgets |
| `PgmenuWindow.loop` | `(self, loop=None)` | Run the main loop |

---

## 12.24 `pgmenu.projects`

| Name | Signature | Description |
| --- | --- | --- |
| `MovablePlaneWindow` | `(screen, **kwargs)` | Pannable and zoomable plane demo |
| `MovablePlaneWindow.clear` | `(self)` | Drop registered surfaces |
| `MovablePlaneWindow.blit` | `(self, surface, dest)` | Register a surface at plane coordinates |
| `MovablePlaneWindow.controls` | `(self, event)` | Pan and zoom input handling |
| `MovablePlaneWindow.m_resize` | `(self, surface, coords, size, new_size)` | Default rescale strategy |
| `MovablePlaneWindow.draw` | `(self)` | Update zoom and draw visible surfaces |
| `modern_ui` | `()` | Stub |

---

## 12.25 `pgmenu.lib`

| Function | Signature | Description |
| --- | --- | --- |
| `init` | `()` | Create and load `pgmenu.Theme`, set the starting cursor |
| `_draw` | `(*widgets)` | Draw a sequence with the priority rules applied |
| `draw_all` | `()` | `_draw(*vars.widgets_draw_order)` |
| `update` | `(events)` | Full update pass |
| `request_cursor` | `(cursor)` | Set `vars.user_cursor` for this frame |
