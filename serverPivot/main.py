import goToFirebase
import drm
import json
import base64
import time
import conection
import timeCustom
import log
import sys

id = ["00:13:A2:00:41:54:B4:F0","00:13:A2:00:41:92:E0:1F","00:13:A2:00:41:9B:43:E4","00:13:A2:00:41:54:B4:EE","00:13:A2:00:41:5B:67:F2"]

try:
    while (True):
        if (conection.valid()):
            for disp in id:
                cant = 10
                # Obtener el ultimo dato desde Digi Remote y convertirla en un JSON
                data = json.loads(drm.getDataDevice(disp,cant))
                dataReverse = data['list'][::-1]
                for x in dataReverse:
                    dataValue = base64.b64decode(x['value'])
                    dataTime = x['timestamp']
                    # Limpiar la data y obtener el dispositivo con sus valores
                    data = drm.obtenerData(dataValue)
                    if goToFirebase.checkData(dataTime, disp):
                        goToFirebase.send(dataTime,disp,data)
        else:
            log.recivedLog(timeCustom.getCurrenDateAndTimeSTR())
        time.sleep(50)
except:
    log.recivedExcept(timeCustom.getCurrenDateAndTimeSTR(), sys.exc_info())