# 6. Theming

Every default value in pgmenu lives in a JSON theme file. The theme is dynamic: it can be
loaded, extended and swapped at any point during runtime.

---

## 6.1 The `THEME` sentinel

Nearly every function argument and widget parameter in pgmenu defaults to the string constant
`pgmenu.THEME` (`"theme"`). At call time it is replaced by the theme's value:

```python
def render(text=THEME, color=THEME, size=THEME, ...):
    text  = resolve(text,  pgmenu.Theme.text_text)
    color = resolve(color, pgmenu.Theme.text_color)
    size  = resolve(size,  pgmenu.Theme.text_size)
```

This is why you can call `pgmenu.text.write(screen)` with no styling arguments at all and get
a themed result, and why overriding one argument never forces you to restate the others.

A second sentinel, `pgmenu.UNSET` (`"unset"`), means "I have no opinion". `resolve` treats it
exactly like `THEME`, so a widget can pass `UNSET` down to a lower layer and let *that* layer
apply its own defaults. `RectMixin` and `TextMixin` use this heavily.

---

## 6.2 File format

Theme files live in `pgmenu/themes/<NAME>.json`. The top-level object has a single key, the
theme name, whose value is the attribute map:

```json
{
  "DEFAULT": {
    "bgcolor": [43, 46, 49],
    "button_fill": [42, 120, 205],
    "button_size": [100, 30]
  }
}
```

Attribute names follow `[module or widget]_[attribute]`:

| Prefix | Applies to |
| --- | --- |
| `position_` | `pgmenu.position` |
| `animation_` | `pgmenu.animation` objects |
| `text_` | `pgmenu.text` functions |
| `aarect_` | `pgmenu.draw.aarect` (the one prefix not derived from a file name) |
| `widget_` | `pgmenu.widget.Widget` defaults for all widgets |
| `rectmixin_` | `RectMixin` fallbacks |
| `label_`, `surface_`, `frame_`, `button_`, `checkbox_` | The matching widget |
| no prefix | Library-wide (`bgcolor`) |

The `aarect_` prefix is an acknowledged exception: the function lives in `draw.py` but the
class it drives lives in `aarect.py`, and the class name won.

### Comments

JSON has no comment syntax, so pgmenu reserves the key `"#"`:

```json
"#": "Button",
"button_coords": [20, 20],
```

`Theme.set` skips the `"#"` key. Because JSON objects cannot really hold duplicate keys, a
standard parser keeps only the last `"#"` in a file; this is harmless (the value is discarded
anyway) but means comments exist for the human reading the file, not for the parser.

### Lists become tuples

Every JSON array is converted to a Python tuple on load, because lists are unhashable and
would break the cache keys built from theme values.

---

## 6.3 Special value types

A JSON object with a `"type"` key expresses a Python value that JSON cannot represent
natively.

| Type | Form | Result |
| --- | --- | --- |
| `method` | `{"type": "method", "module": "pgmenu.widget", "object": "Widget", "method": "m_on_standby"}` | Instantiates the class and binds the named method |
| `function` | `{"type": "function", "module": "pgmenu.animation", "function": "circ"}` | The module-level function object |
| `attribute` | `{"type": "attribute", "attribute": "border_radius"}` | The value of an attribute already set on the theme |
| `variable` | `{"type": "variable", "module": "pgmenu", "variable": "NORMAL"}` | A module-level variable or constant |
| `image` | `{"type": "image", "path": "../assets/gradient.png"}` | `pygame.image.load(path)` |
| `exec` | `{"type": "exec", "code": "round(min(self.aarect_rect[2:]) / 3)"}` | The evaluated expression, implicitly prefixed with `attr = ` |

Notes and constraints:

* `module` must already be imported; the implementation looks it up in `sys.modules`, it does
  not import on demand. Importing your own module before calling `Theme.load` is enough.
* `attribute` resolves against the theme instance being built, so ordering matters: the
  referenced attribute must appear earlier in the file.
* `image` paths are resolved relative to the process working directory, not to the theme
  file. Absolute paths are safer.
* `method` constructs a throwaway instance (`cls()`), so the class must be constructible with
  no arguments. `Widget()` qualifies.
* `exec` is currently non-functional; see
  [Known issues](13-known-issues.md#k6-exec-theme-type-does-not-assign).

---

## 6.4 The `null` convention

Setting an attribute to `null` in a theme makes it `None` in Python, and `resolve` treats
`None` as "no theme value", falling through to the code-level default:

```python
def resolve(value, theme_attr, default=None):
    if value != pgmenu.THEME and value != pgmenu.UNSET:
        return value
    elif theme_attr is not None:
        return theme_attr
    else:
        return default
```

This is how context-dependent defaults are expressed. `DEFAULT.json` leaves
`aarect_border_radius` as `null`, and `draw.aarect` supplies
`round(min(rect[2:]) / 4)`; a user theme that wants a fixed radius simply sets a number
instead.

The same pattern in widget code:

```python
self.border_radius = resolve(border_radius,
                             pgmenu.Theme.button_border_radius,
                             round(min(self.size) / 3))
```

And for corner radii, where `None` means "inherit from `border_radius`":

```json
"aarect_border_top_left_radius": null,
```

```python
border_top_left_radius = (pgmenu.Theme.aarect_border_top_left_radius
                          if pgmenu.Theme.aarect_border_top_left_radius is not None
                          else border_radius)
```

---

## 6.5 The three resolvers

```
resolve(value, theme_attr, default=None)
```

| `value` | Result |
| --- | --- |
| Anything except `THEME` / `UNSET` | `value` |
| `THEME` or `UNSET`, theme attribute is not `None` | The theme attribute |
| `THEME` or `UNSET`, theme attribute is `None` | `default` |

```
resolve_kwarg(kwargs, key, theme_attr, default=None)
```

Same, sourcing the value from `kwargs.get(key, pgmenu.THEME)`. Used for optional keyword
arguments that are not in the explicit signature (`inner_fill` and friends).

```
resolve_widget(kwargs, key, widget_type, default=None)
```

Same again, but the theme attribute is looked up dynamically as
`getattr(pgmenu.Theme, f"{widget_type}_{key}", None)`. This is what lets a theme override a
single widget type without every widget declaring every possible key.

Decision flow:

```
resolve_widget
  user supplied the kwarg?
      yes, and it is not THEME/UNSET  -> user value
      yes, but it is THEME/UNSET      -> {type}_{key} if defined, else default
      no                              -> {type}_{key} if defined, else default
```

Because a missing theme attribute yields `None` from `getattr(..., None)`, the absence of a
per-widget key is indistinguishable from an explicit `null`, and both fall through to
`default`. That is why animation and callback keys need no entries in `DEFAULT.json` at all.

---

## 6.6 Global attributes

Prefixing an attribute with `widgets_` applies it to every widget type at once:

```json
"widgets_border_radius": 8,
"button_border_radius": 16
```

Assignment follows file order, so the later `button_border_radius` wins for buttons while
every other widget gets `8`. Put your global first and your exceptions after it.

> The current implementation calls `str.startswith` with a list, which raises `TypeError`.
> Until that is fixed, `widgets_` keys cannot be used. See
> [Known issues](13-known-issues.md#k7-global-widgets_-prefix-raises-typeerror).

---

## 6.7 The `Theme` class

```python
pgmenu.Theme                      # the live instance, created by lib.init()
pgmenu.theme.Theme                # the class
```

| Method | Purpose |
| --- | --- |
| `load(theme="DEFAULT")` | Read `themes/<theme>.json` and apply it through `set()` |
| `set(**attrs)` | Apply an attribute map, handling comments, special types and list conversion |
| `save(theme, **attrs)` | Write the given attributes to `themes/<theme>.json` |
| `save_all(theme)` | Write every attribute currently on the instance |

`load` accepts a name with or without the `.json` extension, and always resolves the path
relative to the `pgmenu` package directory.

`load` is **additive**. It calls `set()`, which assigns attributes onto the existing
instance; it does not clear anything first. Loading a partial theme on top of `DEFAULT`
therefore overrides only the keys it declares, which is the intended way to write a small
theme. It also means you cannot "unload" a theme without restarting or reloading `DEFAULT`.

`save_all` uses `vars(self)`, which includes non-serialisable values such as loaded surfaces
and function objects, so it only works for themes made entirely of primitives.

---

## 6.8 Runtime theme switching

```python
pgmenu.Theme.load("MODERN")
```

What changes immediately and what does not:

| Consumer | Effect of a reload |
| --- | --- |
| Module-level functions (`text.*`, `draw.aarect`, `position.center_coords`) | Immediate; they resolve at call time |
| Widget attributes | Not retroactive; they were resolved once in `__init__` |
| Newly created widgets | Immediate |

To re-theme a live interface, reload and then rebuild the widgets, or assign the new values
explicitly with `widget.modify(...)`.

A stale-cache caveat: rendered text, rectangles and layouts are cached on their *arguments*,
not on the theme, so a theme change produces new arguments and therefore new cache entries.
Old entries age out through the LRU.

---

## 6.9 Bundled themes

**`DEFAULT.json`** is the reference theme and the one loaded at import. It defines every key
the library reads.

**`MODERN.json`** is experimental. Its keys (`size`, `border_radius`, `fill`, `outline_fill`,
`margin`, ...) do not carry a module or widget prefix, so nothing in the library reads them;
they are simply attached to the theme object. Its `image` paths are also relative
(`../tests/assets/gradient.png`). It illustrates the intended visual direction (gradient
image fills with a contrasting gradient outline) rather than being a working theme.

---

## 6.10 Full `DEFAULT.json` attribute reference

### Library

| Key | Default | Used by |
| --- | --- | --- |
| `bgcolor` | `[43, 46, 49]` | Your `screen.fill`, `PgmenuWindow.loop` |

### Position

| Key | Default | Used by |
| --- | --- | --- |
| `position_center_x` | `true` | `position.center_coords` |
| `position_center_y` | `true` | `position.center_coords` |

### Animation

| Key | Default | Used by |
| --- | --- | --- |
| `animation_duration` | `0.15` | All animation objects |
| `animation_curve` | `circ` | All animation objects |
| `animation_base_alpha` | `0` | `AnimateSurface` |
| `animation_final_alpha` | `0` | `AnimateSurface` |
| `animation_precision` | `0` | Rounding of animated values |

### Text

| Key | Default |
| --- | --- |
| `text_text` | `"Text"` |
| `text_font` | `null` (bundled VarelaRound) |
| `text_color` | `[255, 255, 255]` |
| `text_size` | `20` |
| `text_margin` | `0` |
| `text_background` | `null` |
| `text_antialias` | `true` |
| `text_italic` | `false` |
| `text_bold` | `false` |
| `text_strikethrough` | `false` |
| `text_underline` | `false` |
| `text_transparency` | `255` |
| `text_center_x` | `false` |
| `text_center_y` | `false` |
| `text_coords` | `[20, 20]` |
| `text_dest_rect` | `[100, 30]` |

### AARect

| Key | Default | Fallback when `null` |
| --- | --- | --- |
| `aarect_fill` | `[255, 255, 255]` | |
| `aarect_rect` | `[10, 10, 50, 50]` | |
| `aarect_width` | `0` | |
| `aarect_border_radius` | `null` | `round(min(rect[2:]) / 4)` |
| `aarect_border_top_left_radius` | `null` | `border_radius` |
| `aarect_border_top_right_radius` | `null` | `border_radius` |
| `aarect_border_bottom_left_radius` | `null` | `border_radius` |
| `aarect_border_bottom_right_radius` | `null` | `border_radius` |
| `aarect_antialiasing` | `true` | |
| `aarect_transparency` | `255` | |
| `aarect_aa_strength` | `1` | |
| `aarect_debug` | `false` | |
| `aarect_inner_fill` | `null` | `fill` |
| `aarect_inner_transparency` | `null` | `transparency` |
| `aarect_inner_aa_strength` | `null` | `aa_strength` |
| `aarect_inner_antialiasing` | `null` | `antialiasing` |

### Widget

| Key | Default |
| --- | --- |
| `widget_responsive_size` | `PROPORTIONAL` |
| `widget_responsive_size_w` | `true` |
| `widget_responsive_size_h` | `true` |
| `widget_responsive_coords` | `STRETCH` |
| `widget_responsive_coords_x` | `true` |
| `widget_responsive_coords_y` | `true` |
| `widget_state` | `NORMAL` |
| `widget_animation_scale` | `1.2` |
| `widget_animation_duration` | `0.15` |
| `widget_animation_curve` | `circ` |
| `widget_disable_animation` | `false` |

### RectMixin

| Key | Default |
| --- | --- |
| `rectmixin_antialiasing` | `true` |
| `rectmixin_transparency` | `255` |
| `rectmixin_aa_strength` | `1` |

### Label

`label_coords` `[20, 20]`, `label_text` `"Label"`, `label_font` `null`, `label_color`
`[255, 255, 255]`, `label_size` `20`, `label_background` `null`, `label_antialias` `true`,
`label_italic` `false`, `label_bold` `false`, `label_strikethrough` `false`,
`label_underline` `false`, `label_transparency` `255`, `label_center_x` `false`,
`label_center_y` `false`.

### Surface

`surface_coords` `[20, 20]`, `surface_on_resize` `null`.

### Frame

`frame_coords` `[20, 20]`, `frame_size` `[200, 200]`, `frame_fill` `[47, 51, 54]`,
`frame_width` `0`, `frame_border_radius` `null` (falls back to `round(min(size) / 7)`), plus
any `frame_`-prefixed `RectMixin` key.

### Button

`button_coords` `[20, 20]`, `button_size` `[100, 30]`, `button_fill` `[42, 120, 205]`,
`button_text` `"Button"`, `button_text_color` `[255, 255, 255]`, `button_icon` `null`,
`button_margin` `3`, `button_width` `0`, `button_border_radius` `null` (falls back to
`round(min(size) / 3)`), plus any `button_`-prefixed `RectMixin` or `TextMixin` key.

### Checkbox

`checkbox_fill` `[63, 68, 72]`. The remaining `checkbox_*` keys
(`checkbox_coords`, `checkbox_size`, `checkbox_text`, `checkbox_text_color`,
`checkbox_check_fill`, `checkbox_margin`, `checkbox_width`, `checkbox_border_radius`,
`checkbox_checked`) are read by `checkbox.py` but are not yet defined in the theme.

---

## 6.11 Writing your own theme

`pgmenu/themes/OCEAN.json`:

```json
{
  "OCEAN": {
    "#": "Palette",
    "bgcolor": [12, 24, 38],

    "#": "Widgets",
    "widget_animation_scale": 1.1,
    "widget_animation_duration": 0.12,

    "#": "Frame",
    "frame_fill": [18, 36, 56],
    "frame_border_radius": 14,

    "#": "Button",
    "button_fill": [26, 142, 198],
    "button_text_color": [240, 250, 255],
    "button_border_radius": 10,
    "button_width": 0,

    "#": "Label",
    "label_color": [214, 232, 244],

    "#": "End of file."
  }
}
```

```python
import pgmenu
pgmenu.Theme.load("OCEAN")   # applied on top of DEFAULT
```

Because loading is additive, a partial theme like this one only needs the keys it changes.
