from enum import Enum

__all__ = ['ESC', 'CSI', 'CSI_STYLE', 'Cursor', 'Erase', 'Font', 'Color', 'Fill',
           'get_ansi_style', 'code_styles', 'revert_styles', 'wrap_styles']


ESC = '\x1b'
CSI = ESC + '['
CSI_STYLE = CSI + '{0}m'


class Cursor:
    UP = CSI + '{n:d}A'
    DOWN = CSI + '{n:d}B'
    RIGHT = CSI + '{n:d}C'
    LEFT = CSI + '{n:d}D'
    NEXT = CSI + '{n:d}E'
    PREV = CSI + '{n:d}F'
    COL = CSI + '{n:d}G'
    POSITION = CSI + '{line:d};{column:d}H'
    SHOW = CSI + '?25h'
    HIDE = CSI + '?25l'
    SAVE = CSI + 's'
    RESTORE = CSI + 'u'
    SCROLL_UP = CSI + '{n:d}S'
    SCROLL_DOWN = CSI + '{n:d}T'


class Erase:
    ALL_NEXT = CSI + '0J'
    ALL_PREV = CSI + '1J'
    ALL = CSI + '2J'
    LINE_NEXT = CSI + '0K'
    LINE_PREV = CSI + '1K'
    LINE = CSI + '2K'


class Style:
    pass


class Font(Style, Enum):
    RESET = 0
    BOLD = 1
    DIM = 2
    ITALIC = 3
    SLOW_BLINK = 5
    RAPID_BLINK = 6
    INVERT = 7
    HIDE = 8
    UNDERLINE = 4
    STRIKE = 9
    DOUBLE_LINE = 21
    OVER_LINE = 53


class Color(Style, Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97


class Fill(Style, Enum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    DEFAULT = 49
    BRIGHT_BLACK = 100
    BRIGHT_RED = 101
    BRIGHT_GREEN = 102
    BRIGHT_YELLOW = 103
    BRIGHT_BLUE = 104
    BRIGHT_MAGENTA = 105
    BRIGHT_CYAN = 106
    BRIGHT_WHITE = 107


def get_ansi_style(ansi_style, value: str):
    if isinstance(value, str):
        return ansi_style.__dict__.get(value.upper())

    elif isinstance(value, ansi_style.__class__) or value is None:
        return value

    else:
        raise ValueError


def code_styles(*styles) -> str:
    ansi_styles = [str(style.value) for style in styles if issubclass(style.__class__, Style)]
    return CSI_STYLE.format(';'.join(ansi_styles))


def revert_styles(*styles):
    ansi_styles_revert = []

    if any([isinstance(style, Font) for style in styles]):
        ansi_styles_revert.append(Font.RESET)

    if any([isinstance(style, Color) for style in styles]):
        ansi_styles_revert.append(Color.DEFAULT)

    if any([isinstance(style, Fill) for style in styles]):
        ansi_styles_revert.append(Fill.DEFAULT)

    return ansi_styles_revert


def wrap_styles(*styles):
    styles = [style for style in styles if style is not None]
    open_code = code_styles(*styles)

    ansi_styles_revert = revert_styles(*styles)
    close_code = code_styles(*ansi_styles_revert) if len(ansi_styles_revert) > 0 else ''

    return open_code + '{text}' + close_code
