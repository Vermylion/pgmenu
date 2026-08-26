# 11. Cookbook

Short, working recipes. Each assumes `import pygame, pgmenu`, an initialised display and the
standard loop from [Getting started](02-getting-started.md#23-anatomy-of-the-loop).

---

## C1. Reading the debug scripts

Three scratch files in the repository are the closest thing to a live test suite. They are not
part of the package and are not imported by it.

| File | What it demonstrates |
| --- | --- |
| `DebugWindow.py` | The broadest example: a `Frame` containing a `Surface`, a `Label` with an explicit colour animation and an icon `Button`; live attribute mutation on key presses; a stress mode that resizes the window to random dimensions on a timer |
| `DebugFile.py` | The `PgmenuWindow` path, the `MODERN` theme, and per-widget responsive overrides (`button.responsive_size = pgmenu.STRETCH`) |
| `DebugCode.py` | Animation objects used **without** widgets: `AnimateTuple` for a rect size, `Animate` for a border radius, manual hover detection, and manual text smoothscaling, that is, the technique that `text.fit_render_animated` encapsulates |

The stress loop in `DebugWindow.py` is worth copying when you touch the responsive system:

```python
if go and (time.time() - start) >= 0.05:
    start = time.time()
    w, h = random.randint(10, 3000), random.randint(10, 3000)

    # every 100 iterations, return to the design size and print the geometry
    if incr % 100 == 0:
        w, h = 1080, 720

    screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE))
```

Returning to the design size must restore the original geometry exactly. If it does not, base
geometry is being corrupted somewhere.

---

## C2. Centre a frame in the window

```python
size = (550, 400)
frame = pgmenu.frame.Frame(screen,
                           pgmenu.position.center_coords(size, (0, 0, *screen.get_size())),
                           size)
```

`responsive_coords` defaults to `STRETCH`, so the frame stays centred through a resize.

---

## C3. Two screens with `Menu`

```python
title = pgmenu.label.Label(screen, (320, 80), "My Game", size=48, center_x=True)
play  = pgmenu.button.Button(screen, (270, 200), (140, 40), text="Play")
opts  = pgmenu.button.Button(screen, (270, 250), (140, 40), text="Options")

volume = pgmenu.label.Label(screen, (320, 120), "Volume", size=32, center_x=True)
back   = pgmenu.button.Button(screen, (270, 250), (140, 40), text="Back")

main_menu    = pgmenu.menu.Menu(title, play, opts)
options_menu = pgmenu.menu.Menu(volume, back)

play.on_release = lambda: print("start")
opts.on_release = lambda: pgmenu.menu.show(options_menu)
back.on_release = lambda: pgmenu.menu.show(main_menu)

pgmenu.menu.show(main_menu)

# in the loop, replacing pgmenu.draw_all()
pgmenu.menu.draw()
pgmenu.update(events)
```

---

## C4. A gradient button

Any `pygame.Surface` can be a fill; it is smoothscaled into the shape.

```python
gradient = pygame.image.load("assets/gradient.png")
outline  = pygame.image.load("assets/gradient2.png")

button = pgmenu.button.Button(screen, (40, 40), (160, 40),
                              text="Continue",
                              fill=outline,
                              width=1,
                              inner_fill=gradient,
                              border_radius=12)
```

`width=1` with a distinct `inner_fill` gives a one pixel gradient outline around a gradient
body, which is the look the `MODERN` theme is aiming at.

---

## C5. An icon button

```python
icon = pygame.image.load("assets/save.png")
button = pgmenu.button.Button(screen, (40, 40), (140, 36),
                              text="Save", icon=icon, margin=4)
```

The icon and the label are fitted side by side by `rect.fit_rects` and centred together by
`rect.center_rects`. Raise `margin` for more breathing room; the icon is scaled to the
button height minus the margins.

---

## C6. FPS overlay

```python
def loop():
    pgmenu.text.write(screen, (10, 10), str(round(clock.get_fps())))
```

Call it before `pgmenu.draw_all()` to put it under the UI, after to put it over.

---

## C7. Custom cursor while hovering

Per widget type, by overriding the method:

```python
class MyButton(pgmenu.button.Button):
    def request_cursor(self):
        pgmenu.vars.widget_cursor = pygame.SYSTEM_CURSOR_CROSSHAIR
```

Per instance, from a hover hook:

```python
def hover():
    pgmenu.request_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

widget.on_hover = hover
```

`pgmenu.request_cursor` wins over any widget request and is cleared every frame, so it must
be called from a hook that fires continuously (`on_hover` does).

---

## C8. Turn animation off

```python
button = pgmenu.button.Button(screen, (20, 20), (120, 32), disable_animation=True)
```

Globally, in a theme:

```json
"widget_disable_animation": true
```

Or keep animation but remove the growth by setting `widget_animation_scale` to `1`.

---

## C9. Animate to a specific colour

Automatic wrapping scales colour components by `animation_scale`, which cannot reach an
arbitrary destination. Build the animation yourself:

```python
fill = pgmenu.animation.AnimateTuple((42, 220), (120, 60), (205, 90),
                                     duration=0.2,
                                     curve=pgmenu.animation.circ)

button = pgmenu.button.Button(screen, (20, 20), (120, 32), fill=fill)
```

The stock `m_animation_on_hover` already calls `self.fill.update(pgmenu.FORWARD)`, so the
button now transitions from blue to orange on hover with no further code.

---

## C10. An animated panel that survives resizing

```python
def make_panel(size):
    idle = pgmenu.draw.aarect(None, (63, 68, 72), (0, 0, *size))
    hot  = pgmenu.draw.aarect(None, (68, 72, 77), (0, 0, *size))
    return pgmenu.animation.AnimateSurface(idle, hot, 0, 255, 0.3,
                                           pgmenu.animation.circ)


panel = pgmenu.surface.Surface(frame, make_panel((200, 100)), (10, 150))

panel.on_resize  = lambda: setattr(panel, "surface", make_panel(panel.size))
panel.on_hover   = lambda: panel.surface.update(pgmenu.FORWARD)
panel.on_standby = lambda: panel.surface.update(pgmenu.BACKWARD)
```

Rebuilding in `on_resize` is sharper than the default `smoothscale` path and keeps the
`AnimateSurface` alive.

---

## C11. A full-width top bar

```python
bar = pgmenu.frame.Frame(screen, (0, 0), (screen.get_width(), 48),
                         border_radius=0)
bar.responsive_size = pgmenu.STRETCH
bar.responsive_size_h = False     # keep the 48 pixel height
bar.responsive_coords = False     # pinned to the top left
```

---

## C12. Resize the window from code

`pygame.display.set_mode` does not emit `VIDEORESIZE`. Post it:

```python
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE))
```

---

## C13. Fullscreen toggle

```python
for event in events:
    screen = pgmenu.display.fullscreen_controls(screen, event)
```

F11 toggles. Reassigning `screen` matters: the display surface object changes.

Widgets hold a reference to the old surface in `master`. Recreate them, or keep the UI inside
a `Frame` whose master you can reassign:

```python
frame.master = screen
```

---

## C14. A transparent overlay window (Windows)

```python
pgmenu.display.set_transparent_colorkey((255, 0, 255))

# in the loop
screen.fill((255, 0, 255))    # this colour becomes a hole through the window
pgmenu.draw_all()
```

Use `pgmenu.display.set_transparent_window(180)` for uniform translucency instead.

---

## C15. Performance tuning

| Symptom | Cause | Fix |
| --- | --- | --- |
| Steady frame rate drop with animation | Every animated value is a distinct cache key | Set `animation_precision` to `0` or `1` in the theme |
| Frame rate collapse only while dragging the window edge | Every intermediate size regenerates every rectangle | Expected; consider disabling `responsive_size` on decorative widgets |
| Memory climbing | Large surfaces filling the caches | Lower `pgmenu.system.max_cache_size` |
| Timing lines printed to stdout | `debug` is on for a shape being regenerated every frame | Turn `aarect_debug` off, and check why the cache is missing |
| Corner artifacts on outlined rectangles | Known limitation of the subtractive corner pass | Reduce `aa_strength`, or use a filled shape with a separate outline |

The rule of thumb: pgmenu is cheap when values repeat. Anything that produces a new
`(fill, size, radius, ...)` combination every frame will rebuild a surface every frame.

---

## C16. Introspecting the widget tree

```python
for widget in pgmenu.vars.widgets:
    print(f"{widget.type:>8}  state={widget.state:<8} "
          f"size={widget.size}  coords={widget.coords}  rect={widget.rect}")

print("draw order:", [w.type for w in pgmenu.vars.widgets_draw_order])
print("cache sizes:", {k: len(v) for k, v in pgmenu.vars.cache.items()})
```

---

## C17. Reacting to a click without a `Button`

```python
panel = pgmenu.surface.Surface(screen, my_surface, (20, 20))

def clicked():
    print("panel clicked")

panel.on_press = clicked
```

`Surface` does not currently dispatch press events; only `Button` does. Either subclass
`Surface` and add a `update()` mouse branch (see the `Button.update` body for the pattern), or
test `panel.rect.collidepoint(...)` in your own event loop.
