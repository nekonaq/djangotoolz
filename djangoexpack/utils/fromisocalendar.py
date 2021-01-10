import datetime
from datetime import MINYEAR, MAXYEAR
# from datetime import MINYEAR, MAXYEAR, _ymd2ord, _ord2ymd, _is_leap, _isoweek1monday


def _isoweek1monday(year):
    # Helper to calculate the day number of the Monday starting week 1
    # XXX This could be done more efficiently
    THURSDAY = 3
    # firstday = _ymd2ord(year, 1, 1)
    firstday = datetime.datetime(year, 1, 1).toordinal()
    firstweekday = (firstday + 6) % 7  # See weekday() above
    week1monday = firstday - firstweekday
    if firstweekday > THURSDAY:
        week1monday += 7
    return week1monday


def _is_leap(year):
    "year -> 1 if leap year, else 0."
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# backported from cpython for python3.6
def fromisocalendar(year, week, day):
    """Construct a date from the ISO year, week number and weekday.

    This is the inverse of the date.isocalendar() function"""
    # Year is bounded this way because 9999-12-31 is (9999, 52, 5)
    if not MINYEAR <= year <= MAXYEAR:
        raise ValueError(f"Year is out of range: {year}")

    if not 0 < week < 53:
        out_of_range = True

        if week == 53:
            # ISO years have 53 weeks in them on years starting with a
            # Thursday and leap years starting on a Wednesday
            # first_weekday = _ymd2ord(year, 1, 1) % 7
            first_weekday = datetime.datetime(year, 1, 1).toordinal() % 7
            if (first_weekday == 4 or (first_weekday == 3 and _is_leap(year))):
                out_of_range = False

        if out_of_range:
            raise ValueError(f"Invalid week: {week}")

    if not 0 < day < 8:
        raise ValueError(f"Invalid weekday: {day} (range is [1, 7])")

    # Now compute the offset from (Y, 1, 1) in days:
    day_offset = (week - 1) * 7 + (day - 1)

    # Calculate the ordinal day for monday, week 1
    day_1 = _isoweek1monday(year)
    ord_day = day_1 + day_offset

    # return datetime.datetime(*_ord2ymd(ord_day))
    return datetime.datetime.fromordinal(ord_day)
