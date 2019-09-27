import csv
import os.path as path

fieldNames = ['MAC', 'dateTime', 'T ', 'H ', 'CO2']

def dataToJSON(disp, dataTime, data):
    response = {'MAC': disp, 'dateTime': dataTime}
    if (len(data) == 2):
        data.append("CO2: -414")
    for d in data:
        aux = d.split(":")
        response.update({str(aux[0]) : aux[1]})
    return response

def createFile(nameFile):
    # Crear nombre del archivo
    with open("./datos/" + nameFile, 'a') as csvfile:
        write = csv.DictWriter(csvfile, fieldnames = fieldNames)
        write.writeheader()

def writeData(disp, dataTime, nameFile, data):
    data = dataToJSON(disp, dataTime, data)
    if (path.exists("./datos/" + nameFile) != True ):
        createFile(nameFile)
    with open("./datos/" + nameFile, 'a') as csvfile:
        write = csv.DictWriter(csvfile, fieldnames = fieldNames)
        write.writerow(data)
    print "escrito con exito"