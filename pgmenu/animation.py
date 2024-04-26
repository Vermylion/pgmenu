# Animation curves can be found on: https://easings.net/
# Look into the curves from https://epiceasing.com/
# There isn't the expressions though
# There's easing out_in
# Ease elastic and bounce are separate from easing, with a lot more variants
import math
import time
from typing import Callable
import inspect

import pgmenu


# TODO -> Animation doesn't work well with smaller duration


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


# TODO -> final_num or scale?

class Animate:

    def __init__(self,
                 base_num: int | float,
                 final_num: int | float,
                 duration: float = 0.15,
                 curve: Callable = sine):

        self.base_num = base_num
        self.final_num = final_num
        self.duration = duration
        self.curve = curve

        self.start_time = None
        self.diff_num = self.final_num - self.base_num
        self.num = self.base_num
        self.step = 0
        self.direction = pgmenu.FORWARD
        self.curve_direction = pgmenu.OUT

    def __int__(self):
        return int(self.num)

    def __float__(self):
        return float(self.num)

    def __round__(self, n=None):
        return round(self.num, n)

    @property
    def int(self):
        return round(self.num)

    def initial_call(self):
        # Get initial call time
        self.start_time = time.time()

    def forward(self):
        if self.direction != pgmenu.FORWARD:
            step = self.step
            self.reset()
            self.direction = pgmenu.FORWARD
            if self.curve_direction != pgmenu.IN_OUT:
                self.curve_direction = pgmenu.OUT
            self.step = step

    def backward(self):
        if self.direction != pgmenu.BACKWARD:
            step = self.step
            self.reset()
            self.direction = pgmenu.BACKWARD
            if self.curve_direction != pgmenu.IN_OUT:
                self.curve_direction = pgmenu.IN
            self.step = step

    def reset(self):
        self.start_time = None
        self.diff_num = self.final_num - self.base_num
        self.num = self.base_num
        self.step = 0

    def update(self) -> float:
        if self.start_time is None:
            self.initial_call()

        # Stop progress when reached end of animation
        if (self.step >= 1 and self.direction == pgmenu.FORWARD) or (self.step <= 0 and self.direction == pgmenu.BACKWARD):
            return self.num

        current_time = time.time()

        # Dynamic iteration from 0 to 1
        self.step = (current_time - self.start_time) / self.duration

        if self.direction == pgmenu.BACKWARD:
            self.step = 1 - self.step

        # Stop animation right after it's done -> Maybe find cleaner solution?
        if (self.step >= 1 and self.direction == pgmenu.FORWARD) or (self.step <= 0 and self.direction == pgmenu.BACKWARD):
            return self.num

        # Animation curve output
        if len(inspect.signature(self.curve).parameters) > 1:
            coeff_x = self.curve(self.step, self.curve_direction)
        else:
            coeff_x = self.curve(self.step)

        # Proportion with animation curve
        self.num = self.base_num + self.diff_num * coeff_x

        return self.num
    
    
class AnimateTuple:
    
    def __init__(self,
                 *nums: tuple[int | float, int | float],
                 duration: float = 0.15,
                 curve: Callable = sine):
        """
        :param nums: succession of tuples representing (base_num, final_num)
        :param duration: duration of animation
        :param curve: animation curve used
        """

        self.nums = nums
        self.duration = duration
        self.curve = curve

        self.animate_nums = [Animate(num[0], num[1], self.duration, self.curve) for num in nums]

    @property
    def tuple(self):
        return tuple(animate_num.num for animate_num in self.animate_nums)

    @property
    def inttuple(self):
        return tuple(round(animate_num.num) for animate_num in self.animate_nums)

    @property
    def basetuple(self):
        return tuple(animate_num.base_num for animate_num in self.animate_nums)

    def forward(self):
        for animate_num in self.animate_nums:
            animate_num.forward()

    def backward(self):
        for animate_num in self.animate_nums:
            animate_num.backward()

    def reset(self):
        for animate_num in self.animate_nums:
            animate_num.reset()

    def update(self):
        for animate_num in self.animate_nums:
            animate_num.update()


class AnimateColor:

    def __init__(self,
                 base_color: tuple[int | int | int],
                 final_color: tuple[int | int | int],
                 duration: float = 0.15,
                 curve: Callable = sine):

        self.animate_tuple = AnimateTuple((base_color[0], final_color[0]), (base_color[1], final_color[1]), (base_color[2], final_color[2]),
                                          duration = duration, curve = curve)

    @property
    def color(self):
        return self.animate_tuple.inttuple

    def forward(self):
        self.animate_tuple.forward()

    def backward(self):
        self.animate_tuple.backward()

    def reset(self):
        self.animate_tuple.reset()

    def update(self):
        self.animate_tuple.update()


class AnimateMultiple:

    def __init__(self,
                 *animations):

        self.animations = {id(animation): animation for animation in animations}

    def modify(self, *animations):
        self.animations.update({id(animation): animation for animation in animations})

    def forward(self):
        for animation in list(self.animations.values()):
            animation.forward()

    def backward(self):
        for animation in list(self.animations.values()):
            animation.backward()

    def reset(self):
        for animation in list(self.animations.values()):
            animation.reset()

    def update(self):
        for animation in list(self.animations.values()):
            animation.update()
