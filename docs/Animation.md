# Animation

### object AnimateType()
All animation objects inherit this class. To identify an animation object, it's only necessary to do `isinstance(x, pgmenu.animation.AnimateType)`.

### object Animate()
Should behave like a normal integer or float, and can be used as if it was.

### object AnimateTuple()
Should behave like a normal tuple, and can be used as if it was.

### object AnimateMultiple()
Allows to manipulate multiple animation objects at once.

## Animation Quirks in Practice
Animation objects are particular in python and rather unpythonic as to their functionability. While they have been created for the easiest use and integration, acting as normal `int` or `tuple` objects, this can also lead to some confusion, as they can't, and don't always act like their pythonic conterparts.

For instance, animation objects are mutable, and act as so in lists. If changed/updated, animation objects values' will equally be updated in said list; they are not frozen in place.

### Wiget Color Argument
Widgets include simplified, built-in animation handling. However, for some animations, a more complex handling is necessary.

Color arguments, or fill for some widgets, follow the same `animation_scale` animation scaling factor as all other arguments. However, this means color values can easily surpass their limit of `(255, 255, 255, 255)` or vice versa. As of right now, there is no handling for said color value overflow. In addition, this remains restrictive; this does not allow to choose the final color.

However, there is an easy fix. One simply has to define the color argument as an animation object beforehand:
```python
color = pgmenu.animation.AnimateTuple(*((0, 255), (0, 255), (0, 255)), duration=0.3, curve=pgmenu.animation.circ)
label = pgmenu.label.Label(screen, coords=(100,100), color=color)
```