import datetime
import dateutil.parser
import pytz
import re
from django.utils import timezone


if hasattr(datetime.datetime, 'fromisocalendar'):
    fromisocalendar = datetime.datetime.fromisocalendar
else:
    from .fromisocalendar import fromisocalendar  # noqa: F401


def zstrftime(value):
    """ datetime を elasticsearch のタイムスタンプ形式に変換する。

    :param datetime.datetime value:	; utc であること
    :rtype: str
    """
    return '{:%Y-%m-%dT%H:%M:%S}.{:03d}Z'.format(value, int(value.microsecond / 1000))


def datetime_fromtimestamp(timestamp):
    """ timestamp を UTC の tzaware な datetime に変換する。
    """
    return datetime.datetime.fromtimestamp(timestamp, tz=pytz.utc)


TZINFOS = {
    'UTC': timezone.utc,
}


def parse_timestamp(timestamp):
    """ elasticsearch の timestamp 文字列を aware datetime に変換する

    :param str timestamp:                  # e.g. '2020-07-06T15:00:00.000Z'
    """
    return dateutil.parser.parse(timestamp, tzinfos=TZINFOS)

month_re = re.compile(
    r'(?P<year>\d{4})-(?P<month>\d{1,2})$'
)

def parse_month(value):
    """ 文字列を解析して日付 (datetime.date) を返す。
    value は "YYYY-MM" の形式
    """
    match = month_re.match(value)
    if match:
        kw = {key: int(val) for key, val in match.groupdict().items()}
        return datetime.date(**kw, day=1)
