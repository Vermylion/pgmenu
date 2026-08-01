# 1. Introduction

## 1.1 What pgmenu is

pgmenu is a widget toolkit written in pure Python on top of `pygame`. It is aimed at anyone
building a game or a tool with pygame who needs menus, buttons, panels, labels and images
that look modern, animate smoothly, and survive a window resize, without pulling in a
heavyweight external UI framework or writing the same rounded-rectangle code for the tenth
time.

The name comes from its origin (menus for pygame) but the scope is broader: pgmenu is a
general widget and drawing layer, plus a set of pygame quality-of-life utilities that are
useful even if you never instantiate a widget (`pgmenu.text`, `pgmenu.draw`,
`pgmenu.display`, `pgmenu.position`, `pgmenu.rect`).

## 1.2 What pgmenu is trying to accomplish

Four goals show through consistently in the codebase.

### Goal 1: things should animate without being asked to

Most GUI libraries treat animation as an optional layer bolted on top of static values.
pgmenu inverts that. `Widget.__setattr__` intercepts every attribute assignment and, if the
value is a number, a numeric tuple or a `pygame.Surface`, replaces it with an animation
object whose *final* value is the base value multiplied by `animation_scale`. The animation
objects are written to be drop-in replacements for the types they wrap, so the rest of the
library keeps treating them as plain numbers and tuples.

The consequence: a widget author writes `self.size.update(pgmenu.FORWARD)` in an
`m_animation_on_hover` hook and gets a smooth, curve-driven, time-based grow effect. A
library user writes nothing at all and still gets it.

### Goal 2: every default should live in one editable place

Every public function argument in pgmenu defaults to the sentinel `pgmenu.THEME`. At call
time, `pgmenu.theme.resolve` swaps that sentinel for the corresponding value from the loaded
theme, and falls back to a code-level default only when the theme deliberately leaves the
attribute `null`. The result is that the entire visual identity of an application is a single
JSON file, hot-swappable at runtime with `pgmenu.Theme.load("MY_THEME")`.

### Goal 3: drawing quality pygame does not offer out of the box

`pygame.draw.rect` supports `border_radius` but produces hard, aliased corners.
`pgmenu.aarect.AARect` reimplements rounded rectangles from scratch:

* independent radius per corner,
* outlines of arbitrary width with a separately configurable inner fill,
* a fill that can be a colour, a `pygame.Color`, an animated tuple or a full `pygame.Surface`
  (a gradient image, for example) that is smoothscaled into the shape,
* an antialiasing pass with adjustable strength (`aa_strength` = number of blended pixels),
* per-corner and per-rectangle LRU caching so a static widget costs one blit per frame.

### Goal 4: a UI that survives a resizable window

Widgets record `base_size` and `base_coords` the first time (and every user-driven time) they
are set. On `pygame.VIDEORESIZE` the library recomputes the widget's geometry from the ratio
between the current master size and the master's base size, either preserving aspect ratio
(`pgmenu.PROPORTIONAL`) or filling both axes independently (`pgmenu.STRETCH`). Font sizes,
corner radii and images all follow.

## 1.3 Design philosophy in practice

**Retained mode with a global registry.** Instantiating a widget appends it to
`pgmenu.vars.widgets` and `pgmenu.vars.widgets_draw_order`. There is no root object to own
the tree; the display surface or a `Frame` is passed as `master` and everything else is
implicit. This keeps the smallest program small.

**Duck typing over wrappers.** `Animate` implements `__int__`, `__float__`, `__round__`,
`__index__`, comparisons and the full arithmetic operator set. `AnimateTuple` implements
`__len__`, `__iter__`, `__getitem__` and concatenation. `AnimateSurface` *subclasses*
`pygame.Surface`. Existing pygame code keeps working when handed one of these.

**Mixins for cross-cutting attribute families.** `RectMixin` contributes the border radius,
antialiasing and inner-fill family; `TextMixin` contributes the text styling family. A widget
opts in by inheriting, and `Widget._init_mixins` walks the MRO calling each `_mixin_init`.
`Widget.__setattr__` similarly dispatches to every `_mixin_setattr_hook` found in the MRO.

**Caching everywhere something is expensive.** Five LRU caches live in `pgmenu.vars.cache`:
`aarect`, `aarect_corner`, `text`, `surface`, `rect`. The `Cache` class normalises animation
objects to their current value so animated arguments still produce stable, hashable keys.

## 1.4 Module map

| Module | Role |
| --- | --- |
| `pgmenu/__init__.py` | Package assembly; imports every submodule and calls `lib.init()` |
| `pgmenu/lib.py` | The engine: `init`, `_draw`, `draw_all`, `update`, `request_cursor` |
| `pgmenu/constants.py` | All string constants (states, directions, widget types, sentinels) |
| `pgmenu/vars.py` | Mutable global runtime state (registry, caches, cursor, window sizes) |
| `pgmenu/system.py` | User-tunable engine settings (`widget_draw_priority`, `max_cache_size`) |
| `pgmenu/cache.py` | `Cache` (animation-aware `OrderedDict`) and the LRU helpers |
| `pgmenu/theme.py` | `Theme` class, JSON loading/saving, `resolve*` helpers |
| `pgmenu/animation.py` | Easing curves and the four animation object types |
| `pgmenu/widget.py` | `add()`, `Widget` base class, `RectMixin`, `TextMixin` |
| `pgmenu/label.py` | `Label` widget |
| `pgmenu/surface.py` | `Surface` widget and the cached `resize()` helper |
| `pgmenu/frame.py` | `Frame` widget (container and blit target) |
| `pgmenu/button.py` | `Button` widget |
| `pgmenu/checkbox.py` | `Checkbox` widget (in development) |
| `pgmenu/aarect.py` | `AARect` renderer and a theme-free `aarect()` function |
| `pgmenu/draw.py` | Theme-aware `aarect()` entry point, `gradient()` stub |
| `pgmenu/text.py` | Font matching, multi-line rendering, auto-fitting, animated fitting |
| `pgmenu/rect.py` | `fit_rects`, `center_rects` |
| `pgmenu/position.py` | `center_coords`, `place()` stub |
| `pgmenu/resize.py` | Responsive resize implementation |
| `pgmenu/display.py` | Fullscreen toggle, transparent window helpers (Windows) |
| `pgmenu/menu.py` | `Menu` grouping object |
| `pgmenu/simple.py` | `PgmenuWindow`, a tkinter-level convenience wrapper |
| `pgmenu/projects.py` | Skeleton projects, currently `MovablePlaneWindow` |
| `pgmenu/utils.py` | Alpha blending lookup table and helpers |
| `pgmenu/themes/*.json` | Theme files (`DEFAULT`, `FULL-DEFAULT`, `MODERN`) |

Files named `Debug*.py` in the repository are development scratch pads, not part of the
public API. They are useful as live examples and are described in
[the cookbook](11-cookbook.md#c1-reading-the-debug-scripts).

## 1.5 Vocabulary

| Term | Meaning |
| --- | --- |
| **master** | The surface a widget draws onto: either the display surface or a `Frame` |
| **state** | One of `NORMAL`, `HOVERED`, `ACTIVE`, `DISABLED`, `HIDDEN` |
| **base value** | The user-assigned, pre-animation, pre-resize value of an attribute |
| **final value** | The value an animation reaches at the end of its forward run |
| **reach** | A 0..1 cap on how far along its curve an animation is allowed to travel |
| **animation scale** | Multiplier that produces an attribute's final value from its base |
| **surface size** | The measured size of what a widget actually drew, as opposed to `size` |
| **THEME** | Sentinel meaning "look this argument up in the loaded theme" |
| **UNSET** | Sentinel meaning "I have no opinion, let the callee decide" |
