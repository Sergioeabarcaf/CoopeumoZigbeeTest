import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

cred = credentials.Certificate('dogKey.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://coopeumozigbee.firebaseio.com/'
})

# Almacenar data en registro historico
def send(timestamp,dispositivo,data):
    dataSend = {}
    dataValues = {}
    urlDevice = 'dataDevices/' + dispositivo
    ref = db.reference(urlDevice)
    for x in range (0, len(data)):
        parametro = data[x].split(":")
        dataValues[str(parametro[0])] = parametro[1]
    dataSend["timestamp"] = timestamp
    dataSend["values"] = dataValues
    ref.push(dataSend)

# Verificar si el dato es el ultimo obtenido y actualiza este valor
def checkData(time,id):
    urlCheck = "devices/" + id + "/last"
    ref = db.reference(urlCheck)
    r = ref.get()
    if r == None:
        print "no hay datos anteriores"
        ref.set(time)
        return True
    if r == time:
        print "es el mismo dato"
        print "firebase: " + r + " == " + time
        return 0
    if r < time:
        print "el dato es nuevo"
        print "firebase: " + r + " < " + time
        ref.set(time)
        return True
    if r > time:
        print "el dato es viejo"
        print "firebase: " + r + " > " + time
        return 0
    return False

# Validar que la diferencia de tiempo sea menor a 30 minutos con respecto a la hora actual.
def validDiference30Minutes(id):
    #Obtener la ultima fecha almacenada en el dispositivo y transformarla a formato datetime.
    urlCheck = "devices/" + id + "/last"
    ref = db.reference(urlCheck)
    r = ref.get()
    if (r != None):
        timePas = datetime.datetime.strptime(r, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Obtener fecha actual en formato datetime y calcular la diferencia entre ambas fechas (Formato UTC).
        timeAct = datetime.datetime.utcnow()
        diff = timeAct - timePas
        # Retornar la diferencia entre ellos transformada en cantidad de datos a solicitar.
        return (diff.days * 48) + (diff.seconds / 1800)
    else:
        return 15000
