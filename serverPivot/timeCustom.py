from datetime import datetime
import time

# Retornar timestamp actual
def getTimestamp():
    return time.time()

# Retornar Date en formato ddmmaaaa
def getCurrentDateSTR():
    return time.strftime('%d%m%Y')

# Retornar Hora y fecha actual para log
def getCurrenDateAndTimeSTR():
    now = datetime.now()
    return now.strftime("%m - %d - %Y, %H:%M")