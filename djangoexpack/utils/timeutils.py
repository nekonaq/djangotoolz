import datetime
import pytz

# local_tz = pytz.timezone('Asia/Tokyo')     # XXX 仮


def datetime_fromtimestamp(timestamp):
    # return datetime.datetime.fromtimestamp(timestamp, tz=pytz.utc).astimezone(local_tz)
    return datetime.datetime.fromtimestamp(timestamp, tz=pytz.utc)
