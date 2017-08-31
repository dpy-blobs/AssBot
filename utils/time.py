def human_time(seconds):
    seconds = int(seconds)
    if seconds == 0:
        return '0 seconds'

    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365)

    time_units = {
        'year': years,
        'day': days,
        'hour': hours,
        'minute': minutes,
        'second': seconds
    }

    def _plural(name, value):
        if value != 1:
            name += 's'
        return f'{value} {name}'

    time = [_plural(key, value) for key, value in time_units.items() if value]

    if len(time) > 2:
        return f'{", ".join(time[:-1])}, and {time[-1]}'
    return ' and '.join(time)
