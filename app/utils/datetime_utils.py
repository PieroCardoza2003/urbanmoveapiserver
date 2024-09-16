from datetime import datetime
import pytz

def get_datetime_now():
    zona_horaria_peru = pytz.timezone('America/Lima')
    hora_peru = datetime.now(zona_horaria_peru)
    return hora_peru.strftime('%Y-%m-%d %H:%M:%S')
