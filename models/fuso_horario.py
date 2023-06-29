from datetime import datetime
from pytz import timezone

saopaulo_tz = timezone('America/Sao_Paulo')

def now_saopaulo(tz=saopaulo_tz):
    return datetime.now(tz)

def convert_time_to_tz(time, tz=saopaulo_tz):
    datetime_obj = datetime.combine(datetime.today(), time)

    datetime_obj = datetime_obj.astimezone(tz)

    return datetime_obj.time()