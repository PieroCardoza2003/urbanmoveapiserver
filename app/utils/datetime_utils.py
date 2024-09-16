from datetime import datetime
import pytz

pais = 'America/Lima'

def get_datetime_now():
    zona_horaria = pytz.timezone(pais)
    hora_peru = datetime.now(zona_horaria)
    return hora_peru.strftime('%Y-%m-%d %H:%M:%S')

def get_date_now_unix():
    tz = pytz.timezone(pais)
    now = datetime.now(tz)
    unix_timestamp = int(now.timestamp())
    return unix_timestamp
