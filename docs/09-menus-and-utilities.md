# 9. Menus and utilities

---

## 9.1 `pgmenu.menu`

A `Menu` is a named group of widgets that can be drawn and modified together.

```python
pgmenu.menu.Menu(*widgets, **kwargs)
```

| Member | Purpose |
| --- | --- |
| `widgets` | The grouped widgets |
| `get_widgets()` | Accessor |
| `add(*widgets)` | Append to the group |
| `remove(*widgets)` | Remove from the group, ignoring absent ones |
| `modify(**kwargs)` | Set the attribute on the menu **and** on every member |
| `draw()` | Draw only this menu's widgets, through `lib._draw` |

Module functions:

| Function | Purpose |
| --- | --- |
| `pgmenu.menu.show(menu)` | Record `menu` as the currently shown one |
| `pgmenu.menu.draw()` | Draw the currently shown menu, if any |

```python
main    = pgmenu.menu.Menu(title, play_button, quit_button)
options = pgmenu.menu.Menu(volume_label, volume_frame, back_button)

pgmenu.menu.show(main)

# in the loop, instead of pgmenu.draw_all()
pgmenu.menu.draw()
pgmenu.update(events)
```

### Current limitations

`Menu` groups drawing only. Widgets remain in the global registry, so widgets belonging to a
menu that is not shown are still iterated by `pgmenu.update()`. They are skipped in practice
because `_drawn` is `False` for anything that was not drawn, which means hidden menus are
inert, but they are not free and they are not removed.

Two practical consequences:

* Switching menus is `pgmenu.menu.show(other)`, and nothing else is required.
* If you want a widget truly gone, set `state = pgmenu.HIDDEN` as well.

`Menu.modify` sets the attribute on the `Menu` object itself before propagating, so a menu
accumulates whatever attributes you push through it. `Menu.__init__` forwards `**kwargs` to
`super().__init__()`, which is `object.__init__` and rejects arguments; call it without extra
keywords.

---

## 9.2 `pgmenu.display`

### `fullscreen_controls(screen, event)`

An F11 fullscreen toggle. Call it once per event and reassign the returned surface:

```python
for event in events:
    screen = pgmenu.display.fullscreen_controls(screen, event)
```

Behaviour:

* Remembers the windowed size in `pgmenu.vars.fs_window_size` before going fullscreen.
* Recreates the display at the desktop size, preserving the current flags and bit depth, then
  calls `pygame.display.toggle_fullscreen()`.
* On the way back it posts a `pygame.VIDEORESIZE` event manually so the responsive system
  reacts, then restores the remembered windowed size.
* On the very first invocation it captures the current window size and posts a
  `VIDEORESIZE`, which the source notes is required for correct behaviour.

The reason this cannot be folded into `pgmenu.update()` is that it must replace the caller's
`screen` reference, which a function receiving only the event list cannot do.

### `set_transparent_window(transparency)`

Makes the whole window translucent (`0` fully transparent, `255` opaque) using the Win32
layered-window API through `ctypes`.

### `set_transparent_colorkey(colorkey)`

Makes one specific colour fully transparent, so anything drawn in that colour becomes a hole
through the window.

```python
pgmenu.display.set_transparent_colorkey((255, 0, 255))
screen.fill((255, 0, 255))   # the desktop shows through
```

Both transparency helpers are **Windows only**. The module imports `ctypes.wintypes` at the
top level, which can fail on other platforms and take the whole `import pgmenu` down with it.
See [Known issues](13-known-issues.md#k1-unconditional-ctypeswintypes-import).

---

## 9.3 `pgmenu.simple.PgmenuWindow`

A tkinter-style convenience wrapper that owns the window, the clock and the loop.

```python
PgmenuWindow(size=(230, 210), title="pgmenu", fps=60, flags=pygame.RESIZABLE)
```

| Attribute | Purpose |
| --- | --- |
| `size`, `title`, `fps`, `flags` | Construction parameters, live attributes |
| `screen` | The display surface, pass it as a widget master |
| `clock` | The `pygame.time.Clock` |
| `blit_surfaces` | Surfaces registered through `blit()` |

| Method | Purpose |
| --- | --- |
| `blit(surface, dest)` | Register a surface to be blitted every frame, under the widgets |
| `loop(loop=None)` | Run the main loop, calling `loop()` once per frame |

The loop body, in order: drain events, handle `QUIT`, run `fullscreen_controls`, fill with
`pgmenu.Theme.bgcolor`, call your callback, blit registered surfaces, `pgmenu.draw_all()`,
`pgmenu.update(events)`, `flip`, `tick`.

`fps` and `title` can be changed at any time; `fps` takes effect on the next tick.

The class is annotated in-source as an unfinished demonstration. It is fine for tools and
prototypes; write the loop yourself when you need control over ordering.

---

## 9.4 `pgmenu.projects`

A collection of skeleton projects meant to be copied into an application, not a stable API.

### `MovablePlaneWindow(screen, **kwargs)`

An infinite pannable, zoomable plane.

| Keyword | Default | Meaning |
| --- | --- | --- |
| `scale_speed` | `0.1` | Zoom step per wheel notch |
| `min_scale` | `0.1` | Zoom floor |
| `move_speed` | `1` | Pan speed multiplier |
| `move_button` | `pygame.BUTTON_RIGHT` | Drag button |
| `resize` | `self.m_resize` | Surface rescaling strategy |

| Method | Purpose |
| --- | --- |
| `clear()` | Drop all registered surfaces |
| `blit(surface, dest)` | Register a surface at plane coordinates |
| `controls(event)` | Feed it events for panning and zooming |
| `m_resize(surface, coords, size, new_size)` | Default rescale, replaces the stored surface |
| `draw()` | Update the zoom animation and draw everything currently in view |

Zooming is animated through an `Animate` and is centred on the mouse position. Off-screen
surfaces are culled with a small wiggle factor so partially visible items still render.

The source marks it as a demo that does not work particularly well. Treat it as a starting
point.

`modern_ui()` is a stub reserved for loading the gradient assets that the `MODERN` theme
expects.

---

## 9.5 `pgmenu.system`

User-tunable engine settings, meant to be assigned directly.

| Setting | Default | Effect |
| --- | --- | --- |
| `widget_draw_priority` | `True` | Whether hovered/active widgets that opt in are drawn on top |
| `max_cache_size` | `300` | Maximum entries **per cache**; there are five caches |

```python
import pgmenu
pgmenu.system.max_cache_size = 100        # lower memory ceiling
pgmenu.system.widget_draw_priority = False
```

The source note is worth repeating: roughly 100 entries in the rectangle cache costs on the
order of 150 MB depending on surface sizes, and the limit applies to each of the five caches
independently. Lower it on memory-constrained targets, raise it for UIs with many large
distinct surfaces.

---

## 9.6 `pgmenu.vars`

Global mutable runtime state. Read it freely for introspection; write to it only if you know
what the engine expects.

| Variable | Meaning |
| --- | --- |
| `widgets` | Every widget ever created, in creation order (update order) |
| `widgets_draw_order` | Draw order, with the frame insertion rule applied |
| `widget_types` | Names used to detect widget-prefixed theme keys |
| `cache` | The five `Cache` instances |
| `Theme` | Always `None`; the live theme is `pgmenu.Theme` |
| `widget_cursor` | Cursor requested by a widget this frame |
| `user_cursor` | Cursor requested by the application this frame |
| `base_window_size` | Reference window size for responsive maths |
| `videoresized` | True while a responsive pass is in flight |
| `fs_window_size` | Windowed size remembered across a fullscreen toggle |
| `mouse_x`, `mouse_y` | Mouse position cached once per frame |
| `current_menu_showed` | The menu `pgmenu.menu.draw()` will draw |

Useful introspection:

```python
print(len(pgmenu.vars.widgets), "widgets")
print([w.type for w in pgmenu.vars.widgets_draw_order])
print({name: len(c) for name, c in pgmenu.vars.cache.items()})
```

---

## 9.7 `pgmenu.cache`

| Member | Purpose |
| --- | --- |
| `Cache` | `OrderedDict` subclass that normalises `AnimateType` values inside tuple keys |
| `lru_get(cache, key)` | Return the value and mark it recently used, or `None` |
| `lru_set(cache, key, value)` | Insert and evict the least recently used entry past `max_cache_size` |
| `clear_cache()` | Intended to empty every cache; currently broken |

To clear the caches today:

```python
for c in pgmenu.vars.cache.values():
    c.clear()
```

Writing your own cached helper:

```python
from pgmenu.vars import cache

def my_shape(size, color):
    cache_id = (size, color)

    cached = pgmenu.cache.lru_get(cache["surface"], cache_id)
    if cached is not None:
        return cached

    surface = build_it(size, color)
    pgmenu.cache.lru_set(cache["surface"], cache_id, surface)
    return surface
```

Keys must be tuples for the animation normalisation to apply, and every element must be
hashable after normalisation.

---

## 9.8 `pgmenu.lib`

The engine functions, all re-exported at package level.

| Function | Package-level name | Purpose |
| --- | --- | --- |
| `init()` | `pgmenu.lib.init` | Build and load `pgmenu.Theme`, set the starting cursor. Called on import |
| `_draw(*widgets)` | internal | Draw a specific widget sequence with the priority rules |
| `draw_all()` | `pgmenu.draw_all` | Draw every registered widget |
| `update(events)` | `pgmenu.update` | The full update pass |
| `request_cursor(cursor)` | `pgmenu.request_cursor` | Claim the cursor for this frame; `None` releases it |

```python
def m_animation_on_hover(self):
    pgmenu.request_cursor(pygame.SYSTEM_CURSOR_HAND)
```
