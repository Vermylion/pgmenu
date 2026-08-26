# FIXME -> Some dunler methods return AnimateTuple when it represents an interaction between 2 AnimateTuple -> Keep it or remove it?
@total_ordering
class AnimateTuple(AnimateType):

    def __init__(self,
                 *pairs: tuple[int | float, int | float],
                 duration: float = THEME,
                 curve: Callable = THEME):
        """
        :param pairs: succession of tuples representing (base_num, final_num)
        :param duration: duration of animation
        :param curve: animation curve used
        """

        super().__init__()

        self.duration = resolve(duration, pgmenu.Theme.animation_duration)
        self.curve = resolve(curve, pgmenu.Theme.animation_curve)

        self._items = []
        self.base_tuple = ()
        self.final_tuple = ()
        self.int_tuple = ()
        self.float_tuple = ()

        for base, final in pairs:
            animate_num = Animate(base, final, self.duration, self.curve)
            self._items.append(animate_num)
            self.base_tuple += base
            self.final_tuple += final

            self.int_tuple += int(animate_num.value)
            self.float_tuple += float(animate_num.value)

    @property
    def value(self):
        return self.float_tuple

    @property
    def tuple(self):
        return self.float_tuple

    # Core Tuple Behavior
    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        result = self._items[index]

        # slice → return new AnimateTuple
        if isinstance(index, slice):
            return AnimateTuple(*[(a.base_num, a.final_num) for a in result],
                                duration=self.duration,
                                curve=self.curve)

        return result

    def __repr__(self):
        return repr(self.value)

    def __hash__(self):
        return id(self)

    # Tuple Concatenation -> IF 2 AnimateTuple are added, it gives another AnimateTuple
    def __add__(self, other):
        if isinstance(other, AnimateTuple):
            return AnimateTuple(*[(a.base_num, a.final_num) for a in self._items + other._items],
                                duration=self.duration,
                                curve=self.curve)

        # allow adding raw tuples like Python does
        return tuple(self.value) + tuple(other)

    def __radd__(self, other):
        return tuple(other) + tuple(self.value)

    # Comparison
    def __eq__(self, other):
        if isinstance(other, AnimateTuple):
            return tuple(self.value) == tuple(other.value)
        return tuple(self.value) == tuple(other)

    def __lt__(self, other):
        if isinstance(other, AnimateTuple):
            return tuple(self.value) < tuple(other.value)
        return tuple(self.value) < tuple(other)

    # Animation controls
    def init(self):
        for animate_num in self._items:
            animate_num.init()

    def forward(self):
        for animate_num in self._items:
            animate_num.forward()

    def backward(self):
        for animate_num in self._items:
            animate_num.backward()

    def reset(self):
        for animate_num in self._items:
            animate_num.reset()

    def update(self):
        self.int_tuple = ()
        self.float_tuple = ()

        for animate_num in self._items:
            animate_num.update()
            self.int_tuple += int(animate_num.value)
            self.float_tuple += float(animate_num.value)