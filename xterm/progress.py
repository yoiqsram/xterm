import time
from multiprocessing import Process

from .core import write, cursor_show, cursor_hide
from .draw import stylize

__all__ = ['Progress']


class Progress:
    progress_format = {'clock': '\r{cycle} {msg}'}
    progress_cycle = {'line': ['\\', '|', '/', '\u2500']}

    def __init__(self, interval: float = 0.25, **kwargs):
        self.interval = interval
        self.mode = kwargs.get('mode', 'clock')
        self.cycle = kwargs.get('cycle', 'line')
        self.cycle_style = kwargs.get('cycle_style', dict())

        self.timer = []
        self._loader = None

    def _cycle(self, msg: str):
        pos = 0
        progress_format = self.progress_format[self.mode]
        progress_cycle = self.progress_cycle[self.cycle]
        while True:
            cycle = stylize(progress_cycle[pos], **self.cycle_style)
            pos = (pos + 1) % len(progress_cycle)
            yield progress_format.format(cycle=cycle, msg=msg)

    def _write(self):
        while True:
            write(next(self._cycle), end='')
            time.sleep(self.interval)

    def start(self, msg: str = None):
        if msg is None:
            msg = 'Start progress' if len(self.timer) == 0 else 'Resume progress'

        self.timer.append((time.time(), msg))

        cursor_hide()
        self._loader = Process(target=self._write, args=(msg,))

    def stop(self, msg: str = None):
        if self._loader is None:
            raise LookupError

        if msg is None:
            msg = 'End progress'

        self.timer.append((time.time(), msg))

        self._loader.terminate()
        self._loader.join()
        self._loader = None

        write('\r' + msg.format(time=self.timer[-1][0]))
        cursor_show()

        time_elapsed = self.timer[-1] - self.timer[-2]
        return time_elapsed
