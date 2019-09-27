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

id = ["00:13:A2:00:41:54:B4:F0","00:13:A2:00:41:92:E0:1F","00:13:A2:00:41:9B:43:E4","00:13:A2:00:41:54:B4:EE","00:13:A2:00:41:5B:67:F2"]
dates = ["2019-09-09T00:00:00.0","2019-09-09T12:00:00.0","2019-09-10T00:00:00.0","2019-09-10T12:00:00.0","2019-09-11T00:00:00.0","2019-09-11T12:00:00.0",
        "2019-09-12T00:00:00.0","2019-09-12T12:00:00.0","2019-09-13T00:00:00.0","2019-09-13T12:00:00.0","2019-09-14T00:00:00.0","2019-09-14T12:00:00.0",
        "2019-09-15T00:00:00.0","2019-09-15T12:00:00.0","2019-09-16T00:00:00.0","2019-09-16T12:00:00.0","2019-09-17T00:00:00.0","2019-09-17T12:00:00.0",
        "2019-09-18T00:00:00.0","2019-09-18T12:00:00.0","2019-09-19T00:00:00.0","2019-09-19T12:00:00.0","2019-09-20T00:00:00.0","2019-09-20T12:00:00.0",
        "2019-09-21T00:00:00.0","2019-09-21T12:00:00.0","2019-09-22T00:00:00.0","2019-09-22T12:00:00.0","2019-09-23T00:00:00.0","2019-09-23T12:00:00.0",
        "2019-09-24T00:00:00.0","2019-09-24T12:00:00.0","2019-09-25T00:00:00.0","2019-09-25T12:00:00.0","2019-09-26T00:00:00.0","2019-09-26T12:00:00.0",
        "2019-09-27T00:00:00.0","2019-09-27T12:00:00.0","2019-09-28T00:00:00.0","2019-09-28T12:00:00.0","2019-09-29T00:00:00.0","2019-09-29T12:00:00.0",
        "2019-09-30T00:00:00.0","2019-09-30T12:00:00.0"]

try:
    while (True):
        if (conection.valid()):
            for disp in id:
                for date in dates:
                    cant = 750
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
                        csvFile.writeData(disp, dataTime, (dataTime.split("T")[0] + '.csv'), data)
                        if goToFirebase.checkData(dataTime, disp):
                            goToFirebase.send(dataTime,disp,data)
            # actualizar el contenido en carpeta Drive
            os.system("grive -u -s datos/")
        else:
            log.recivedLog(timeCustom.getCurrenDateAndTimeSTR())
        time.sleep(60)
except:
    log.recivedExcept(timeCustom.getCurrenDateAndTimeSTR(), sys.exc_info())