# Proposed in-library documentation

This document contains a docstring for every function and method in pgmenu, plus a small set
of comments for the places where the code is genuinely hard to follow without them.

**No code was modified.** Everything here is a proposal, formatted so it can be pasted
directly under the corresponding `def` line. Bodies are elided as `...`; only the signature is
shown so the insertion point is unambiguous.

---

## Conventions used

**Accessors.** pgmenu defines one `get_<attribute>()` per public attribute. They are
mechanical and all share one form. Rather than repeating it sixty times, apply this rule:

```python
def get_border_radius(self):
    """Return the widget's ``border_radius``."""
    ...
```

That is, `"""Return the widget's ``<attribute>``."""` for widget accessors, and
`"""Return the animation's ``<attribute>``."""` for animation accessors. The few accessors
whose name does not match a plain attribute are given explicit docstrings below.

**Style.** Sphinx-compatible `:param:` / `:return:` fields, matching the style already used in
`draw.aarect`, `rect.fit_rects` and `text.fit_size`.

**`THEME` arguments.** Every parameter documented as "themeable" defaults to `pgmenu.THEME`
and is resolved against the loaded theme. Rather than repeating that on each parameter, each
affected function's docstring says so once.

---

## `constants.py`

No functions. Proposed module docstring:

```python
"""
String constants used throughout pgmenu.

Constants are plain lowercase strings so that they can be written directly into theme
files and compared cheaply. Groups:

* widget states: NORMAL, HOVERED, ACTIVE, DISABLED, HIDDEN
* animation directions: FORWARD, BACKWARD
* easing curve directions: IN, OUT, IN_OUT
* widget type tags: WIDGET, LABEL, SURFACE, FRAME, BUTTON, CHECKBOX, RADIOBUTTON
* argument sentinels: THEME (resolve from the theme), UNSET (defer to the callee)
* responsive resize modes: PROPORTIONAL, STRETCH
"""
```

---

## `vars.py`

No functions. Proposed module docstring:

```python
"""
Mutable global runtime state shared by the whole library.

Nothing here is configuration; user-facing settings live in pgmenu.system. These values
are written by the engine during the draw and update passes and may be read for
introspection.
"""
```

---

## `system.py`

No functions. The existing comments are adequate; consider adding:

```python
"""
User-tunable engine settings.

Assign to these directly, for example ``pgmenu.system.max_cache_size = 100``. They take
effect on the next draw or update pass.
"""
```

---

## `cache.py`

```python
class Cache(OrderedDict):
    """
    An ordered dict whose keys tolerate animation objects.

    pgmenu builds cache keys out of live widget attributes, many of which are AnimateType
    instances rather than plain numbers. Those objects are unhashable in practice (their
    value changes every frame) so every tuple key is normalised on the way in and out:
    each AnimateType element is replaced by its current ``.value``.
    """

    def _normalize(self, key):
        """
        Return ``key`` with any AnimateType element replaced by its current value.

        :param key: cache key; only tuples are normalised, other types pass through
        :return: a hashable, animation-free equivalent of ``key``
        """
        ...

    def __setitem__(self, key, value):
        """Store ``value`` under the normalised form of ``key``."""
        ...

    def __getitem__(self, key):
        """Return the value stored under the normalised form of ``key``."""
        ...

    def __contains__(self, key):
        """Return whether the normalised form of ``key`` is present."""
        ...

    def get(self, key, default=None):
        """Return the value under the normalised ``key``, or ``default``."""
        ...

    def move_to_end(self, key, last=True):
        """Move the normalised ``key`` to either end of the ordering."""
        ...


def lru_get(cache, key):
    """
    Look a key up and mark it as recently used.

    :param cache: a Cache instance from pgmenu.vars.cache
    :param key: cache key
    :return: the cached value, or None if absent
    """
    ...


def lru_set(cache, key, value):
    """
    Insert a value and evict the least recently used entry if the cache is over budget.

    The budget is pgmenu.system.max_cache_size and applies per cache, not globally.

    :param cache: a Cache instance from pgmenu.vars.cache
    :param key: cache key
    :param value: value to store
    """
    ...


def clear_cache():
    """Empty every cache held in pgmenu.vars.cache."""
    ...
```

---

## `utils.py`

```python
def only_alpha_blending(source_alpha, dest_alpha):
    """
    Return the alpha resulting from blending ``source_alpha`` over ``dest_alpha``.

    Only the alpha channel is considered. AARect uses this to pre-compensate for an alpha
    value passing through several intermediate surfaces before reaching the destination.

    :param source_alpha: alpha of the source pixel, 0..255
    :param dest_alpha: alpha of the destination pixel, 0..255
    :return: the blended alpha
    """
    ...


def div(a, b, round_num=None):
    """
    Divide ``a`` by ``b`` without raising on a zero denominator.

    :param a: numerator
    :param b: denominator
    :param round_num: if not None, round the result to this many decimals
    :return: the quotient, or float('inf') when ``b`` is zero
    """
    ...
```

Proposed comment above `sub_values`, extending the existing one:

```python
# Lookup table inverting pygame's BLEND_RGBA_SUB blending.
# Key: the alpha we want to end up subtracting. Value: the alpha that must actually be
# written to the mask surface so that the subtraction produces that result.
```

---

## `theme.py`

```python
class Theme:
    """
    Container for every default value in the library.

    A single instance lives at ``pgmenu.Theme``, created and populated by pgmenu.lib.init.
    Attribute names follow ``[module or widget]_[attribute]``, for example
    ``button_fill`` or ``text_size``. Loading is additive: a theme file only needs to
    declare the keys it changes.
    """

    def __init__(self):
        """Create an empty theme. Call load() to populate it."""
        ...

    def set(self, **attrs):
        """
        Apply an attribute map to this theme.

        Handles four things beyond a plain setattr:

        * keys named "#" are comments and are skipped
        * keys prefixed "widgets_" are expanded onto every widget-prefixed key present,
          following file order so that a later specific key wins
        * dict values are special types and are converted: method, function, attribute,
          variable, image, exec (see the theming documentation)
        * lists are converted to tuples, because cache keys must be hashable

        :param attrs: attribute name to value mapping, typically a parsed theme file
        """
        ...

    def save(self, theme, **attrs):
        """
        Write the given attributes to ``themes/<theme>.json``.

        :param theme: theme name, with or without the .json extension
        :param attrs: attributes to write
        """
        ...

    def save_all(self, theme):
        """
        Write every attribute currently held by this theme to ``themes/<theme>.json``.

        Only themes made entirely of JSON-serialisable values can be saved this way;
        loaded surfaces and function objects cannot be encoded.

        :param theme: theme name, with or without the .json extension
        """
        ...

    def load(self, theme="DEFAULT"):
        """
        Read ``themes/<theme>.json`` and apply it through set().

        Loading is additive and can be repeated at any point during runtime. Attributes
        already resolved by existing widgets are not retroactively updated.

        :param theme: theme name, with or without the .json extension
        """
        ...


def _format_theme_path(theme):
    """
    Normalise a theme name and resolve its file path.

    :param theme: theme name, with or without the .json extension
    :return: (theme name without extension, absolute path to the theme file)
    """
    ...


def resolve(value, theme_attr, default=None):
    """
    Resolve an argument against the theme.

    ``pgmenu.THEME`` means "use the theme value". ``pgmenu.UNSET`` means "I have no
    opinion" and is treated the same way, which lets a caller forward an argument down a
    layer without overriding that layer's own default. A theme attribute of None counts
    as absent and falls through to ``default``; this is the convention used for values
    that depend on their context, such as a border radius derived from the widget size.

    :param value: the caller's value, possibly THEME or UNSET
    :param theme_attr: the corresponding theme attribute
    :param default: fallback used when the theme leaves the attribute undefined
    :return: the resolved value
    """
    ...


def resolve_kwarg(kwargs, key, theme_attr, default=None):
    """
    resolve() for an optional keyword argument.

    An absent key is treated as THEME, so omitting it selects the theme value.

    :param kwargs: the receiving function's keyword arguments
    :param key: keyword name
    :param theme_attr: the corresponding theme attribute
    :param default: fallback used when the theme leaves the attribute undefined
    :return: the resolved value
    """
    ...


def resolve_widget(kwargs, key, widget_type, default=None):
    """
    resolve_kwarg() against a per-widget-type theme attribute.

    The theme attribute is looked up dynamically as ``{widget_type}_{key}``, so a theme
    can override one widget type without every widget declaring every possible key. A
    missing attribute falls through to ``default``.

    :param kwargs: the widget's keyword arguments
    :param key: attribute name without the widget prefix
    :param widget_type: one of the widget type constants, normally self.type
    :param default: fallback used when the theme defines no such attribute
    :return: the resolved value
    """
    ...
```

---

## `animation.py`

Proposed module docstring (extending the existing comment block):

```python
"""
Easing curves and animation objects.

Curves follow the easings.net catalogue. Each family function takes ``(x, direction)``
and dispatches to a concrete ``ease_{in,out,in_out}_{name}(x)`` implementation, where x
runs from 0 at the start of the animation to 1 at its end.

Animation objects are deliberately transparent: Animate behaves like a number,
AnimateTuple like a tuple, and AnimateSurface subclasses pygame.Surface, so existing code
keeps working when handed one.
"""
```

### Curves

Family dispatchers, one docstring each:

```python
def linear(x, direction=None):
    """
    Linear interpolation.

    :param x: normalised progress, 0..1
    :param direction: accepted for signature compatibility, ignored
    :return: the eased coefficient
    """
    ...


def sine(x, direction):
    """
    Sine easing. Dispatches to ease_{direction}_sine.

    :param x: normalised progress, 0..1
    :param direction: pgmenu.IN, pgmenu.OUT or pgmenu.IN_OUT
    :return: the eased coefficient
    """
    ...
```

The same docstring applies verbatim to `quad`, `cubic`, `quart`, `quint`, `expo`, `circ`,
`back`, `elastic` and `bounce`, replacing the family name and the shape description:

| Function | Shape description for the first line |
| --- | --- |
| `sine` | Sine easing |
| `quad` | Quadratic easing |
| `cubic` | Cubic easing |
| `quart` | Quartic easing |
| `quint` | Quintic easing |
| `expo` | Exponential easing |
| `circ` | Circular easing |
| `back` | Back easing, overshoots past the endpoint before settling |
| `elastic` | Elastic easing, oscillates around the endpoint |
| `bounce` | Bounce easing, rebounds against the endpoint |

Concrete implementations take one docstring line each:

```python
def ease_in_sine(x):
    """Sine easing with a slow start. Maps x in 0..1 to its coefficient."""

def ease_out_sine(x):
    """Sine easing with a slow finish. Maps x in 0..1 to its coefficient."""

def ease_in_out_sine(x):
    """Sine easing with a slow start and finish. Maps x in 0..1 to its coefficient."""
```

Repeat for every family, substituting the family name. Two implementations deserve an extra
line:

```python
def ease_in_bounce(x):
    """
    Bounce easing with the rebounds at the start.

    Defined as the mirror of ease_out_bounce, which holds the actual bounce maths.
    """

def ease_out_bounce(x):
    """
    Bounce easing with the rebounds at the end.

    The four branches are the four successive rebounds, each a shifted parabola of
    decreasing amplitude.
    """
```

### `AnimateType`

```python
class AnimateType:
    """
    Abstract base of every animation object.

    Its practical purpose is identification: ``isinstance(x, AnimateType)`` is the check
    used throughout the library to decide whether a value is already animated. It also
    declares the shared interface that Animate, AnimateTuple and AnimateSurface implement.
    """

    def __init__(self):
        """Base initialiser. Subclasses do not rely on it for state."""

    @property
    def value(self):
        """The animation's current value."""

    @property
    def base_value(self):
        """The value the animation starts from."""

    @property
    def final_value(self):
        """The value the animation ends at."""

    def init(self):
        """Start the animation clock."""

    def reset(self):
        """Return to the base value and clear all timing state."""

    def update(self, direction=pgmenu.FORWARD, reach=1):
        """
        Advance the animation.

        :param direction: pgmenu.FORWARD or pgmenu.BACKWARD
        :param reach: 0..1 cap on how far along the curve this run may travel
        """
```

(`get_value`, `get_base_value`, `get_final_value` follow the accessor convention.)

### `Animate`

```python
class Animate(AnimateType):
    """
    An animated number that behaves like a number.

    Implements the numeric conversions, all six comparisons and the full arithmetic
    operator set, so it can be passed anywhere an int or float is expected. Arithmetic
    returns plain numbers rather than new Animate objects.

    The value is recomputed from wall-clock time on every update() call:
    ``value = base + (final - base) * curve(step)``.
    """

    def __init__(self, base_num, final_num, duration=THEME, curve=THEME, precision=THEME):
        """
        :param base_num: value at the start of the animation
        :param final_num: value at the end of the animation
        :param duration: seconds for a full run; themeable, clamped above zero
        :param curve: easing callable taking (x) or (x, direction); themeable
        :param precision: decimals the value is rounded to, or None; themeable.
                          Rounding keeps cache keys stable across frames.
        """
        ...
```

Properties:

```python
    @property
    def value(self):
        """The current value."""

    @property
    def int(self):
        """The current value rounded to the nearest integer."""

    @property
    def float(self):
        """The current value as a float."""

    @property
    def base_value(self):
        """The value the animation starts from."""

    @property
    def final_value(self):
        """The value the animation ends at."""
```

Dunders worth documenting:

```python
    def _coerce(self, other):
        """Return ``other``'s current value if it is an animation, otherwise ``other``."""

    def __eq__(self, other):
        """Compare current values. Note that __hash__ uses identity, not value."""

    def __lt__(self, other):
        """Compare current values; total_ordering derives the remaining comparisons."""

    def __getattr__(self, name):
        """
        Forward unknown attribute lookups to the current value as a float.

        This makes float methods such as is_integer() available. The trade-off is that a
        misspelled attribute may silently resolve to a float attribute instead of raising.
        """
```

Methods:

```python
    def init(self):
        """Stamp the start time. Called automatically by the first update()."""

    def reset(self):
        """Return to the base value and clear timing, step and done state."""

    def update(self, direction=pgmenu.FORWARD, reach=1):
        """
        Advance the animation and return the new value.

        Changing direction or reach restarts the clock and clears ``done``. Switching to
        BACKWARD records the current step so the reverse run starts from wherever the
        forward run got to, rather than snapping to the end.

        Forward runs use the OUT curve direction and stop at ``reach``. Backward runs use
        IN and stop at ``1 - reach``, which is how a partial press-in effect is produced
        (see Button.m_animation_on_hold, which passes reach=0.15).

        :param direction: pgmenu.FORWARD or pgmenu.BACKWARD
        :param reach: 0..1 cap on travel along the curve
        :return: the new current value
        """
```

### `AnimateTuple`

```python
class AnimateTuple(AnimateType):
    """
    A tuple of animated numbers that behaves like a tuple.

    Holds one Animate per component and keeps four derived tuples in sync so callers can
    pick the representation they need without converting: base_tuple, final_tuple,
    int_tuple (for blitting) and float_tuple (the value).

    Iteration and indexing yield the underlying Animate objects, while ``value`` yields
    plain floats.
    """

    def __init__(self, *pairs, duration=THEME, curve=THEME, precision=THEME):
        """
        :param pairs: one (base_num, final_num) tuple per component
        :param duration: seconds for a full run; themeable
        :param curve: easing callable; themeable
        :param precision: decimals each component is rounded to, or None; themeable
        """
```

Properties:

```python
    @property
    def value(self):
        """The current values as a tuple of floats."""

    @property
    def tuple(self):
        """Alias of value."""

    @property
    def base_value(self):
        """The values the animation starts from."""

    @property
    def final_value(self):
        """The values the animation ends at."""
```

Protocol and control:

```python
    def __len__(self):
        """Number of components."""

    def __iter__(self):
        """Iterate the component Animate objects, not their values."""

    def __getitem__(self, index):
        """Return the component Animate at ``index``."""

    def __add__(self, other):
        """Concatenate the current values with another sequence."""

    def __radd__(self, other):
        """Concatenate another sequence with the current values."""

    def __eq__(self, other):
        """Compare current values against another animation or a plain sequence."""

    def __lt__(self, other):
        """Compare current values; total_ordering derives the remaining comparisons."""

    def init(self):
        """Start the clock on every component."""

    def reset(self):
        """Reset every component to its base value."""

    def update(self, direction=pgmenu.FORWARD, reach=1):
        """
        Advance every component and rebuild int_tuple and float_tuple.

        :param direction: pgmenu.FORWARD or pgmenu.BACKWARD
        :param reach: 0..1 cap on travel along the curve
        """
```

### `AnimateSurface`

```python
class AnimateSurface(pygame.Surface, AnimateType):
    """
    A cross-fade between two surfaces, usable anywhere a pygame.Surface is.

    Its own pixels are the composite of the two layers: update() clears them, sets the top
    layer's alpha from an internal Animate running between base_alpha and final_alpha, and
    blits base then final.

    Its dimensions come from max() of the two layer sizes, which compares tuples
    lexicographically rather than per axis; give both layers the same size.
    """

    def __init__(self, base_surface, final_surface, base_alpha=THEME, final_alpha=THEME,
                 duration=THEME, curve=THEME, precision=THEME):
        """
        :param base_surface: the layer that is always fully visible
        :param final_surface: the layer whose alpha is animated on top
        :param base_alpha: starting alpha of the top layer; themeable
        :param final_alpha: ending alpha of the top layer; themeable
        :param duration: seconds for a full run; themeable
        :param curve: easing callable; themeable
        :param precision: decimals the alpha is rounded to, or None; themeable
        """

    @property
    def value(self):
        """This surface itself, since it is its own composite."""

    @property
    def surface(self):
        """Alias of value."""

    @property
    def base_value(self):
        """The bottom layer."""

    @property
    def final_value(self):
        """The top layer."""

    def init(self):
        """Start the alpha animation clock."""

    def reset(self):
        """Reset the blend to the base surface only."""

    def update(self, direction=pgmenu.FORWARD, reach=1):
        """
        Advance the alpha animation and recomposite this surface.

        :param direction: pgmenu.FORWARD or pgmenu.BACKWARD
        :param reach: 0..1 cap on travel along the curve
        """
```

### `AnimateMultiple`

```python
class AnimateMultiple:
    """
    A remote control for several animation objects at once.

    Members are stored keyed by id(), so adding the same object twice is a no-op. Note
    that AnimateMultiple is not itself an AnimateType and has no init().
    """

    def __init__(self, *animations):
        """:param animations: the animation objects to control together"""

    @property
    def value(self):
        """List of the members' current values."""

    @property
    def base_value(self):
        """List of the members' base values."""

    @property
    def final_value(self):
        """List of the members' final values."""

    def modify(self, *animations):
        """Add animation objects to the group, replacing any already present."""

    def reset(self):
        """Reset every member."""

    def update(self, direction=pgmenu.FORWARD, reach=1):
        """Advance every member with the same direction and reach."""
```

---

## `widget.py`

```python
def add(widget):
    """
    Register a widget with the engine.

    Appends to pgmenu.vars.widgets, which sets update order, and inserts into
    pgmenu.vars.widgets_draw_order, which sets draw order. Frames are positioned by
    frame_handling() so that a container is drawn after the children that blit onto it.

    Called at the end of every widget's __init__; there is no need to call it manually.

    :param widget: the widget to register
    """
    ...
```

Proposed comment inside, replacing nothing and clarifying the nested helper:

```python
    # Frames are blit targets rather than real surfaces: children queue their surfaces
    # onto them during draw and the frame flushes the queue when it is drawn, so a frame
    # must come after its children in the draw order.
```

### `Widget`

```python
class Widget:
    """
    Base class for every pgmenu widget.

    Provides, in order of importance:

    * the attribute pipeline in __setattr__, which wraps numbers, numeric tuples and
      surfaces in animation objects, validates the master, tracks base geometry for the
      responsive system and dispatches to mixin hooks
    * the animation attributes (scale, duration, curve) and the two callback families
      (on_* actions and animation_on_* visuals), each resolved per widget type
    * the responsive flags and the base_size / base_coords bookkeeping
    * default draw(), update() and resize() behaviour

    Subclasses must set ``self.type`` before calling super().__init__(), because every
    theme lookup is keyed on ``{type}_{attribute}``.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs: any widget attribute; unrecognised keys are simply unused.
                       Commonly passed: animation_scale, animation_duration,
                       animation_curve, disable_animation, state, responsive_size,
                       responsive_coords, and any on_* or animation_on_* callback.
        """
        ...

    def __setattr__(self, key, value):
        """
        Assign an attribute, applying the widget attribute pipeline.

        Steps:

        1. Ignore the assignment if the attribute already holds an animation whose base
           value equals ``value``. This is what stops per-frame assignments from
           restarting animations.
        2. Wrap the value in an animation object unless it already is one:
           numbers become Animate, numeric sequences become AnimateTuple, and surfaces
           become AnimateSurface (only for the Surface widget, and never for master).
           Wrapping is skipped while the animation attributes themselves are still being
           initialised.
        3. Perform the actual assignment.
        4. Validate master: it must be the display surface or a Frame, and assigning a
           Frame registers this widget as one of its children.
        5. Mirror size and coords into base_size and base_coords, unless a responsive
           resize is in progress (pgmenu.vars.videoresized).
        6. Call every _mixin_setattr_hook found in the MRO.

        :param key: attribute name
        :param value: new value
        """
        ...

    def _update_rect(self, size, coords):
        """
        Recompute the hit-test rect from a size and position.

        For a widget inside a Frame, the coordinates are frame-relative, so they are
        offset by the frame position and the size is clipped to the frame bounds. A child
        overflowing its frame is therefore not clickable outside it.

        :param size: (width, height) in pixels, normally surface_size
        :param coords: (x, y), master-relative
        """
        ...

    def _init_mixins(self, **kwargs):
        """
        Run the _mixin_init of every class in the MRO that defines one.

        Called first in __init__ so mixin attributes exist before the widget body runs.
        Mixins should be flat: getattr follows inheritance, so a mixin subclassing another
        mixin would run the parent initialiser twice.

        :param kwargs: forwarded to each mixin initialiser
        """
        ...

    def _make_2d(self, value):
        """
        Normalise a value into a two-component form.

        Animation objects are unwrapped to their current value first, and a scalar is
        duplicated. Used so that widgets whose size is a single number, such as Label,
        can go through the same resize maths as widgets with a (w, h) size.

        :param value: scalar, sequence, or AnimateType
        :return: a two-component sequence
        """
        ...

    def _get_2d(self, key):
        """
        _make_2d applied to one of this widget's attributes.

        :param key: attribute name
        :return: the two-component form, or None if the attribute does not exist
        """
        ...

    def get_2d_size(self):
        """Return the current size as a two-component form."""
        ...

    def get_2d_base_size(self):
        """Return the base (pre-resize) size as a two-component form."""
        ...

    def modify(self, **kwargs):
        """
        Assign several attributes in one call.

        Each assignment goes through __setattr__ and therefore through the animation
        pipeline.

        :param kwargs: attribute name to value mapping
        """
        ...

    def draw(self):
        """
        Mark the widget as drawn for this frame.

        Subclasses call this first, then build self.surface and blit it to self.master.
        The flag gates the update pass: a widget that was not drawn receives no hover
        detection, callbacks or resize handling.
        """
        ...

    def update(self, event):
        """
        Measure the rendered surface and refresh the hit rect.

        Subclasses call this first, then handle the event. Because measurement happens
        after drawing, hit testing uses the previous frame's rendered size.

        :param event: a pygame event, or the engine's placeholder event on idle frames
        """
        ...

    def resize(self, w, h):
        """
        Apply a new size computed by the responsive system.

        The default does nothing. Overriding widgets should rescale dependent properties
        first, while base_size still holds the docs-archive value, and only then assign the new
        size.

        :param w: new width in pixels
        :param h: new height in pixels
        """
        ...
```

Hook stubs, one line each:

```python
    def m_animation_on_standby(self):
        """Default standby animation. No-op; override or replace animation_on_standby."""

    def m_animation_on_hover(self):
        """Default hover animation. No-op."""

    def m_animation_on_press(self):
        """Default press animation. No-op."""

    def m_animation_on_hold(self):
        """Default hold animation. No-op."""

    def m_animation_on_release(self):
        """Default release animation. No-op."""

    def m_animation_on_key_press(self, key):
        """Default key press animation. No-op. :param key: the pygame key code."""

    def m_animation_on_key_hold(self):
        """Default key hold animation. No-op."""

    def m_animation_on_key_release(self, key):
        """Default key release animation. No-op. :param key: the pygame key code."""

    def m_on_standby(self):
        """Default standby action. No-op; override or replace on_standby."""

    def m_on_hover(self):
        """Default hover action. No-op."""

    def m_on_press(self):
        """Default press action. No-op."""

    def m_on_hold(self):
        """Default hold action. No-op."""

    def m_on_release(self):
        """Default release action. No-op."""

    def m_on_key_press(self, key):
        """Default key press action. No-op. :param key: the pygame key code."""

    def m_on_key_hold(self, key):
        """Default key hold action. No-op. :param key: the pygame key code."""

    def m_on_key_release(self, key):
        """Default key release action. No-op. :param key: the pygame key code."""

    def m_on_resize(self):
        """Default resize action. No-op; called after the widget has been resized."""

    def request_cursor(self):
        """
        Claim a mouse cursor while this widget is hovered.

        Called every frame the cursor is over the widget. Implementations assign to
        pgmenu.vars.widget_cursor. The default does nothing, leaving the arrow.
        """
```

### `RectMixin`

```python
class RectMixin:
    """
    Contributes the rounded-rectangle attribute family to a widget.

    Adds the five border radii, the antialiasing settings and the inner fill settings,
    plus base_* mirrors of the radii and the helpers used to rescale and animate them.

    The inner_* attributes default to pgmenu.UNSET rather than to a concrete value, so
    that pgmenu.draw.aarect can apply its own fallbacks (inner_fill defaults to fill,
    inner_transparency to transparency, and so on).
    """

    def _mixin_init(self, **kwargs):
        """
        Resolve the rectangle attribute family from kwargs and the theme.

        Called by Widget._init_mixins, after self.type exists and before the widget body
        runs. border_radius is set to None here and assigned properly by the widget.

        :param kwargs: the widget's keyword arguments
        """
        ...

    def _mixin_setattr_hook(self, key, value):
        """
        Mirror radius assignments into their base_* counterparts.

        Skipped while a responsive resize is in progress, so the base radii keep their
        design-time values.

        :param key: attribute name being assigned
        :param value: value being assigned
        """
        ...

    def _resize_border_radii(self, w, h):
        """
        Rescale every radius for a new widget size.

        The factor is min(w / base_width, h / base_height), so corners stay circular
        rather than becoming elliptical. Call this before assigning the new size, because
        the factor is computed against the base size.

        :param w: new width in pixels
        :param h: new height in pixels
        """
        ...

    def _animation_update_border_radii(self, direction=pgmenu.FORWARD, reach=1):
        """
        Forward an animation update to every radius that is set.

        :param direction: pgmenu.FORWARD or pgmenu.BACKWARD
        :param reach: 0..1 cap on travel along the curve
        """
        ...
```

### `TextMixin`

```python
class TextMixin:
    """
    Contributes the text styling attribute family to a widget.

    Every attribute defaults to pgmenu.UNSET so that the pgmenu.text functions apply
    their own text_* theme defaults. The text content and colour are not part of the
    mixin, because they are content rather than styling and each widget names them
    differently.
    """

    def _mixin_init(self, **kwargs):
        """
        Resolve the text styling family from kwargs and the theme.

        :param kwargs: the widget's keyword arguments
        """
        ...
```

---

## `label.py`

```python
class Label(Widget):
    """
    A text widget.

    Supports multiple lines through "\\n", the full pygame font styling set, and optional
    centring around its coordinates. Its ``size`` is a font point size rather than a pixel
    box, so responsive resizing drives it from the height factor and hit testing uses the
    measured surface_size instead.
    """

    def __init__(self, master, coords=THEME, text=THEME, color=THEME, size=THEME,
                 font=THEME, background=THEME, antialias=THEME, italic=THEME, bold=THEME,
                 strikethrough=THEME, underline=THEME, transparency=THEME,
                 center_x=THEME, center_y=THEME, **kwargs):
        """
        All parameters except master are themeable through the label_* keys.

        :param master: the display surface or a Frame
        :param coords: (x, y) top-left, or the centre anchor when centring is enabled
        :param text: the string to render; "\\n" starts a new line
        :param color: text colour
        :param size: font point size
        :param font: font file path or system font name; None uses the bundled font
        :param background: solid colour drawn behind the glyphs, or None
        :param antialias: antialias the glyphs
        :param italic: render italic
        :param bold: render bold
        :param strikethrough: render struck through
        :param underline: render underlined
        :param transparency: surface alpha, 0..255
        :param center_x: treat coords[0] as a horizontal centre
        :param center_y: treat coords[1] as a vertical centre
        :param kwargs: forwarded to Widget
        """
        ...

    def draw(self):
        """
        Render the text and blit it to the master.

        Centring uses surface_size, which is measured during update(), so the frame in
        which the text changes is positioned with the previous metrics.
        """
        ...

    def resize(self, w, h):
        """
        Apply a responsive resize by treating the new height as the font size.

        The width is ignored, so a label can overflow a container that stretches
        horizontally.

        :param w: new width in pixels, unused
        :param h: new height in pixels, used as the font size
        """
        ...
```

---

## `surface.py`

```python
class Surface(Widget):
    """
    Wraps an arbitrary pygame.Surface as a widget.

    Gives any surface hit testing, callbacks, animation and responsive resizing. This is
    the only widget whose ``surface`` attribute is animated by the attribute pipeline:
    assigning a plain surface produces an AnimateSurface that cross-fades to a brightened
    copy, which is the default hover highlight.

    ``_surface`` shadows the last surface assigned by the user so that repeated resizes
    always scale from the original rather than compounding scaling artefacts.
    """

    def __init__(self, master, surface, coords=THEME, **kwargs):
        """
        :param master: the display surface or a Frame
        :param surface: the surface to display; a pygame.Surface or an AnimateSurface
        :param coords: (x, y), themeable through surface_coords
        :param kwargs: forwarded to Widget
        """
        ...

    def __setattr__(self, key, value):
        """
        Assign an attribute, keeping the ``_surface`` shadow in sync.

        :param key: attribute name
        :param value: new value
        """
        ...

    def draw(self):
        """Blit the current surface to the master."""
        ...

    def resize(self, w, h):
        """
        Scale the original surface to a new size.

        Scaling always starts from the shadow ``_surface``, which is restored afterwards
        so that the next resize is not a rescale of a rescale. This path replaces any
        AnimateSurface with a plain scaled surface; rebuild it from an on_resize callback
        to keep the animation.

        :param w: new width in pixels
        :param h: new height in pixels
        """
        ...

    def update(self, event):
        """
        Refresh the widget size from the current surface.

        :param event: a pygame event
        """
        ...


def resize(surface, size):
    """
    Scale a surface with smoothscale and cache the result.

    :param surface: source surface, may be an AnimateSurface
    :param size: target (width, height), may be an AnimateTuple
    :return: the scaled surface from the cache
    """
    ...
```

---

## `frame.py`

```python
class Frame(Widget, RectMixin):
    """
    A container widget: an antialiased rounded rectangle other widgets draw into.

    A Frame is a blit target rather than a real surface. Children call Frame.blit during
    their own draw, which queues the surface, and the frame flushes the queue when it is
    drawn. Children therefore use frame-relative coordinates, their hit rects are offset
    and clipped by Widget._update_rect, and the frame must be drawn after them.

    Frames nest: a Frame may itself be another Frame's master.
    """

    def __init__(self, master, coords=THEME, size=THEME, fill=THEME, width=THEME,
                 border_radius=THEME, **kwargs):
        """
        All parameters except master are themeable through the frame_* keys.

        :param master: the display surface or another Frame
        :param coords: (x, y) of the top-left corner
        :param size: (width, height)
        :param fill: colour, animated colour, or a surface scaled into the shape
        :param width: outline width in pixels; 0 fills the shape
        :param border_radius: corner radius; falls back to round(min(size) / 7)
        :param kwargs: forwarded to Widget and RectMixin
        """
        ...

    def add(self, *widgets):
        """
        Register children.

        Called automatically when a widget is given this frame as its master.

        :param widgets: widgets to add
        """
        ...

    def remove(self, *widgets):
        """
        Unregister children, ignoring any that are not present.

        This detaches from the frame's own list only; the widgets remain registered with
        the engine.

        :param widgets: widgets to remove
        """
        ...

    def blit(self, surface, coords):
        """
        Queue a child surface to be drawn onto this frame.

        The queue is keyed by surface object and is flushed and cleared by draw(), so it
        must be refilled every frame.

        :param surface: the child's rendered surface
        :param coords: (x, y) relative to this frame
        """
        ...

    def draw(self):
        """
        Render the frame, flush the child queue onto it, and blit it to the master.
        """
        ...

    def resize(self, w, h):
        """
        Apply a responsive resize, rescaling the corner radii first.

        :param w: new width in pixels
        :param h: new height in pixels
        """
        ...
```

---

## `button.py`

```python
class Button(Widget, RectMixin, TextMixin):
    """
    A clickable rounded rectangle with an auto-fitted label and an optional icon.

    The reference widget of the library: it exercises the rectangle renderer, the animated
    text fitting, the icon layout helpers, the three-state mouse handling and the stock
    hover, hold and standby animations.
    """

    def __init__(self, master, coords=THEME, size=THEME, fill=THEME, text=THEME,
                 text_color=THEME, icon=THEME, margin=THEME, width=THEME,
                 border_radius=THEME, **kwargs):
        """
        All parameters except master are themeable through the button_* keys.

        :param master: the display surface or a Frame
        :param coords: (x, y) of the top-left corner at the base size
        :param size: (width, height)
        :param fill: colour, animated colour, or a surface scaled into the shape
        :param text: label text
        :param text_color: label colour
        :param icon: a pygame.Surface drawn to the left of the label, or None
        :param margin: inner padding used when fitting the icon and label
        :param width: outline width in pixels; 0 fills the shape
        :param border_radius: corner radius; falls back to round(min(size) / 3)
        :param kwargs: forwarded to Widget, RectMixin and TextMixin
        """
        ...

    def draw(self):
        """
        Render the background, fit the label and icon into it, and blit to the master.

        The animated size is centred inside the base rect so that hover growth expands
        around the centre instead of the top-left corner. Text is rendered once at the
        final animated size and smoothscaled to the current size, which keeps growth
        continuous rather than stepping between integer font sizes.
        """
        ...

    def update(self, event):
        """
        Handle mouse interaction while hovered or active.

        Pressing sets the ACTIVE state, which the engine will not clear on its own;
        releasing returns to NORMAL. Because this runs once per event, a hold can fire
        more than once per frame.

        :param event: a pygame event
        """
        ...

    def resize(self, w, h):
        """
        Apply a responsive resize, rescaling the corner radii first.

        :param w: new width in pixels
        :param h: new height in pixels
        """
        ...

    def m_animation_on_standby(self):
        """Run size, fill and corner radii backwards, unless animation is disabled."""
        ...

    def m_animation_on_hover(self):
        """Run size, fill and corner radii forwards, unless animation is disabled."""
        ...

    def m_animation_on_hold(self):
        """
        Shrink slightly while held.

        Uses a backward update capped at reach=0.15, so the button travels only the last
        fifteen percent of its growth back, producing a press-in rather than a full
        collapse.
        """
        ...

    def m_on_release(self):
        """Default release action. Placeholder; replace by passing on_release."""
        ...

    def request_cursor(self):
        """Request the hand cursor while hovered."""
        ...
```

---

## `checkbox.py`

```python
class Checkbox(Widget, RectMixin, TextMixin):
    """
    A toggleable box with an optional label. In development.

    The constructor, attribute resolution, size normalisation, resizing and cursor are
    implemented; draw, update and the check state methods are not. The module is not
    imported by pgmenu/__init__.py yet, and most checkbox_* theme keys are still missing
    from DEFAULT.json.

    The check mark carries its own check_* styling family, resolved per widget type with
    the rectmixin_* values as fallbacks. This is the template for any widget that draws
    more than one rectangle.
    """

    def __init__(self, master, coords=THEME, size=THEME, fill=THEME, text=THEME,
                 text_color=THEME, check_fill=THEME, margin=THEME, width=THEME,
                 border_radius=THEME, checked=THEME, **kwargs):
        """
        All parameters except master are themeable through the checkbox_* keys.

        :param master: the display surface or a Frame
        :param coords: (x, y) of the top-left corner
        :param size: box size; a scalar is expanded to a square
        :param fill: box colour, animated colour, or a surface
        :param text: label text drawn beside the box
        :param text_color: label colour
        :param check_fill: colour of the check mark
        :param margin: inner padding between the box and the check mark
        :param width: outline width in pixels; 0 fills the shape
        :param border_radius: corner radius of the box
        :param checked: initial state
        :param kwargs: forwarded to Widget, RectMixin and TextMixin, plus the check_*
                       styling family
        """
        ...

    def _format_size(self, size):
        """
        Normalise the size argument into a (width, height) pair.

        A scalar, including an Animate, is expanded into a square.

        :param size: scalar or sequence, possibly animated
        :return: a two-component size
        """
        ...

    def is_checked(self):
        """Return whether the checkbox is currently checked."""
        ...

    def check(self):
        """Set the checkbox to checked."""
        ...

    def uncheck(self):
        """Set the checkbox to unchecked."""
        ...

    def toggle(self):
        """Invert the checked state."""
        ...

    def draw(self):
        """Render the box, the check mark if checked, and the label."""
        ...

    def update(self, event):
        """
        Handle mouse interaction and toggle on click.

        :param event: a pygame event
        """
        ...

    def resize(self, w, h):
        """
        Apply a responsive resize, rescaling the corner radii first.

        :param w: new width in pixels
        :param h: new height in pixels
        """
        ...

    def request_cursor(self):
        """Request the hand cursor while hovered."""
        ...
```

---

## `draw.py`

`aarect` already has a parameter list; the proposed replacement fills in the descriptions:

```python
def aarect(surface=None, fill=THEME, rect=THEME, width=THEME, border_radius=THEME,
           border_top_left_radius=THEME, border_top_right_radius=THEME,
           border_bottom_left_radius=THEME, border_bottom_right_radius=THEME,
           antialiasing=THEME, transparency=THEME, aa_strength=THEME, **kwargs):
    """
    Draw an antialiased rounded rectangle and return it as a surface.

    Every argument is themeable through the aarect_* keys. Results are cached on their
    visual parameters, so repeatedly drawing the same shape costs one blit.

    :param surface: destination to blit onto, or None to only build and return the surface
    :param fill: colour, pygame.Color, animated colour, or a surface scaled into the shape.
                 A four-component colour moves its fourth component into transparency
    :param rect: (x, y, width, height); x and y are only used for the blit
    :param width: outline width in pixels, clamped to half the smaller side; 0 fills
    :param border_radius: radius applied to every corner without its own value; falls back
                          to round(min(width, height) / 4)
    :param border_top_left_radius: per-corner override, or None to inherit border_radius
    :param border_top_right_radius: per-corner override, or None
    :param border_bottom_left_radius: per-corner override, or None
    :param border_bottom_right_radius: per-corner override, or None
    :param antialiasing: enable the antialiasing pass
    :param transparency: surface alpha, 0..255
    :param aa_strength: number of blended pixels along the edge
    :key inner_fill: fill of the area inside the outline; defaults to fill
    :key inner_transparency: alpha of that area; defaults to transparency
    :key inner_aa_strength: antialiasing width of the inner edge; defaults to aa_strength
    :key inner_antialiasing: antialias the inner edge; defaults to antialiasing
    :key debug: print generation timing whenever the shape is actually built
    :return: the rendered rectangle as a new surface
    """
    ...


def gradient(color1, color2, angle, curve):
    """
    Build a gradient surface. Not implemented.

    :param color1: colour at the start of the gradient
    :param color2: colour at the end of the gradient
    :param angle: gradient direction in degrees
    :param curve: easing callable shaping the interpolation
    """
    ...
```

---

## `aarect.py`

```python
class AARect:
    """
    Renderer for antialiased rounded rectangles.

    Everything is computed during construction plus the aarect() call; there is no
    incremental drawing. The shape is produced subtractively: a full rectangle is filled,
    then an alpha mask carving out the corners and edges is subtracted from it with
    BLEND_RGBA_SUB.

    Up to three passes run through the same draw_rect() code, driven by the temp_*
    attributes: the outer rectangle, an inner rectangle subtracted to hollow out an
    outline, and an inner rectangle blitted as an overlay when a distinct inner fill is
    given. Finished rectangles and individual corner masks are cached separately.
    """

    def __init__(self, surface, fill, rect, width=0, border_radius=10,
                 border_top_left_radius=None, border_top_right_radius=None,
                 border_bottom_left_radius=None, border_bottom_right_radius=None,
                 antialiasing=True, transparency=255, aa_strength=1, **kwargs):
        """
        See pgmenu.draw.aarect for the parameter meanings. This class performs no theme
        resolution; every value must be concrete.

        :param kwargs: inner_fill, inner_transparency, inner_aa_strength,
                       inner_antialiasing, debug
        """
        ...

    def aarect(self):
        """
        Return the finished rectangle, building it if it is not already cached.

        Blits onto the destination surface first if one was given. A copy is returned so
        the caller can modify it without corrupting the cache entry.

        :return: the rendered rectangle as a surface
        """
        ...

    def format_rect(self):
        """
        Validate and normalise the drawing parameters, then build the cache id.

        Splits a four-component colour into colour plus transparency, scales surface fills
        to the rectangle, clamps the outline width and every radius to half the smaller
        side so they cannot overlap, and rebuilds the per-corner radius map.
        """
        ...

    def create_rect(self):
        """
        Compose the rendering passes into the final rectangle and cache it.

        The inner rectangle is subtracted to hollow out an outline, unless an opaque inner
        fill makes that unnecessary, and the overlay is blitted when a distinct inner fill
        is given.
        """
        ...

    def draw_rects(self):
        """
        Run the required passes, each through draw_rect().

        Sets the temp_* attributes before each pass: the outer rectangle at full size, and
        where an outline is present the inner rectangle inset by the outline width plus
        the antialiasing width, with correspondingly reduced radii.

        :return: dict of the produced surfaces, keyed by pass name
        """
        ...

    def draw_rect(self):
        """
        Render a single rectangle from the current temp_* state.

        Fills a surface, applies its alpha, paints the corner and edge antialiasing into a
        mask, then subtracts the mask from the fill. A degenerate rectangle produces an
        empty surface.

        :return: the rendered surface for this pass
        """
        ...

    def get_corners(self):
        """
        Drive aa_corners() once per distinct radius.

        Corners sharing a radius are computed together by setting their draw_border_*
        flags, so a rectangle with four equal radii runs one corner computation instead of
        four.
        """
        ...

    def aa_corners(self, border_radius):
        """
        Build one antialiased corner mask and stamp it onto the flagged corners.

        For each pixel in the radius square, the distance to the circle centre decides
        whether the pixel is inside the shape, inside the antialiasing band, or fully
        outside. Band alphas are pre-compensated twice for passing through intermediate
        surfaces and then mapped through utils.sub_values so that BLEND_RGBA_SUB produces
        the intended result.

        One corner is computed and cached, then mirrored with flips for the other three.

        :param border_radius: radius of the corners being drawn this round
        :return: the antialiasing mask surface
        """
        ...

    def aa_sides(self):
        """
        Paint the antialiasing bands along the four straight edges.

        One line per antialiasing layer per edge, drawn between the corner arcs, with the
        same alpha compensation as the corners.

        :return: the antialiasing mask surface
        """
        ...


def aarect(surface, fill, rect, width=0, border_radius=10, ...):
    """
    Build an antialiased rounded rectangle without theme resolution.

    Identical to pgmenu.draw.aarect except that every argument must be supplied
    explicitly. Prefer pgmenu.draw.aarect unless you are deliberately bypassing the theme.

    :return: the rendered rectangle as a surface
    """
    ...
```

Proposed comment for `force_only_overlay` in `__init__`:

```python
# An opaque inner fill hides whatever is under it, so the "subtract the interior" pass
# can be skipped entirely and only the overlay drawn.
```

---

## `text.py`

```python
def match_font(font, italic=False, bold=False):
    """
    Resolve a font name or file to an absolute path.

    Tries pygame's system font matching first, then the working directory.

    :param font: font name or file name
    :param italic: prefer an italic face
    :param bold: prefer a bold face
    :return: absolute path to a font file, or None if nothing matched
    """
    ...


def format_font(font, italic=False, bold=False):
    """
    Normalise a font argument into a usable path.

    None, or the bundled font's name, resolves to the font shipped with the library.
    Anything else is passed through match_font.

    :param font: font name, file name, path, or None
    :param italic: prefer an italic face
    :param bold: prefer a bold face
    :return: a path suitable for pygame.font.Font
    """
    ...


def render(text=THEME, color=THEME, size=THEME, font=THEME, background=THEME,
           antialias=THEME, italic=THEME, bold=THEME, strikethrough=THEME,
           underline=THEME, transparency=THEME):
    """
    Render text to a new surface.

    Every argument is themeable through the text_* keys. Newlines are supported: each line
    is rendered separately and stacked, giving a surface as wide as the widest line and as
    tall as their total. Results are cached on every argument and a copy is returned, so
    callers may modify the result freely.

    :param text: the string to render; "\\n" starts a new line
    :param color: text colour
    :param size: font point size
    :param font: font path or name; None uses the bundled font
    :param background: solid colour behind the glyphs, or None
    :param antialias: antialias the glyphs
    :param italic: render italic
    :param bold: render bold
    :param strikethrough: render struck through
    :param underline: render underlined
    :param transparency: surface alpha, 0..255
    :return: a new surface containing the rendered text
    """
    ...


def write(surface, coords=THEME, text=THEME, ..., center_x=THEME, center_y=THEME):
    """
    Render text and blit it onto a surface.

    Every argument except surface is themeable through the text_* keys.

    :param surface: destination surface
    :param coords: (x, y) top-left, or the centre anchor when centring is enabled
    :param center_x: treat coords[0] as a horizontal centre
    :param center_y: treat coords[1] as a vertical centre
    (remaining parameters as in render)
    """
    ...
```

`fit_size`, `fit_render` and `fit_render_animated` already carry docstrings. Proposed
additions, appended to the existing text:

```python
def fit_size(...):
    """
    ... (existing text)

    The search is analytic rather than iterative: it starts from the smaller side of the
    destination, then scales down by the width overflow ratio and again by the height
    overflow ratio, flooring each time so the result never overshoots. The margin is
    subtracted from the resulting point size, not from the destination rectangle.
    """


def fit_render_animated(...):
    """
    ... (existing text)

    Text is rendered once at the destination's final animated size and then smoothscaled
    to the current size, rather than re-rendered at each integer point size. This is what
    makes text growth look continuous instead of stepping.
    """
```

---

## `rect.py`

Both functions have docstrings. Proposed additions:

```python
def fit_rects(dest_rect, *rects, margin=0):
    """
    ... (existing text)

    Scaling is done in two stages: every rect is first scaled to the destination height
    minus vertical margins, and if the resulting row is too wide, all of them are scaled
    down by one common factor so their relative proportions are preserved. A single input
    rect is returned unwrapped rather than as a one-element list. Results are cached.
    """


def center_rects(dest_rect, *rects, center_x=THEME, center_y=THEME):
    """
    Centre a group of rectangles inside a destination rectangle.

    The bounding box of all inputs is centred and every rectangle is shifted by the same
    offset, so their relative positions are preserved. A single input rect is returned
    unwrapped. Results are cached.

    :param dest_rect: (x, y, width, height) to centre within
    :param rects: (x, y, width, height) rectangles to shift together
    :param center_x: centre horizontally; themeable through position_center_x
    :param center_y: centre vertically; themeable through position_center_y
    :return: the shifted rectangles, unwrapped when there is only one
    """
```

---

## `position.py`

```python
def center_coords(size, rect, center_x=THEME, center_y=THEME):
    """
    Return the top-left coordinates that centre a size inside a rectangle.

    Each axis is independent, so a size can be centred horizontally while staying at the
    rectangle's top. Passing a zero-sized rectangle turns this into "centre on a point",
    which is how Label centres on its coords.

    :param size: (width, height) of the thing being placed
    :param rect: (x, y, width, height) to centre within
    :param center_x: centre horizontally; themeable through position_center_x
    :param center_y: centre vertically; themeable through position_center_y
    :return: (x, y) top-left coordinates
    """
    ...


def place():
    """Place a widget by anchor or grid position. Not implemented."""
    ...
```

---

## `resize.py`

```python
def _scale(base, master_size, master_base_size, mode, resize_x, resize_y):
    """
    Rescale a base geometry for a new master size.

    The base value is expressed as the fraction of the master it covered at design time,
    and that fraction is re-applied to the current master size. In PROPORTIONAL mode the
    smaller of the two resulting factors wins and the other axis is derived from the
    original aspect ratio, so the widget never distorts. The per-axis switches are applied
    last and override both modes.

    :param base: the design-time (x, y) or (width, height)
    :param master_size: the master's current size
    :param master_base_size: the master's design-time size
    :param mode: pgmenu.PROPORTIONAL or pgmenu.STRETCH
    :param resize_x: scale the first component
    :param resize_y: scale the second component
    :return: the rescaled two-component value
    """
    ...


def responsive_resize(widget, event):
    """
    Apply responsive scaling to a widget on a window resize.

    Does nothing unless the event is pygame.VIDEORESIZE. Widgets inside a Frame scale
    against the frame; everything else scales against the window, using the size captured
    on the first update() call as the reference.

    Raises pgmenu.vars.videoresized for the duration, which stops Widget.__setattr__ from
    overwriting the base geometry the calculation depends on.

    :param widget: the widget to rescale
    :param event: the event being processed
    """
    ...


def reset_videoresize():
    """Lower the videoresized flag at the end of an update pass."""
    ...
```

---

## `display.py`

```python
def fullscreen_controls(screen, event):
    """
    Toggle fullscreen when F11 is released.

    Must be called per event from the application's event loop, and its return value must
    be assigned back to the caller's display surface, because toggling recreates it. The
    windowed size is remembered so it can be restored, and a VIDEORESIZE event is posted
    where pygame does not emit one, so the responsive system reacts.

    This cannot be folded into pgmenu.update because it has to replace the caller's screen
    reference.

    :param screen: the current display surface
    :param event: the event being processed
    :return: the display surface to use from now on
    """
    ...


def set_transparent_window(transparency):
    """
    Make the whole window translucent. Windows only.

    Uses the Win32 layered-window API through ctypes.

    :param transparency: window alpha, 0 fully transparent to 255 opaque
    """
    ...


def set_transparent_colorkey(colorkey):
    """
    Make one colour fully transparent, punching a hole through the window. Windows only.

    Anything drawn in this colour lets the desktop show through, including mouse input.

    :param colorkey: (r, g, b) colour to treat as transparent
    """
    ...
```

---

## `menu.py`

```python
class Menu:
    """
    A named group of widgets that can be drawn and modified together.

    Menu affects drawing only. Its members stay registered with the engine, so switching
    menus is a matter of calling pgmenu.menu.show; widgets belonging to a menu that is not
    drawn are skipped by the update pass because they were not drawn that frame.
    """

    def __init__(self, *widgets, **kwargs):
        """
        :param widgets: the widgets in this menu
        :param kwargs: reserved for future options
        """
        ...

    def modify(self, **kwargs):
        """
        Set attributes on this menu and on every member widget.

        :param kwargs: attribute name to value mapping
        """
        ...

    def add(self, *widgets):
        """Add widgets to the menu."""
        ...

    def remove(self, *widgets):
        """Remove widgets from the menu, ignoring any that are not members."""
        ...

    def draw(self):
        """Draw only this menu's widgets, with the usual draw priority rules."""
        ...


def show(menu):
    """
    Set the menu that pgmenu.menu.draw will draw.

    :param menu: the Menu to show
    """
    ...


def draw():
    """Draw the currently shown menu, if one has been set."""
    ...
```

---

## `simple.py`

```python
class PgmenuWindow:
    """
    A window and main loop wrapper, in the spirit of tkinter's mainloop.

    Owns the display surface, the clock and the event loop, including fullscreen handling
    and the pgmenu draw and update calls. Intended for prototypes and small tools; write
    the loop yourself when ordering matters.
    """

    def __init__(self, size=(230, 210), title="pgmenu", fps=60, flags=pygame.RESIZABLE):
        """
        Initialise pygame and create the window.

        :param size: initial window size, also the reference size for responsive scaling
        :param title: window caption
        :param fps: frame rate cap, changeable at any time
        :param flags: pygame display flags
        """
        ...

    def blit(self, surface, dest):
        """
        Register a surface to be blitted every frame, underneath the widgets.

        :param surface: the surface to draw
        :param dest: (x, y) destination
        """
        ...

    def loop(self, loop=None):
        """
        Run the main loop until the window is closed.

        Each frame: drain events, handle quitting and the fullscreen toggle, clear with
        the theme background, call the user callback, blit registered surfaces, draw and
        update the widgets, flip, and tick the clock.

        :param loop: callable invoked once per frame after clearing and before the widgets
        """
        ...
```

---

## `projects.py`

```python
class MovablePlaneWindow:
    """
    An infinite plane that can be panned with the mouse and zoomed with the wheel.

    A skeleton project meant to be copied into an application rather than used as a stable
    API. Surfaces are registered at plane coordinates, culled when off screen and rescaled
    to the current zoom.
    """

    def __init__(self, screen, **kwargs):
        """
        :param screen: the display surface to draw onto
        :key scale_speed: zoom step per wheel notch
        :key min_scale: lower bound on the zoom factor
        :key move_speed: pan speed multiplier
        :key move_button: mouse button used to drag the plane
        :key resize: callable replacing the default surface rescaling strategy
        """
        ...

    def clear(self):
        """Drop every registered surface."""
        ...

    def blit(self, surface, dest):
        """
        Register a surface at plane coordinates.

        :param surface: the surface to draw
        :param dest: (x, y) in plane space, not screen space
        """
        ...

    def controls(self, event):
        """
        Handle panning and zooming input.

        :param event: the event being processed
        """
        ...

    def m_resize(self, surface, coords, size, new_size):
        """
        Default rescaling strategy, replacing the stored surface with the scaled one.

        :param surface: the original surface
        :param coords: its plane coordinates
        :param size: its unscaled size
        :param new_size: the size required at the current zoom
        :return: the rescaled surface
        """
        ...

    def draw(self):
        """
        Advance the zoom animation and draw every surface currently in view.

        Also acts as the update step: zooming is recentred on the mouse position by
        adjusting the plane offset around the scale change.
        """
        ...


def modern_ui():
    """Load the gradient assets used by the MODERN theme. Not implemented."""
    ...
```

---

## `lib.py`

```python
def init():
    """
    Initialise the library.

    Creates pgmenu.Theme, loads the DEFAULT theme into it, and sets the starting cursor.
    Called automatically when the package is imported.
    """
    ...


def _draw(*widgets):
    """
    Draw a sequence of widgets, applying the draw priority rules.

    Hidden widgets are skipped. Widgets that must appear on top, that is containers whose
    children have queued surfaces onto them, and hovered or active widgets that opt into
    draw priority, are collected and drawn after the rest.

    :param widgets: the widgets to draw, in order
    """
    ...


def draw_all():
    """Draw every registered widget, in draw order."""
    ...


def update(events):
    """
    Run the update pass: hit testing, state transitions, callbacks and resizing.

    Call once per frame, after draw_all and before flipping the display, passing the same
    event list the application collected. A single event is accepted as well as a list, and
    an empty list is padded with a placeholder so per-frame widget logic still runs on
    idle frames.

    Widgets that are disabled, hidden, or were not drawn this frame are skipped. The
    window size captured on the first call becomes the reference for all responsive
    scaling, so the display should already be at its design size.

    :param events: the events collected this frame
    """
    ...


def request_cursor(cursor):
    """
    Claim the mouse cursor for this frame, overriding any widget request.

    The request is cleared at the end of every update, so it must be renewed each frame,
    typically from an on_hover callback. Pass None to release it.

    :param cursor: a pygame cursor constant, or None
    """
    ...
```

Proposed comment inside `update`, above the event normalisation:

```python
# A placeholder event keeps per-event widget logic running on frames where the queue is
# empty. Note that this appends to the caller's list.
```

---

## `__init__.py`

Proposed module docstring:

```python
"""
pgmenu: a widget toolkit, animation system and drawing layer for pygame.

Importing the package imports every submodule and runs lib.init(), which creates
pgmenu.Theme and loads the DEFAULT theme. Widgets are used through their modules
(pgmenu.button.Button, pgmenu.label.Label, ...), while the engine functions draw_all,
update and request_cursor and every constant are available at package level.
"""
```

---

## Summary of proposed comments

Only six places genuinely need a comment beyond the docstrings above. All others in the code
today are adequate.

| File | Location | Comment |
| --- | --- | --- |
| `utils.py` | above `sub_values` | What the table inverts and how to read it |
| `widget.py` | inside `add.frame_handling` | Why frames need special ordering |
| `widget.py` | `__setattr__`, step 1 | That the equality guard is what prevents animation restarts |
| `aarect.py` | `force_only_overlay` assignment | Why an opaque inner fill lets a whole pass be skipped |
| `aarect.py` | `draw_rect`, the final subtractive blit | That the shape is carved out of a full rectangle, not drawn |
| `lib.py` | `update`, event normalisation | Why a placeholder event exists, and that it mutates the caller's list |
