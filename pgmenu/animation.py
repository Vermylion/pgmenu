# Animation curves can be found on: https://easings.net/
# Look into the curves from https://epiceasing.com/
# There isn't the expressions though
# There's easing out_in
# Ease elastic and bounce are separate from easing, with a lot more variants
import sys
import math
import time
from functools import total_ordering
from typing import Callable
import inspect

import pygame

import pgmenu
from pgmenu.constants import THEME
from pgmenu.theme import resolve


# x represents from beginning to end of animation, from 0 to 1

# Needs direction since acts as main hub for linear, since it's alone
def linear(x, direction = None):
    return x


def sine(x, direction):
    return globals()[f"ease_{direction}_sine"](x)


def ease_in_sine(x):
    return 1 - math.cos((x * math.pi) / 2)


def ease_out_sine(x):
    return math.sin((x * math.pi) / 2)


def ease_in_out_sine(x):
    return -(math.cos(math.pi * x) - 1) / 2


def quad(x, direction):
    return globals()[f"ease_{direction}_quad"](x)


def ease_in_quad(x):
    return x * x


def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)


def ease_in_out_quad(x):
    return 2 * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 2) / 2


def cubic(x, direction):
    return globals()[f"ease_{direction}_cubic"](x)


def ease_in_cubic(x):
    return x ** 3


def ease_out_cubic(x):
    return 1 - math.pow(1 - x, 3)


def ease_in_out_cubic(x):
    return 4 * x ** 3 if x < 0.5 else 1 - math.pow(-2 * x + 2, 3) / 2


def quart(x, direction):
    return globals()[f"ease_{direction}_quart"](x)


def ease_in_quart(x):
    return x ** 4


def ease_out_quart(x):
    return 1 - math.pow(1 - x, 4)


def ease_in_out_quart(x):
    return 8 * x ** 4 if x < 0.5 else 1 - math.pow(-2 * x + 2, 4) / 2


def quint(x, direction):
    return globals()[f"ease_{direction}_quint"](x)


def ease_in_quint(x):
    return x ** 5


def ease_out_quint(x):
    return 1 - math.pow(1 - x, 5)


def ease_in_out_quint(x):
    return 16 * x ** 5 if x < 0.5 else 1 - math.pow(-2 * x + 2, 5) / 2


def expo(x, direction):
    return globals()[f"ease_{direction}_expo"](x)


def ease_in_expo(x):
    return 0 if x == 0 else math.pow(2, 10 * x - 10)


def ease_out_expo(x):
    return 1 if x == 1 else 1 - math.pow(2, -10 * x)


def ease_in_out_expo(x):
    return 0 if x == 0 else \
        1 if x == 1 else \
            2 ** (20 * x - 10) / 2 if x < 0.5 else \
                (2 - 2 ** (-20 * x + 10)) / 2


def circ(x, direction):
    return globals()[f"ease_{direction}_circ"](x)


def ease_in_circ(x):
    return 1 - math.sqrt(1 - math.pow(x, 2))


def ease_out_circ(x):
    return math.sqrt(1 - math.pow(x - 1, 2))


def ease_in_out_circ(x):
    return (1 - ((1 - (2 * x) ** 2) ** 0.5)) / 2 if x < 0.5 else \
        ((1 - ((-2 * x + 2) ** 2)) ** 0.5 + 1) / 2


def back(x, direction):
    return globals()[f"ease_{direction}_back"](x)


def ease_in_back(x):
    c1 = 1.70158
    c3 = c1 + 1

    return c3 * x ** 3 - c1 * x * x


def ease_out_back(x):
    c1 = 1.70158
    c3 = c1 + 1

    return 1 + c3 * math.pow(x - 1, 3) + c1 * math.pow(x - 1, 2)


def ease_in_out_back(x):
    c1 = 1.70158
    c2 = c1 * 1.525

    return (2 * x) ** 2 * ((c2 + 1) * 2 * x - c2) / 2 if x < 0.5 else \
        ((2 * x - 2) ** 2 * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2


def elastic(x, direction):
    return globals()[f"ease_{direction}_elastic"](x)


def ease_in_elastic(x):
    c4 = (2 * math.pi) / 3

    return 0 if x == 0 else \
        1 if x == 1 else \
            -math.pow(2, 10 * x - 10) * math.sin((x * 10 - 10.75) * c4)


def ease_out_elastic(x):
    c4 = (2 * math.pi) / 3

    return 0 if x == 0 else \
        1 if x == 1 else \
            math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1


def ease_in_out_elastic(x):
    c5 = (2 * math.pi) / 4.5

    return 0 if x == 0 else \
        1 if x == 1 else \
            -(math.pow(2, 20 * x - 10) * math.sin((20 * x - 11.125) * c5)) / 2 if x < 0.5 else \
                (math.pow(2, -20 * x + 10) * math.sin((20 * x - 11.125) * c5)) / 2 + 1


def bounce(x, direction):
    return globals()[f"ease_{direction}_bounce"](x)


def ease_in_bounce(x):
    return 1 - ease_out_bounce(1 - x)


def ease_out_bounce(x):
    n1 = 7.5625
    d1 = 2.75

    if x < 1 / d1:
        return n1 * x * x
    elif x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    elif x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    else:
        x -= 2.625 / d1
        return n1 * x * x + 0.984375


def ease_in_out_bounce(x):
    return (1 - ease_out_bounce(1 - 2 * x)) / 2 if x < 0.5 else \
        (1 + ease_out_bounce(2 * x - 1)) / 2


# FIXME -> Keep initial_call() as a method for all Animates?

class AnimateType:

    def __init__(self):
        ...

    @property
    def value(self):
        ...

    @property
    def base_value(self):
        ...

    @property
    def final_value(self):
        ...

    def init(self):
        ...

    def reset(self):
        ...

    def update(self, direction = pgmenu.FORWARD, reach: int | float = 1):
        ...


@total_ordering
class Animate(AnimateType):

    def __init__(self,
                 base_num: int | float,
                 final_num: int | float,
                 duration: float = THEME,
                 curve: Callable = THEME,
                 precision: int | None = THEME):

        super().__init__()

        self.base_num = base_num
        self.final_num = final_num
        self.duration = resolve(duration, pgmenu.Theme.animation_duration)
        # Makes sure it can never be 0 (because of division by 0)
        self.duration = max(self.duration, sys.float_info.epsilon)
        self.curve = resolve(curve, pgmenu.Theme.animation_curve) # Different from animation_curve?
        self.precision = resolve(precision, pgmenu.Theme.animation_precision)

        self.start_time = None
        self.diff_num = self.final_num - self.base_num
        self.num = self.base_num
        self.step = 0
        self.last_step = 0 # Last step of forward used in backward step loop: backward_step = (last step - step)
        self.direction = pgmenu.FORWARD
        self.reach = 1
        self.curve_direction = pgmenu.OUT
        self.done = False

    @property
    def value(self):
        return self.num

    @property
    def int(self):
        return round(self.num)

    @property
    def float(self):
        return float(self.num)

    @property
    def base_value(self):
        return self.base_num

    @property
    def final_value(self):
        return self.final_num

    def __int__(self):
        return int(self.num)

    def __float__(self):
        return float(self.num)

    def __round__(self, n=None):
        return round(self.num, n)

    def __index__(self):
        return int(self.num)

    def __repr__(self):
        return str(self.num)

    # Comparisons (via total_ordering)
    def _coerce(self, other):
        return other.value if isinstance(other, AnimateType) else other

    def __eq__(self, other):
        other = self._coerce(other)
        return self.num == other

    def __lt__(self, other):
        other = self._coerce(other)
        return self.num < other

    # Arithmetic operators
    # (return raw numbers, not Animate)
    def __add__(self, other):
        return self.num + self._coerce(other)

    def __radd__(self, other):
        return self._coerce(other) + self.num

    def __sub__(self, other):
        return self.num - self._coerce(other)

    def __rsub__(self, other):
        return self._coerce(other) - self.num

    def __mul__(self, other):
        return self.num * self._coerce(other)

    def __rmul__(self, other):
        return self._coerce(other) * self.num

    def __truediv__(self, other):
        return self.num / self._coerce(other)

    def __rtruediv__(self, other):
        return self._coerce(other) / self.num

    def __floordiv__(self, other):
        return self.num // self._coerce(other)

    def __rfloordiv__(self, other):
        return self._coerce(other) // self.num

    def __mod__(self, other):
        return self.num % self._coerce(other)

    def __rmod__(self, other):
        return self._coerce(other) % self.num

    def __hash__(self):
        return id(self)

    def __getattr__(self, name):
        return getattr(float(self.num), name)
        # raise AttributeError(f"'Animate' object has no attribute '{name}'. Use .value or .int instead.")

    def init(self):
        # Get initial call time
        self.start_time = time.time()

    def reset(self):
        self.start_time = None
        self.diff_num = self.final_num - self.base_num
        self.num = self.base_num
        self.step = 0
        self.last_step = 0
        self.done = False

    def update(self,
               direction = pgmenu.FORWARD,
               reach: float = 1):

        if direction != self.direction or reach != self.reach:
            self.start_time = time.time()
            self.done = False

            if direction == pgmenu.FORWARD:
                if self.curve_direction != pgmenu.IN_OUT:
                    self.curve_direction = pgmenu.OUT

            if direction == pgmenu.BACKWARD:
                self.last_step = self.step

                if self.curve_direction != pgmenu.IN_OUT:
                    self.curve_direction = pgmenu.IN

        self.direction = direction

        reach = max(min(reach, 1), 0)
        self.reach = reach

        # Stop progress when reached end of animation
        if self.done:
            return self.num

        if self.start_time is None:
            self.init()

        current_time = time.time()

        # Dynamic iteration from 0 to 1
        step = (current_time - self.start_time) / self.duration

        if self.direction == pgmenu.BACKWARD:
            self.step = max(self.last_step - step, 1-self.reach)

        else:
            self.step = min(step, self.reach)

        # print(self.step, 1-self.reach, self.reach)

        # Animation curve output
        # Check how many arguments self.curve takes
        if len(inspect.signature(self.curve).parameters) > 1:
            coeff_x = self.curve(self.step, self.curve_direction)
        else:
            coeff_x = self.curve(self.step)

        # Proportion with animation curve
        self.num = self.base_num + self.diff_num * coeff_x

        # Limit decimal digits; important for caching surfaces
        if self.precision is not None:
            self.num = round(self.num, self.precision)

        # Stop animation when the max step is reached
        if (self.step >= self.reach and self.direction == pgmenu.FORWARD) or (self.step <= 1-self.reach and self.direction == pgmenu.BACKWARD):
            self.done = True

        return self.num


@total_ordering
class AnimateTuple(AnimateType):
    
    def __init__(self,
                 *pairs: tuple[int | float, int | float],
                 duration: float = THEME,
                 curve: Callable = THEME,
                 precision: int | None = THEME):
        """
        :param pairs: succession of tuples representing (base_num, final_num)
        :param duration: duration of animation
        :param curve: animation curve used
        :param precision: number of decimal points given to each item
        """

        super().__init__()

        self.duration = resolve(duration, pgmenu.Theme.animation_duration)
        self.curve = resolve(curve, pgmenu.Theme.animation_curve)
        self.precision = resolve(precision, pgmenu.Theme.animation_precision)

        self.items = []
        # This is done for optimization and to reduce for loops. Hopefully worth it
        self.base_tuple = []
        self.final_tuple = []
        self.int_tuple = []
        self.float_tuple = []

        for base, final in pairs:
            animate_num = Animate(base, final, self.duration, self.curve, self.precision)
            self.items.append(animate_num)

            self.base_tuple.append(base)
            self.final_tuple.append(final)

            self.int_tuple.append(int(animate_num.value))
            self.float_tuple.append(float(animate_num.value))

        self.base_tuple = tuple(self.base_tuple)
        self.final_tuple = tuple(self.final_tuple)
        self.int_tuple = tuple(self.int_tuple)
        self.float_tuple = tuple(self.float_tuple)

    @property
    def value(self):
        return self.float_tuple

    @property
    def tuple(self):
        return self.float_tuple

    @property
    def base_value(self):
        return self.base_tuple

    @property
    def final_value(self):
        return self.final_tuple

    #Core Tuple Behavior
    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __repr__(self):
        return repr(self.value)

    def __hash__(self):
        return id(self)

    def __add__(self, other):
        return self.value + tuple(other)

    def __radd__(self, other):
        return tuple(other) + self.value

    # Comparison
    def __eq__(self, other):
        if isinstance(other, AnimateType):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other):
        if isinstance(other, AnimateType):
            return self.value < other.value
        return self.value < other

    # Animation controls
    def init(self):
        for animate_num in self.items:
            animate_num.init()

    def reset(self):
        for animate_num in self.items:
            animate_num.reset()

    def update(self,
               direction = pgmenu.FORWARD,
               reach: int | float = 1):
        self.int_tuple = []
        self.float_tuple = []

        for animate_num in self.items:
            animate_num.update(direction, reach)
            self.int_tuple.append(int(animate_num.value))
            self.float_tuple.append(float(animate_num.value))

        self.int_tuple = tuple(self.int_tuple)
        self.float_tuple = tuple(self.float_tuple)


class AnimateSurface(pygame.Surface, AnimateType):

    def __init__(self,
                 base_surface: pygame.Surface,
                 final_surface: pygame.Surface,
                 base_alpha: int | float = THEME,
                 final_alpha: int | float = THEME,
                 duration: int | float = THEME,
                 curve: Callable = THEME,
                 precision: int | None = THEME):

        super().__init__(max(base_surface.get_size(), final_surface.get_size()),
                         base_surface.get_flags(),
                         base_surface.get_bitsize(),
                         base_surface.get_masks())

        self.base_surface = base_surface#.convert_alpha()
        self.final_surface = final_surface#.convert_alpha()

        self.base_alpha = resolve(base_alpha, pgmenu.Theme.animation_base_alpha)
        self.final_alpha = resolve(final_alpha, pgmenu.Theme.animation_final_alpha)

        self.duration = resolve(duration, pgmenu.Theme.animation_duration)
        self.curve = resolve(curve, pgmenu.Theme.animation_curve)
        self.precision = resolve(precision, pgmenu.Theme.animation_precision)

        self.animation_alpha = Animate(self.base_alpha, self.final_alpha, self.duration, self.curve, self.precision)

        self.blit(self.base_surface, (0, 0))

    @property
    def value(self):
        return self

    @property
    def surface(self):
        return self

    @property
    def base_value(self):
        return self.base_surface

    @property
    def final_value(self):
        return self.final_surface

    def __repr__(self):
        return repr(self.value)

    def __hash__(self):
        return id(self)

    # Animation controls
    def init(self):
        self.animation_alpha.init()

    def reset(self):
        self.animation_alpha.reset()
        # FIXME -> Is this step necessary or could we just wait till update?
        self.fill((0, 0, 0))
        self.final_surface.set_alpha(self.animation_alpha)
        self.blit(self.base_surface, (0, 0))

    def update(self,
               direction=pgmenu.FORWARD,
               reach: int | float = 1):
        self.animation_alpha.update(direction, reach)

        self.fill((0, 0, 0, 0))
        self.final_surface.set_alpha(self.animation_alpha)

        self.blits(((self.base_surface, (0, 0)), (self.final_surface, (0, 0))))


class AnimateMultiple:

    def __init__(self,
                 *animations: AnimateType):

        self.animations = {id(animation): animation for animation in animations}

    @property
    def value(self):
        return [animation.value for animation in list(self.animations.values())]

    @property
    def base_value(self):
        return [animation.base_value for animation in list(self.animations.values())]

    @property
    def final_value(self):
        return [animation.final_value for animation in list(self.animations.values())]

    def modify(self, *animations):
        self.animations.update({id(animation): animation for animation in animations})

    def reset(self):
        for animation in list(self.animations.values()):
            animation.reset()

    def update(self,
               direction = pgmenu.FORWARD,
               reach: int | float = 1):
        for animation in list(self.animations.values()):
            animation.update(direction, reach)
