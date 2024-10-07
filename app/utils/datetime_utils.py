from datetime import datetime, timedelta
import pytz

# TIME UTC

def datetime_now():
    return datetime.now(pytz.utc)

def datetime_limit(minutes: int):
    return datetime_now() + timedelta(minutes=minutes)

def datetime_unix(time):
    return int(time.timestamp())