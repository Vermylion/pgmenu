# 8. Drawing and text

The drawing layer is usable on its own. Nothing in this chapter requires a widget.

---

## 8.1 `pgmenu.draw.aarect`

```python
pgmenu.draw.aarect(surface=None, fill=THEME, rect=THEME, width=THEME,
                   border_radius=THEME,
                   border_top_left_radius=THEME, border_top_right_radius=THEME,
                   border_bottom_left_radius=THEME, border_bottom_right_radius=THEME,
                   antialiasing=THEME, transparency=THEME, aa_strength=THEME,
                   **kwargs)
```

Draws an antialiased rounded rectangle and returns it as a surface.

| Parameter | Meaning | Theme default |
| --- | --- | --- |
| `surface` | Destination. `None` means "build and return only, do not blit" | none |
| `fill` | `tuple`/`list`/`pygame.Color`/`pygame.Surface`/`AnimateType` | `(255, 255, 255)` |
| `rect` | `(x, y, w, h)`; `x, y` are only used for the blit | `(10, 10, 50, 50)` |
| `width` | Outline width in pixels; `0` means filled | `0` |
| `border_radius` | Radius applied to every corner without its own value | `null` then `round(min(w, h) / 4)` |
| `border_*_radius` | Per-corner override | `null` then `border_radius` |
| `antialiasing` | Enable the antialiasing pass | `True` |
| `transparency` | Surface alpha, `0..255` | `255` |
| `aa_strength` | Number of blended pixels at the edge | `1` |

Keyword-only extras:

| Keyword | Meaning | Falls back to |
| --- | --- | --- |
| `inner_fill` | Fill of the area inside the outline | `fill` |
| `inner_transparency` | Alpha of that area | `transparency` |
| `inner_aa_strength` | Antialiasing width of the inner edge | `aa_strength` |
| `inner_antialiasing` | Antialiasing of the inner edge | `antialiasing` |
| `debug` | Print generation timing when the shape is not cached | `aarect_debug` (`False`) |

A four-component colour is accepted: the fourth component is moved into `transparency` and
the fill becomes a three-tuple. The same applies to `inner_fill`.

A `pygame.Surface` fill is smoothscaled to the rectangle's dimensions, which is how gradient
fills work:

```python
gradient = pygame.image.load("assets/gradient.png")
panel = pgmenu.draw.aarect(None, gradient, (0, 0, 240, 64), border_radius=16)
screen.blit(panel, (20, 20))
```

Common shapes:

```python
# filled, default radius
pgmenu.draw.aarect(screen, (42, 120, 205), (20, 20, 200, 60))

# pill
pgmenu.draw.aarect(screen, (42, 120, 205), (20, 20, 200, 60), border_radius=30)

# outline only
pgmenu.draw.aarect(screen, (255, 255, 255), (20, 20, 200, 60), width=2)

# outline with a distinct interior
pgmenu.draw.aarect(screen, (255, 255, 255), (20, 20, 200, 60), width=2,
                   inner_fill=(30, 30, 40))

# tab shape: rounded on top only
pgmenu.draw.aarect(screen, (60, 60, 70), (20, 20, 120, 40),
                   border_top_left_radius=12, border_top_right_radius=12,
                   border_bottom_left_radius=0, border_bottom_right_radius=0)

# heavier antialiasing
pgmenu.draw.aarect(screen, (200, 80, 80), (20, 20, 200, 60), aa_strength=3)
```

`pgmenu.aarect.aarect(...)` is the same function without theme resolution: every argument
must be supplied and there are no `THEME` defaults. Use `pgmenu.draw.aarect` unless you are
deliberately bypassing the theme.

`pgmenu.draw.gradient(color1, color2, angle, curve)` is declared but not implemented.

---

## 8.2 Inside `AARect`

`pgmenu.aarect.AARect` builds the shape. Everything happens during construction plus the
`aarect()` call; there is no incremental drawing.

### Call flow

```
AARect(...)            store arguments, temp_* copies and the four draw_border_* flags
  .aarect()
      .format_rect()   validate, normalise, clamp, build the cache id
      cache miss?
          .create_rect()
              .draw_rects()      up to three passes, each ending in .draw_rect()
                  outer rectangle
                  inner rectangle to subtract      (only when width and not force_only_overlay)
                  inner rectangle overlay          (only when width and inner_fill)
              subtract the inner rectangle with BLEND_RGBA_SUB
              blit the overlay
              store in cache["aarect"]
      return cache entry .copy()
```

### `format_rect`

* Rejects a `fill` that is not a `tuple`, `list`, `pygame.Surface`, `pygame.Color` or
  `AnimateType`.
* Splits a four-component colour into colour plus `transparency`.
* Smoothscales surface fills to the rectangle size.
* Clamps `width` to half the smaller side.
* Floors every radius at half the smaller side, so radii can never overlap.
* Builds `object_cache_id`, a tuple of every visual parameter (with `str()` applied to the
  fills).

### `draw_rect`

The single-pass renderer, driven entirely by the `temp_*` attributes so the same code serves
all three passes.

```
if rect is degenerate (w < 1 or h < 1): return an empty surface
create aa_surface       (SRCALPHA, size of the rect)
create draw_rect_surface (SRCALPHA, size of the rect)
fill it with temp_fill (blit if temp_fill is a Surface)
set_alpha(temp_transparency)
get_corners()   -> paints corner alpha into aa_surface
aa_sides()      -> paints edge alpha into aa_surface
draw_rect_surface.blit(aa_surface, (0, 0), special_flags=BLEND_RGBA_SUB)
```

The shape is therefore *subtractive*: a full rectangle is drawn and the corners and edges are
carved out of its alpha channel.

### `get_corners`

Groups corners with identical radii so each distinct radius is computed once, then sets the
`draw_border_*_radius` flags telling `aa_corners` which corners to paint this round. A
rectangle with four equal radii runs one corner computation; a rectangle with four different
radii runs four.

### `aa_corners`

For a corner of radius `r`, iterate the `r` by `r` square and compute each pixel's distance
from the circle centre at `(r, r)`:

* distance below `r - aa_strength`: inside the shape, untouched.
* distance between `r - aa_strength` and `r`: partial alpha from
  `(r - distance + 2) * (255 / (aa_strength + 2))`, capped at 255.
* distance above `r`: fully removed (alpha 255).

The resulting alpha then goes through two corrections:

1. `utils.only_alpha_blending(alpha, 0)` applied twice, compensating for the value passing
   through three surfaces instead of one.
2. `utils.sub_values[alpha]`, a 256-entry lookup table mapping "the alpha I want to end up
   subtracting" to "the alpha I must write so that `BLEND_RGBA_SUB` produces it".

The mask colour is `(a, a, a, a)` for inner antialiasing or fully removed pixels, and
`(0, 0, 0, a)` otherwise, which subtracts alpha without darkening the colour channels.

One corner is computed and cached under
`(border_radius, aa_pixel_width, antialiasing, inner_aa)`, then mirrored with
`pygame.transform.flip` for the other three.

### `aa_sides`

For each antialiasing layer from `1` to `aa_strength`, computes the layer alpha, applies the
same two corrections, and draws four `pygame.gfxdraw.line` segments along the edges between
the corner arcs.

### `force_only_overlay`

Set when `inner_transparency == 255` and `inner_fill is not None`. An opaque inner fill hides
whatever is underneath, so the "subtract the interior" pass is skipped and only the overlay is
drawn. This is a pure optimisation.

### Performance and caching

| Cache | Key | Effect |
| --- | --- | --- |
| `cache["aarect"]` | Every visual parameter | A static widget renders its rectangle once, ever |
| `cache["aarect_corner"]` | Radius plus antialiasing parameters | Shared across every rectangle with the same corner |

The per-pixel corner loop is the expensive part, which is why the corner cache exists
separately: an animated rectangle changing size still reuses its corners as long as the radius
is unchanged, and the animation `precision` setting keeps radius values from exploding into
thousands of distinct keys.

Set `debug=True` (or `aarect_debug` in the theme) to print the generation time whenever a
shape is actually built. Persistent printing means you are missing the cache.

---

## 8.3 `pgmenu.text`

### `match_font(font, italic=False, bold=False)`

Resolves a font name or file to an absolute path, trying `pygame.font.match_font` first and
then the working directory. Returns `None` when nothing matches.

### `format_font(font, italic=False, bold=False)`

Normalises `None` or `"VarelaRound.ttf"` to the bundled font shipped next to `text.py`, then
runs `match_font`. This is the function that gives pgmenu its default typeface.

### `render(...)`

```python
pgmenu.text.render(text=THEME, color=THEME, size=THEME, font=THEME, background=THEME,
                   antialias=THEME, italic=THEME, bold=THEME, strikethrough=THEME,
                   underline=THEME, transparency=THEME)
```

Renders text to a new surface and returns a copy.

* `\n` is supported: each line is rendered separately and the lines are stacked, with the
  surface width taken from the widest line and the height from the sum.
* `transparency` is applied with `set_alpha`.
* The result is cached on all eleven arguments, and a **copy** is returned so callers can
  mutate it safely.

### `write(...)`

```python
pgmenu.text.write(surface, coords=THEME, text=THEME, ..., center_x=THEME, center_y=THEME)
```

`render` plus a blit, with optional centring around `coords`. The convenience function for
debug overlays:

```python
pgmenu.text.write(screen, (20, 20), str(round(clock.get_fps())))
```

### `fit_size(...)`

```python
pgmenu.text.fit_size(dest_rect=THEME, text=THEME, color=THEME, margin=THEME, ...)
```

Returns the largest integer point size at which `text` fits inside `dest_rect` (a
`(width, height)` pair), minus `margin`. It starts from `min(dest_rect)`, then scales down by
the width overflow ratio and again by the height overflow ratio, using `math.floor` so the
result never overshoots. Cached.

### `fit_render(...)`

`fit_size` followed by `render`, returning a copy of the fitted surface. Use this for static
text that must fill a box.

### `fit_render_animated(...)`

```python
surface, rect = pgmenu.text.fit_render_animated(dest_rect, text, color, margin, ...)
```

The version used by `Button`. `dest_rect` is an `AnimateTuple`, and the function:

1. Renders once at the animation's **final** size (`dest_rect.final_tuple`), so the glyph
   rasterisation is done at the largest size and only once.
2. Computes the text rectangle for the **current** animated size with `rect.fit_rects`.
3. `smoothscale`s the rendered text into that rectangle.
4. Centres it inside the current destination rect.

Returns the scaled surface and its rectangle. Scaling pixels rather than re-rendering at each
integer point size is what makes growing text look continuous instead of stepping.

> The returned rectangle is built as `(*text_pos, text_rect[2:])`, a three-element tuple whose
> last element is itself a tuple. Callers use only `[:2]`. See
> [Known issues](13-known-issues.md#k8-fit_render_animated-returns-a-malformed-rect).

---

## 8.4 `pgmenu.rect`

### `fit_rects(dest_rect, *rects, margin=0)`

Fits any number of `(width, height)` rectangles side by side inside `dest_rect`, preserving
each one's aspect ratio, and returns their positions as `(x, y, w, h)`.

* All rectangles are first scaled to the destination height minus vertical margins.
* If the row is then too wide, everything is scaled down by a single common factor so the
  proportions between items are preserved.
* Items are laid left to right with `margin` between them and around the outside.
* A single input rectangle is returned unwrapped rather than as a one-element list.
* Cached on `(dest_rect, rects, margin)`.

This is the icon-plus-label layout engine used by `Button`.

### `center_rects(dest_rect, *rects, center_x=THEME, center_y=THEME)`

Centres a **group** of rectangles inside `dest_rect` while preserving their relative
positions: it computes the bounding box of all inputs, centres that box, and shifts every
rectangle by the same offset. A single rectangle is returned unwrapped. Cached.

Together:

```python
icon_rect, text_rect = pgmenu.rect.fit_rects(button_size, icon.get_size(), text.get_size(),
                                             margin=4)
icon_rect, text_rect = pgmenu.rect.center_rects((0, 0, *button_size), icon_rect, text_rect)
```

---

## 8.5 `pgmenu.position`

### `center_coords(size, rect, center_x=THEME, center_y=THEME)`

Returns the top-left coordinates that centre a `size` inside a `(x, y, w, h)` rectangle,
independently per axis.

```python
coords = pgmenu.position.center_coords((550, 400), (0, 0, 1080, 720))
```

Passing a zero-sized rectangle turns it into a centre-on-a-point helper, which is how `Label`
centres on its `coords`:

```python
coords = pgmenu.position.center_coords(self.surface_size, (*self.coords, 0, 0),
                                       self.center_x, self.center_y)
```

`place()` is declared but not implemented; a grid or anchor layout helper is the intended
follow-up.

---

## 8.6 `pgmenu.utils`

| Member | Purpose |
| --- | --- |
| `sub_values` | 256-entry lookup table mapping a desired subtracted alpha to the alpha that must be written for `BLEND_RGBA_SUB` to produce it |
| `only_alpha_blending(source_alpha, dest_alpha)` | Alpha-only blend, used to pre-compensate for values passing through several surfaces |
| `div(a, b, round_num=None)` | Division that returns `float('inf')` instead of raising on divide by zero |

These exist for `AARect` and are unlikely to be needed directly, but `div` is handy for
frames-per-second style computations.
