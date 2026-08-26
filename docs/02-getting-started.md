# 2. Getting started

## 2.1 Requirements and installation

pgmenu is a plain Python package. It requires:

* **Python 3.10+**, because annotations use the `int | float` union syntax at runtime in
  function signatures.
* **pygame**, including `pygame.gfxdraw` and `pygame.font`.
* A `themes/` directory next to `pgmenu/__init__.py` containing at least `DEFAULT.json`, and
  the bundled font `VarelaRound.ttf` next to `text.py`.

Expected layout:

```
your_project/
    pgmenu/
        __init__.py
        lib.py
        ...
        VarelaRound.ttf
        themes/
            DEFAULT.json
            FULL-DEFAULT.json
            MODERN.json
    main.py
```

Then:

```python
import pgmenu
```

Importing the package runs `pgmenu.lib.init()`, which:

1. constructs `pgmenu.Theme` as a `pgmenu.theme.Theme` instance,
2. loads `themes/DEFAULT.json` into it,
3. sets the starting cursor.

There is no separate initialisation call for you to make. You do still need `pygame.init()`
and a display surface before you create widgets, because widget construction touches
`pygame.display.get_surface()` for master validation and may render text.

> **Import order note.** `pgmenu` imports `pgmenu.display`, which imports `ctypes.wintypes`
> at module level. On non-Windows platforms that import can fail and take the whole package
> down with it. See [Known issues](13-known-issues.md#k1-unconditional-ctypeswintypes-import).

## 2.2 The smallest complete program

```python
import pygame
import pgmenu

pygame.init()
screen = pygame.display.set_mode((480, 270), pygame.RESIZABLE)
clock = pygame.time.Clock()

label = pgmenu.label.Label(screen, coords=(20, 20), text="Hello pgmenu", size=28)

running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pgmenu.Theme.bgcolor)

    pgmenu.draw_all()
    pgmenu.update(events)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

## 2.3 Anatomy of the loop

Every pgmenu program has the same five-step body. Order matters.

```python
events = pygame.event.get()      # 1. collect events ONCE
screen.fill(pgmenu.Theme.bgcolor)  # 2. clear
pgmenu.draw_all()                # 3. draw every registered widget
pgmenu.update(events)            # 4. hit testing, callbacks, animation triggers, resizing
pygame.display.flip()            # 5. present
```

**1. Collect events once.** `pygame.event.get()` drains the queue. If you call it twice per
frame, the second call returns nothing and pgmenu never sees your clicks. Store the list and
pass it to `pgmenu.update`.

**2. Clear.** `pgmenu.Theme.bgcolor` is the theme's background colour, present so your clear
colour follows your theme.

**3. `pgmenu.draw_all()`.** Iterates `pgmenu.vars.widgets_draw_order`, skips `HIDDEN`
widgets, and calls `draw()` on each. `draw()` is what produces `widget.surface` and blits it
to the widget's master.

**4. `pgmenu.update(events)`.** This is where the library does its real work:

* On the very first call it records `pgmenu.vars.base_window_size`, the reference size used
  by every responsive calculation. This is why the responsive system needs at least one frame
  before it is meaningful.
* Normalises `events`: a single `pygame.event.Event` is accepted as well as a list, and an
  empty list is padded with one dummy event so per-event widget code still runs every frame.
* Caches the mouse position once into `pgmenu.vars.mouse_x/mouse_y`.
* For each widget that is not `DISABLED`, not `HIDDEN` and was drawn this frame: performs
  hit testing against `widget.rect`, applies the resulting state transition, fires
  `on_hover`/`animation_on_hover` or `on_standby`/`animation_on_standby`, asks the widget for
  its cursor, runs the responsive resize check per event, then calls `widget.update(event)`.
* Applies the cursor and clears the per-frame cursor requests.

**5. Present.** `pygame.display.flip()` and `clock.tick(fps)` as usual.

> Widgets that were not drawn this frame are skipped by `update`. This is deliberate: a
> widget with a stale `rect` should not receive hover events. It also means calling
> `pgmenu.update` without `pgmenu.draw_all` does nothing useful.

## 2.4 Creating widgets

Every widget takes `master` as its first positional argument. `master` must be either the
display surface returned by `pygame.display.set_mode`, or a `pgmenu.frame.Frame`. Anything
else raises `ValueError` from `Widget.__setattr__`.

```python
frame  = pgmenu.frame.Frame(screen, coords=(40, 40), size=(400, 200))
label  = pgmenu.label.Label(frame, coords=(20, 20), text="Settings", size=24)
button = pgmenu.button.Button(frame, coords=(20, 150), size=(120, 32), text="Apply")
```

Assigning a `Frame` as master automatically calls `frame.add(widget)`, so you never register
children manually.

Every other argument defaults to `pgmenu.THEME`, meaning "use the loaded theme's value". You
only pass what you want to override.

## 2.5 Reacting to input

Widgets expose two parallel families of callbacks: **action** hooks (`on_*`) and **animation**
hooks (`animation_on_*`). Both can be passed as constructor keyword arguments or assigned
later.

```python
def apply_settings():
    print("applied")

button = pgmenu.button.Button(screen, (20, 20), (120, 32),
                              text="Apply",
                              on_release=apply_settings)

# or later
button.on_hover = lambda: print("hovering")
```

The full list of hooks is in [Widgets](04-widgets.md#44-callbacks).

> `Button` ships with a default `m_on_release` that prints `"Button pressed"`. Override
> `on_release` in production code. See [Known issues](13-known-issues.md#k9-button-prints-by-default).

## 2.6 Using `PgmenuWindow` instead of writing the loop

`pgmenu.simple.PgmenuWindow` wraps window creation, the event loop, fullscreen handling and
the draw/update pair, in the spirit of tkinter's `mainloop`.

```python
import pgmenu

window = pgmenu.simple.PgmenuWindow((400, 400), title="Demo", fps=120)
screen = window.screen

button = pgmenu.button.Button(screen, (150, 185), (100, 30), text="Click")


def loop():
    pgmenu.text.write(screen, (10, 10), str(round(window.clock.get_fps())))


window.loop(loop)
```

`PgmenuWindow.loop(callback)` runs the callback after clearing and before drawing widgets, so
anything drawn there sits underneath the UI. `PgmenuWindow` is explicitly marked in-source as
a demonstration of what the API could look like; treat it as convenience, not as the
supported path for a complex app.

## 2.7 Making the window resizable

Two things are needed:

1. Create the display with `pygame.RESIZABLE`.
2. Let `pygame.VIDEORESIZE` events reach `pgmenu.update`.

Everything else is automatic; widgets default to `responsive_size = PROPORTIONAL` and
`responsive_coords = STRETCH` from the theme. To opt a widget out:

```python
button.responsive_size = False
button.responsive_coords = False
```

See [Responsive resize](07-responsive-resize.md) for the full model.

## 2.8 Fullscreen

`pgmenu.display.fullscreen_controls` implements an F11 toggle. It must be called per event,
inside your event loop, and it returns the (possibly new) display surface:

```python
for event in events:
    screen = pgmenu.display.fullscreen_controls(screen, event)
```

`PgmenuWindow` already does this for you.

## 2.9 Switching theme at runtime

```python
pgmenu.Theme.load("MODERN")
```

Theme values are read at widget construction time and at draw time depending on the
attribute, so a mid-run reload affects newly created widgets immediately and existing widgets
only for attributes they re-resolve. To fully re-theme a live UI, reload the theme and then
re-create the widgets. See [Theming](06-theming.md#65-runtime-theme-switching).

## 2.10 Where to go next

* You want to know what happens between `draw_all()` and `flip()`: [Architecture](03-architecture.md).
* You want the list of widgets and their attributes: [Widgets](04-widgets.md).
* You want to control animation explicitly: [Animation](05-animation.md).
* You want to write your own widget: [Extending pgmenu](10-extending.md).
