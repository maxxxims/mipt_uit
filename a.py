import datetime
from pytz import timezone 
tz=timezone('Europe/Moscow')
print(datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'))