from .ansi import Font, Color, Fill, get_ansi_style, wrap_styles

__all__ = ['Drawer', 'DrawerCollection', 'stylize']


class Drawer:
    def __init__(self, **kwargs):
        self.width = kwargs.get('width', 'auto')
        self.align = kwargs.get('align', 'left')
        self.wrap = kwargs.get('wrap', False)

        self.color = kwargs.get('color')
        self.fill = kwargs.get('fill')
        self.font = kwargs.get('font')

    def __str__(self):
        return wrap_styles(self._color, self._fill, *self._font)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: str):
        self._color = get_ansi_style(Color, value)

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, value: str):
        self._fill = get_ansi_style(Fill, value)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value: str or list or tuple):
        if not (isinstance(value, list) or isinstance(value, tuple)):
            value = [value]

        self._font = [get_ansi_style(Font, v) for v in value]


class DrawerItem(Drawer):
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return DrawerCollection(self, other)

        elif isinstance(other, DrawerCollection):
            return other + self

        else:
            raise ValueError


class DrawerCollection(Drawer):
    def __init__(self, *text, sep: str = '', **kwargs):
        super().__init__(**kwargs)

        self.items = text
        self.sep = sep

    def __str__(self):
        items_str = self.sep.join(str(item) for item in self.items)
        return super().__str__().format(text=items_str)

    def __len__(self):
        return len(self.items)

    def __add__(self, other):
        if isinstance(other, DrawerItem):
            return DrawerCollection(*self.items[:], other)

        elif isinstance(other, DrawerCollection):
            return DrawerCollection(self, other)

        else:
            raise ValueError


class Text(DrawerItem):
    def __init__(self, value: str, **kwargs):
        super().__init__(**kwargs)

        self.value = str(value)

    def __str__(self):
        return super().__str__().format(text=self.value)

    def __len__(self):
        return len(self.value)

    def __add__(self, other):
        if isinstance(other, str):
            new_text = self
            new_text.value += other
            return new_text

        return super().__add__(other)

    def __mod__(self, other):
        new_text = self
        new_text.value %= other
        return new_text

    def __format__(self, format_spec):
        drawer = self
        drawer.value = format(drawer.value, format_spec)
        return drawer


def stylize(text: str, **kwargs):
    return Text(text, **kwargs)
