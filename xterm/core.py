import sys
import shutil

from .ansi import Cursor, Erase

__all__ = ['get_size', 'raw_write', 'raw_read', 'write', 'read',
           'cursor_to', 'cursor_move', 'cursor_show', 'cursor_hide',
           'cursor_save', 'cursor_restore', 'cursor_scroll', 'clear', 'clear_line']


def get_size():
    columns, lines = shutil.get_terminal_size()
    return columns, lines


def raw_write(text: str, flush: bool = True):
    sys.stdout.write(text)
    if flush:
        sys.stdout.flush()


def raw_read(prompt: str = None):
    if prompt is None:
        prompt = ''
    raw_write(prompt)
    input_string = sys.stdin.readline()
    return input_string.rstrip('\n')


def cursor_to(line: int, column: int):
    if line is None:
        raw_write(Cursor.COL.format(n=column))
    else:
        raw_write(Cursor.POSITION.format(line=line, column=column))


def cursor_move(lines: int, columns: int):
    shift = ''

    if lines < 0:
        shift += Cursor.UP.format(n=-lines)
    elif lines > 0:
        shift += Cursor.DOWN.format(n=lines)

    if columns < 0:
        shift += Cursor.LEFT.format(n=-columns)
    elif columns > 0:
        shift += Cursor.RIGHT.format(n=columns)

    raw_write(shift)


def cursor_show():
    raw_write(Cursor.SHOW)


def cursor_hide():
    raw_write(Cursor.HIDE)


def cursor_save():
    raw_write(Cursor.SAVE)


def cursor_restore():
    raw_write(Cursor.RESTORE)


def cursor_scroll(n: int):
    scroll_direction = Cursor.SCROLL_UP if n < 0 else Cursor.SCROLL_DOWN
    raw_write(scroll_direction.format(n=abs(n)))


def clear(mode: str = None):
    assert mode in {None, 'all', 'next', 'prev', 'screen'}

    if mode is None:
        cursor_to(0, 0)
        raw_write(Erase.ALL)

    elif mode == 'all':
        raw_write(Erase.ALL)

    elif mode == 'next':
        raw_write(Erase.ALL_NEXT)

    elif mode == 'prev':
        raw_write(Erase.ALL_PREV)


def clear_line(mode: str = None):
    assert mode in {None, 'all', 'next', 'prev'}

    if mode is None:
        raw_write('\r' + Erase.LINE)

    if mode == 'all':
        raw_write(Erase.LINE)

    elif mode == 'next':
        raw_write(Erase.LINE_NEXT)

    elif mode == 'prev':
        raw_write(Erase.LINE_PREV)


def write(*value, sep: str = ' ', end: str = '\n'):
    text = sep.join([str(v) for v in value])
    raw_write(text + end)


def read(prompt: str = None, end: str = '\n'):
    input_string = raw_read(prompt + Cursor.SAVE)
    cursor_restore()
    raw_write(end)
    return input_string
