# 5. Animation

`pgmenu.animation` provides the easing curves and the four animation object types. It is the
subsystem that makes pgmenu widgets feel alive without the user writing animation code, and
it is also the subsystem with the sharpest edges, because its objects deliberately pretend to
be plain Python values.

---

## 5.1 The model

An animation holds a **base value**, a **final value**, a **duration** and a **curve**.
Calling `update(direction, reach)` advances an internal normalised step `x` from `0` towards
`1` (forward) or back down (backward), based on wall-clock time, and recomputes

```
value = base + (final - base) * curve(x, curve_direction)
```

Nothing advances on its own. Something must call `update()` every frame, which is exactly
what the `m_animation_on_*` widget hooks do while a state holds.

| Concept | Meaning |
| --- | --- |
| `direction` | `pgmenu.FORWARD` or `pgmenu.BACKWARD` |
| `reach` | Clamp in `0..1` limiting how far along the curve this call may travel |
| `curve_direction` | `pgmenu.IN`, `pgmenu.OUT` or `pgmenu.IN_OUT`, chosen automatically |
| `done` | True once the current direction has reached its limit; further updates are no-ops |
| `precision` | Decimal places the value is rounded to, for cache friendliness |

Direction handling: on a forward run the curve direction becomes `OUT` (fast start, soft
landing); on a backward run it becomes `IN`. If you set `curve_direction = pgmenu.IN_OUT`
manually, it is left alone.

Changing `direction` or `reach` between calls restarts the timer and clears `done`. On a
backward switch the current step is stored in `last_step`, and the backward step is computed
as `last_step - elapsed / duration`. This is what makes an interrupted hover reverse from
wherever it got to instead of snapping to the end.

---

## 5.2 Curves

The easing functions come from the standard easing set (see easings.net). Each *family*
function takes `(x, direction)` and dispatches to the concrete implementation:

```python
def circ(x, direction):
    return globals()[f"ease_{direction}_circ"](x)
```

| Family | Concrete functions |
| --- | --- |
| `linear` | `linear(x, direction=None)` (no in/out variants) |
| `sine` | `ease_in_sine`, `ease_out_sine`, `ease_in_out_sine` |
| `quad` | `ease_in_quad`, `ease_out_quad`, `ease_in_out_quad` |
| `cubic` | `ease_in_cubic`, `ease_out_cubic`, `ease_in_out_cubic` |
| `quart` | `ease_in_quart`, `ease_out_quart`, `ease_in_out_quart` |
| `quint` | `ease_in_quint`, `ease_out_quint`, `ease_in_out_quint` |
| `expo` | `ease_in_expo`, `ease_out_expo`, `ease_in_out_expo` |
| `circ` | `ease_in_circ`, `ease_out_circ`, `ease_in_out_circ` |
| `back` | `ease_in_back`, `ease_out_back`, `ease_in_out_back` (overshoots) |
| `elastic` | `ease_in_elastic`, `ease_out_elastic`, `ease_in_out_elastic` |
| `bounce` | `ease_in_bounce`, `ease_out_bounce`, `ease_in_out_bounce` |

Pass a **family** function as `curve` so that pgmenu can pick the direction for you:

```python
pgmenu.animation.Animate(10, 20, duration=0.4, curve=pgmenu.animation.back)
```

Pass a **concrete** function to lock the shape regardless of direction:

```python
pgmenu.animation.Animate(10, 20, curve=pgmenu.animation.ease_out_bounce)
```

`Animate.update` inspects the callable's signature (`inspect.signature`) and only passes the
direction when the function takes more than one parameter, so both styles and your own
one-argument curves work.

**Writing a custom curve.** Any callable mapping `x` in `0..1` to a coefficient (usually in
`0..1`, but overshooting is fine, `back` and `elastic` do it) is valid:

```python
def snap(x):
    return 0.0 if x < 0.8 else 1.0

anim = pgmenu.animation.Animate(0, 100, 0.3, snap)
```

To register a curve for use from a theme file, it must be importable as a module attribute:

```json
"widget_animation_curve": {"type": "function", "module": "my_curves", "function": "snap"}
```

---

## 5.3 `AnimateType`

The abstract base. Its only real purpose is identification:

```python
isinstance(x, pgmenu.animation.AnimateType)
```

It declares the shared interface: the `value`, `base_value` and `final_value` properties,
their `get_*` accessors, and `init()`, `reset()`, `update(direction, reach)`.

---

## 5.4 `Animate`

```python
Animate(base_num, final_num, duration=THEME, curve=THEME, precision=THEME)
```

An animated number that behaves like a number.

| Property | Returns |
| --- | --- |
| `value` / `num` | Current value |
| `int` | `round(num)` |
| `float` | `float(num)` |
| `base_value` / `base_num` | Starting value |
| `final_value` / `final_num` | Destination value |
| `step` | Current normalised progress |
| `direction`, `reach`, `curve_direction`, `done` | Current animation state |

**Numeric protocol.** `__int__`, `__float__`, `__round__`, `__index__`, `__repr__`, all six
comparisons (through `functools.total_ordering` on `__eq__` and `__lt__`), and the arithmetic
operators `+ - * / // %` in both normal and reflected form. Arithmetic returns **plain
numbers**, not new `Animate` objects, which is what keeps `min(self.size) / 3` style code
working.

`__getattr__` forwards unknown attribute lookups to `float(self.num)`, so `.is_integer()` and
friends work. The side effect is that a misspelled attribute may silently resolve to a float
method instead of raising a clear error.

**Methods**

| Method | Effect |
| --- | --- |
| `init()` | Stamps `start_time`; called automatically on the first `update` |
| `reset()` | Back to base value, clears timing, step and `done` |
| `update(direction=FORWARD, reach=1)` | Advances and returns the new value |

**Example**

```python
size = pgmenu.animation.Animate(30, 60, duration=0.25, curve=pgmenu.animation.circ)

while running:
    if hovering:
        size.update(pgmenu.FORWARD)
    else:
        size.update(pgmenu.BACKWARD)

    pygame.draw.circle(screen, (255, 255, 255), (100, 100), round(size))
```

---

## 5.5 `AnimateTuple`

```python
AnimateTuple(*pairs, duration=THEME, curve=THEME, precision=THEME)
```

Each `pair` is a `(base, final)` tuple, one per component. Internally it holds a list of
`Animate` items and keeps four derived tuples in sync.

| Property | Returns |
| --- | --- |
| `value` / `tuple` / `float_tuple` | Current values as floats |
| `int_tuple` | Current values rounded to ints (what you pass to blitting code) |
| `base_tuple` / `base_value` | Starting values |
| `final_tuple` / `final_value` | Destination values |
| `items` | The underlying `Animate` list |

**Tuple protocol.** `__len__`, `__iter__`, `__getitem__` (returns the `Animate`, not a
float), `__add__` / `__radd__` (concatenates with plain tuples), `__eq__` and `__lt__`.

Note the asymmetry: iterating gives you `Animate` objects, while `value` gives floats. This
is why `min(button.size)` returns an `Animate` and `min(button.size.int_tuple)` returns an
`int`. Both work where a number is expected.

**Example: an explicit colour transition**

```python
color = pgmenu.animation.AnimateTuple((250, 50), (50, 50), (50, 250),
                                      duration=0.5,
                                      curve=pgmenu.animation.circ)
label = pgmenu.label.Label(frame, (250, 150), color=color, size=100)


def on_hover():
    label.color.update(pgmenu.FORWARD)


def on_standby():
    label.color.update(pgmenu.BACKWARD)


label.animation_on_hover = on_hover
label.animation_on_standby = on_standby
```

`AnimateTuple` does not expose an aggregate `done` flag; check `all(item.done for item in
tuple_anim)` if you need one.

---

## 5.6 `AnimateSurface`

```python
AnimateSurface(base_surface, final_surface,
               base_alpha=THEME, final_alpha=THEME,
               duration=THEME, curve=THEME, precision=THEME)
```

A cross-fade between two surfaces. It **subclasses `pygame.Surface`**, so you can blit it,
pass it to `smoothscale`, or hand it to any pygame function directly.

Its own pixels are the composite: `update()` clears to transparent, sets the final surface's
alpha from the internal `animation_alpha` (an `Animate` from `base_alpha` to `final_alpha`),
and blits base then final on top.

| Property | Returns |
| --- | --- |
| `value` / `surface` | `self` |
| `base_value` / `base_surface` | The bottom layer |
| `final_value` / `final_surface` | The top layer |
| `animation_alpha` | The `Animate` driving the blend |

Its own dimensions come from `max(base.get_size(), final.get_size())`, which is a
lexicographic tuple comparison, not a per-axis maximum. Give both surfaces the same size to
avoid surprises.

> The theme defaults `animation_base_alpha` and `animation_final_alpha` are both `0`, so an
> `AnimateSurface` built with `THEME` alphas never fades in. Always pass explicit alphas,
> as the automatic wrapping in `Widget.__setattr__` does.

**Example**

```python
idle  = pgmenu.draw.aarect(None, (63, 68, 72), (0, 0, 200, 100))
hot   = pgmenu.draw.aarect(None, (68, 72, 77), (0, 0, 200, 100))
panel = pgmenu.animation.AnimateSurface(idle, hot, 0, 255, 0.3,
                                        pgmenu.animation.circ)

widget = pgmenu.surface.Surface(frame, panel, (10, 150),
                                on_hover=lambda: widget.surface.update(pgmenu.FORWARD),
                                on_standby=lambda: widget.surface.update(pgmenu.BACKWARD))
```

---

## 5.7 `AnimateMultiple`

```python
AnimateMultiple(*animations)
```

A remote control for several animation objects at once. It stores them in a dict keyed by
`id()`, so adding the same object twice is idempotent.

| Member | Effect |
| --- | --- |
| `value` / `base_value` / `final_value` | Lists of the members' corresponding values |
| `modify(*animations)` | Add or replace members |
| `reset()` | Reset every member |
| `update(direction, reach)` | Update every member |

```python
group = pgmenu.animation.AnimateMultiple(button.size, button.fill, button.border_radius)
group.update(pgmenu.FORWARD)
```

`AnimateMultiple` is not an `AnimateType` and has no `init()`.

---

## 5.8 Quirks in practice

Animation objects are deliberately unpythonic. The following behaviours are consequences of
that design and are worth knowing before debugging.

**They are mutable and shared.** Putting an animation object in a list, a dict or on several
widgets does not freeze it. Every holder sees the same live value, and updating it once
updates it everywhere. This is often what you want (share one `AnimateTuple` colour across a
row of labels) and occasionally not.

**Equality compares current values.** `Animate.__eq__` compares `self.num` to the other
value, and `AnimateTuple.__eq__` compares `value`. Two animations at the same instant are
equal even if they have different destinations. `__hash__` is `id()`, so identity is used for
dict keys while `==` is not identity. Do not mix the two.

**Re-assignment is guarded.** `Widget.__setattr__` ignores an assignment whose value equals
the attribute's existing `base_value`. `button.size = button.size.base_tuple` does nothing;
that is intentional, and it is what stops a per-frame assignment from restarting animations.

**Arithmetic degrades to plain numbers.** `button.size[0] * 2` is a float, not an animation.
Chained arithmetic silently loses animation.

### The colour argument problem

Widget colour and fill arguments go through the same automatic wrapping as everything else,
which means the final colour is `base * animation_scale` per channel. Two problems follow:

1. Channels can exceed `255` (or drop below `0` on a scale under 1). There is currently no
   clamping.
2. You cannot choose the destination colour, only a uniform brightness multiplier.

The fix is to build the animation yourself and pass it in, which bypasses the wrapping
entirely because the value is already an `AnimateType`:

```python
color = pgmenu.animation.AnimateTuple((0, 255), (0, 255), (0, 255),
                                      duration=0.3,
                                      curve=pgmenu.animation.circ)
label = pgmenu.label.Label(screen, coords=(100, 100), color=color)
```

The same technique applies to `size`, `coords`, `border_radius` and `fill` on any widget.

### Disabling animation

Three levels:

| Scope | How |
| --- | --- |
| One widget | `widget.disable_animation = True` (respected by the stock `m_animation_*` hooks) |
| One widget, one attribute | Assign an `AnimateType` whose base and final values are equal |
| Globally | Set `widget_animation_scale` to `1` in your theme, or override the `m_animation_*` hooks |

Setting `animation_duration` to `0` is not a way to disable animation: the constructor clamps
duration to at least `sys.float_info.epsilon` to avoid division by zero, which makes the
animation instantaneous rather than absent.
