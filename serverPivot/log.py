import json
import os.path

path = "./log.txt"

# Funcion para almacenar datos de respaldo
def saveBackup(data):
    # Abrir archivo de respaldo y agregar data en formato string al final
    f = open(path, "a")
    f.write(json.dumps(data) + "\n")
    f.close()

# Funcion para revisar si existen datos en el archivo
def loadBackup():
    # Verificar si existe el archivo, si no existe el archivo, retornar False
    if os.path.isfile(path):
        # abrir el archivo y almacenar en un array los datos en formato json
        data = []
        f = open(path)
        for line in f:
            # Eliminar los saltos de linea de cada dato y convertirlos a json
            data.append(json.loads(str(line).replace("\n","")))
        f.close()
        # validar el largo de los datos antes de responder, si esta vacio, retornar false
        if len(data) > 0:
            return data
        else:
            return False
    else:
        return False

# Funcion para limpiar archivo backup
def clean():
    f = open(path,"w")
    f.write("")
    f.close()

# Funcion para almacenar en archivo TXT la fecha y hora del dato recibido.
def recivedLog(datetime):
    f = open(path, "a")
    f.write(datetime + " No hay Conexion. \n")
    f.close()
    return True

# Funcion para almacenar en archivo TXT el error de la exception
def recivedExcept(datetime, error):
    f = open("./error.txt", "a")
    f.write("=====================\n")
    f.write(datetime + "  \n")
    f.write(str(error[0]) + "\n")
    f.write(str(error[1]) + "\n")
    f.write("\n")
    f.close()
    return True

# Funcion para almacenar cualquier mensaje que se requiera.
def recivedAll(datetime, message):
    f = open(path, "a")
    f.write(datetime + " - " + message + "\n")
    f.close()
    return True