import time
import logging

from .ansi import Font, Color, Fill
from .draw import stylize

__all__ = ['LoggerTheme', 'Logger']


class LoggerTheme:
    class Debug:
        font = Font.BOLD
        color = Color.DEFAULT
        fill = Fill.DEFAULT

    class Info:
        font = None
        color = Color.DEFAULT
        fill = Fill.DEFAULT

    class Done:
        font = None
        color = Color.GREEN
        fill = Fill.DEFAULT

    class Warning:
        font = None
        color = Color.YELLOW
        fill = Fill.DEFAULT

    class Error:
        font = None
        color = Color.RED
        fill = Fill.DEFAULT


class Logger(logging.Logger):
    theme = LoggerTheme

    _level = {'silent': logging.WARNING, 'info': logging.INFO, 'debug': logging.DEBUG}

    def __init__(self, name: str, level: str = 'info'):
        super().__init__(name, self._level[level])

        self.handler = logging.StreamHandler()
        self.handler.setFormatter(logging.Formatter('%(message)s'))
        self.addHandler(self.handler)

        self._timer = dict()

    def timer(self, name: str, mode: str = None):
        self._timer[name] = self._timer.get(name, [])
        self._timer[name].append(time.time())

        if mode is None or len(self._timer[name]) == 1:
            return self._timer[name][-1] - self._timer[name][0]
        elif mode == 'delta':
            return self._timer[name][-1] - self._timer[name][-2]

    def info(self, msg, end='\n', **kwargs):
        self.handler.terminator = end
        super().info(msg, **kwargs)

    @staticmethod
    def _log_format(name: str, msg: str, begin: str, style):
        highlight = stylize(' {} '.format(name), font=Font.INVERSE, color=style.color, fill=style.fill)
        msg = stylize(msg, color=style.color, fill=style.fill, font=style.font)
        return begin + str(highlight) + ' ' + str(msg)

    def debug(self, msg, begin='', end='\n', **styles):
        self.handler.terminator = end
        super().debug(self._log_format('Done', msg, begin, self.theme.Debug))

    def done(self, msg, begin='\n', end='\n\n'):
        self.info(self._log_format('Done', msg, begin, self.theme.Done), end=end)

    def warning(self, msg, begin='\n', end='\n\n', **kwargs):
        self.handler.terminator = end
        super().warning(self._log_format('Warning', msg, begin, self.theme.Warning), **kwargs)

    def error(self, msg, begin='\n', end='\n\n', **kwargs):
        self.handler.terminator = end
        super().error(self._log_format('Error', msg, begin, self.theme.Error), **kwargs)
