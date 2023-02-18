from datetime import datetime as dt
from datetime import timedelta


def to_datetime(s: str):
    try:
        return dt.strptime(s, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(e)
        return None


def now_delay(sec: int):
    return dt.now() - timedelta(seconds=sec)


def now():
    return dt.now()
