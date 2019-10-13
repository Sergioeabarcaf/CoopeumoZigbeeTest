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
dates = ["2019-10-02T12:00:00.0","2019-10-03T00:00:00.0","2019-10-03T12:00:00.0",
         "2019-10-04T00:00:00.0","2019-10-04T12:00:00.0","2019-10-05T00:00:00.0","2019-10-05T12:00:00.0",
         "2019-10-06T00:00:00.0","2019-10-06T12:00:00.0","2019-10-07T00:00:00.0","2019-10-07T12:00:00.0",
         "2019-10-08T00:00:00.0","2019-10-08T12:00:00.0","2019-10-09T00:00:00.0","2019-10-09T12:00:00.0",
         "2019-10-10T00:00:00.0","2019-10-10T12:00:00.0","2019-10-11T00:00:00.0","2019-10-11T12:00:00.0"]

cant = 750

try:
    if (conection.valid()):
        while (cant > 0):
            for disp in id:
                for date in dates:
                    # Obtener el ultimo dato desde Digi Remote y convertirla en un JSON
                    data = json.loads(drm.getDataInit(disp,cant,date))
                    # Revertir orden de la data
                    dataReverse = data['list'][::-1]
                    for x in dataReverse:
                        # Decodificar mensaje
                        dataValue = base64.b64decode(x['value'])
                        #Extraer tiempo del mensaje
                        dataTime = x['timestamp']
                        # Limpiar la data y obtener el dispositivo con sus valores
                        data = drm.obtenerData(dataValue)
                        # Se guarda el dato en CSV y si el dato es nuevo, se envia a firebase
                        if goToFirebase.checkData(dataTime, disp):
                            goToFirebase.send(dataTime,disp,data)
                            csvFile.writeData(disp, dataTime, (dataTime.split("T")[0] + '.csv'), data)
                    log.recivedAll(timeCustom.getCurrenDateAndTimeSTR(), "revisado " + str(disp) + " en fecha " + str(date) + " con una cantidad de " + str(cant))
                    # actualizar el contenido en carpeta Drive
                    os.system("grive -u -s datos/")
                    log.recivedAll(timeCustom.getCurrenDateAndTimeSTR, "Se actualizo GRIVE del dispositivo " + str(disp))
                if (cant > 50):
                    cant -= 50
    else:
        log.recivedLog(timeCustom.getCurrenDateAndTimeSTR())
except:
    log.recivedExcept(timeCustom.getCurrenDateAndTimeSTR(), sys.exc_info())