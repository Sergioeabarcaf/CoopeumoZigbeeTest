import httplib
import base64
import json

username = "idiProteinlab"
password = "Proteinlab2017!"

def obtenerData(dataValues):
    data = dataValues.split("#")
    data.pop(len(data) - 1)
    if ( len(data) < 4):
        return data
    else:
        return False

def getDataDevice(id,cantidad):
    link = "/ws/v1/streams/history/00000000-00000000-00409DFF-FF6496C2/xbee.serialIn/["+ id + "]!?size=" + str(cantidad) + "&order=desc"
    auth = base64.encodestring("%s:%s"%(username,password))[:-1]
    webservice = httplib.HTTPSConnection("remotemanager.digi.com")
    webservice.putrequest("GET", link)
    webservice.putheader("Authorization", "Basic %s"%auth)
    webservice.endheaders()
    response = webservice.getresponse()
    if (response.status == 200):
        return response.read()
    else:
        return response.status

def getDataInit(id,cantidad,dateStart):
    link = "/ws/v1/streams/history/00000000-00000000-00409DFF-FF6496C2/xbee.serialIn/["+ id + "]!?size=" + str(cantidad) + "&order=desc&start_time=" + str(dateStart)
    auth = base64.encodestring("%s:%s"%(username,password))[:-1]
    webservice = httplib.HTTPSConnection("remotemanager.digi.com")
    webservice.putrequest("GET", link)
    webservice.putheader("Authorization", "Basic %s"%auth)
    webservice.endheaders()
    response = webservice.getresponse()
    if (response.status == 200):
        return response.read()
    else:
        return response.status
