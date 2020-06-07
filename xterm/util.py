__all__ = ['strftime']


def strftime(time: float, unit: str = 'sec', base: str = 'sec', digit: int = 3):
    units = ('ms', 'sec', 'min', 'hour', 'day', 'month', 'year')
    units_modifier = (1000, 60, 60, 24, 30, 12, 1)

    base_rank = units.index(base)
    current_rank = units.index(unit)

    str_time = []
    while time > 0 and current_rank < len(units):
        current_unit = units[current_rank]
        unit_modifier = units_modifier[current_rank]

        current_time = time if unit_modifier == 1 else time % unit_modifier

        if current_time > 0 and current_rank >= base_rank:
            if current_time > 1 and current_unit != 'ms':
                current_unit += 's'

            if current_rank == base_rank:
                str_time.append('%.{}f %s'.format(digit) % (current_time, current_unit))
            else:
                str_time.append('%d %s' % (current_time, current_unit))

            time //= unit_modifier
        else:
            time /= unit_modifier

        current_rank += 1

    return ' '.join(reversed(str_time))
