# pgmenu

**A retained-mode GUI and widget toolkit for pygame, with animation, theming and antialiased drawing built in.**

pgmenu sits on top of `pygame` and gives it what pygame deliberately leaves out: widgets, a
theme system, animation, antialiased rounded rectangles, responsive layout, and a collection
of quality-of-life helpers for text, fullscreen handling and window manipulation.

The library is *retained mode*. You create widgets once, they register themselves globally,
and from then on two calls inside your existing pygame loop keep them alive:

```python
pgmenu.draw_all()
pgmenu.update(events)
```

---

## The one-paragraph description

pgmenu is a pure-Python widget layer for pygame. Widgets (`Label`, `Surface`, `Frame`,
`Button`, with `Checkbox` and `RadioButton` in development) are declared once and driven by a
global draw/update pass. Four things distinguish it from a plain "draw a rectangle and check
`collidepoint`" approach:

1. **Animation is the default, not an add-on.** Every numeric, tuple or surface attribute
   assigned to a widget is transparently wrapped in an animation object that still behaves
   like the raw `int`, `tuple` or `Surface` it replaced. Hover growth, colour transitions and
   corner-radius interpolation happen without the user writing a single line of animation code.
2. **Everything has a theme default.** A JSON theme file supplies the default value of every
   argument of every module, can be swapped at runtime, supports comments, and can express
   Python types (functions, methods, images, references to other attributes) inside JSON.
3. **Drawing is done from scratch.** `AARect` renders antialiased rounded rectangles with
   independent per-corner radii, outlines, inner fills, surface fills and tunable antialiasing
   strength, all behind an LRU cache so repeated frames cost close to nothing.
4. **Layout is responsive.** Widgets track a *base* geometry and rescale proportionally or by
   stretch whenever the window (or their parent `Frame`) is resized.

---

## Status

| Area | State |
| --- | --- |
| Core loop, widget registry, states | Stable |
| `Label`, `Surface`, `Frame`, `Button` | Implemented |
| `Checkbox` | Skeleton, not exported from `__init__.py` |
| `RadioButton` | Constant reserved only |
| Animation (`Animate`, `AnimateTuple`, `AnimateSurface`, `AnimateMultiple`) | Implemented |
| Theme engine and `DEFAULT` theme | Implemented |
| `MODERN` theme | Experimental, key names do not follow the theme convention |
| `AARect` drawing | Implemented, known corner artifacts with outlines |
| Responsive resize | Implemented |
| `Menu` | Minimal |
| `projects.MovablePlaneWindow` | Demo quality |
| `display.set_transparent_*` | Windows only |
| `draw.gradient`, `projects.modern_ui` | Stubs |

---

## Documentation map

| Document | What it covers |
| --- | --- |
| [01 Introduction](docs/01-introduction.md) | What pgmenu is, goals, design philosophy, module map |
| [02 Getting started](docs/02-getting-started.md) | Install, first window, anatomy of the loop, `PgmenuWindow` |
| [03 Architecture](docs/03-architecture.md) | Registry, draw order, update loop, blit tree, caching, frame lifecycle |
| [04 Widgets](docs/04-widgets.md) | `Widget`, mixins, states, callbacks, and every concrete widget |
| [05 Animation](docs/05-animation.md) | Curves, `Animate`, `AnimateTuple`, `AnimateSurface`, `AnimateMultiple`, quirks |
| [06 Theming](docs/06-theming.md) | Theme files, special JSON types, resolution rules, full attribute table |
| [07 Responsive resize](docs/07-responsive-resize.md) | Base geometry, `PROPORTIONAL` vs `STRETCH`, the `resize()` contract |
| [08 Drawing and text](docs/08-drawing-and-text.md) | `draw.aarect`, `AARect` internals, text rendering and fitting, rect/position helpers |
| [09 Menus and utilities](docs/09-menus-and-utilities.md) | `Menu`, `display`, `simple`, `projects`, `system`, `utils` |
| [10 Extending pgmenu](docs/10-extending.md) | Writing a new widget, new mixin, new curve, new theme |
| [11 Cookbook](docs/11-cookbook.md) | Task-oriented recipes |
| [12 API reference](docs/12-api-reference.md) | Exhaustive per-module signature listing |
| [13 Known issues and roadmap](docs/13-known-issues.md) | Confirmed bugs, sharp edges, planned work |
| [DOCSTRINGS](DOCSTRINGS.md) | Proposed in-library docstrings for every function and method |
| [REVIEW](REVIEW.md) | Code review: bugs found, fixes proposed, structural suggestions |

---

## Quickstart

```python
import pygame
import pgmenu

pygame.init()
screen = pygame.display.set_mode((640, 360), pygame.RESIZABLE)
clock = pygame.time.Clock()


def start_game():
    print("Start")


button = pgmenu.button.Button(screen,
                              coords=(270, 165),
                              size=(100, 30),
                              text="Play",
                              on_release=start_game)

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

That button already grows on hover, shrinks on press, brightens its fill, interpolates its
corner radius, fits its label to its own box, and rescales itself when the window is resized.
None of that needed configuration.

---

## Requirements

* Python 3.10 or newer (the code uses `int | float` union syntax in annotations).
* `pygame` (uses `pygame.gfxdraw`, `pygame.transform.smoothscale`, `pygame.font`).
* Windows only for `pgmenu.display.set_transparent_window` and
  `pgmenu.display.set_transparent_colorkey`. See
  [Known issues](docs/13-known-issues.md) regarding the unconditional `ctypes.wintypes`
  import.
