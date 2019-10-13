import goToFirebase
import drm
import json
import base64
import time
import conection
import timeCustom
import log
import sys
import csvFile
import os

id = ["00:13:A2:00:41:54:B4:F0","00:13:A2:00:41:92:E0:1F","00:13:A2:00:41:9B:43:E4","00:13:A2:00:41:54:B4:EE","00:13:A2:00:41:5B:67:F2"]

cant = 5

try:
    while (True):
        if (conection.valid()):
            for disp in id:
                # Obtener el ultimo dato desde Digi Remote y convertirla en un JSON
                data = json.loads(drm.getDataDevice(disp,cant))
                # Revertir orden de la data
                dataReverse = data['list'][::-1]
                for x in dataReverse:
                    # Decodificar mensaje
                    dataValue = base64.b64decode(x['value'])
                    #Extraer tiempo del mensaje
                    dataTime = x['timestamp']
                    # Limpiar la data y obtener el dispositivo con sus valores
                    data = drm.obtenerData(dataValue)
                    # si el dato es nuevo, se envia a firebase y se guarda en CSV
                    if goToFirebase.checkData(dataTime, disp):
                        goToFirebase.send(dataTime,disp,data)
                        csvFile.writeData(disp, dataTime, (dataTime.split("T")[0] + '.csv'), data)
                # actualizar el contenido en carpeta Drive
                os.system("grive -u -s datos/")
                log.recivedAll(timeCustom.getCurrenDateAndTimeSTR(), "Se actualizo GRIVE del dispositivo " + str(disp))
        else:
            log.recivedLog(timeCustom.getCurrenDateAndTimeSTR())
        time.sleep(60)
except:
    log.recivedExcept(timeCustom.getCurrenDateAndTimeSTR(), sys.exc_info())