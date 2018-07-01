from datetime import date


def int2date(argdate=int):
    """If you have date (int), use this method to obtain a date object.

    Args:
        argdate (int): Date as a regular integer value (example: 20160618)

    Return:
        dateandtime.date: A date object which corresponds to the given value
                          `argdate`.
    """
    year = int(argdate / 10000)
    month = int((argdate % 10000) / 100)
    day = int(argdate % 100)

    return date(year, month, day)
