#include <DHT.h>
#include <stdlib.h>
#include <XBee.h>
#include "Adafruit_CCS811.h"

#define pindht 5
#define DHTTYPE DHT22

Adafruit_CCS811 ccs;

//---------Objetos

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
DHT dht (pindht, DHTTYPE);

//--------- SH + SL Address of receiving XBee
XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x40dc588f);

//variable mensaje
char payload[50];
char aux[10];

//variable para el estado del envio
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

//---------------------Conversion de float a char
void floatAchar(float num, char resultado[10])
{
  //dtostrf(variable,mumero de digitos,numero de decimales,matriz);
  dtostrf(num, 5, 2, resultado);

}

void setup()
{

  Serial.begin(9600);
  xbee.setSerial(Serial);
  dht.begin();

  // Inicio de sensor CO2
  if(!ccs.begin()){
    Serial.println("Fallo en sensor CO2");
    while(1);
  }

  // Esperar a que el sensor de CO2 este disponible
  while(!ccs.available());
}

void loop()
{
  
  //lectura de sensor dht11
  float humedad = dht.readHumidity();
  float temperatura = dht.readTemperature();
  //chequeo si son valores nulos
  if (!isnan(temperatura) && !isnan(humedad) && ccs.available())
  {
    floatAchar(humedad, aux);
    Serial.print(aux);
    strcpy(payload, "H :");
    strcat(payload, aux);
    strcat(payload, "#");
    floatAchar(temperatura, aux);
    Serial.print(aux);
    strcat(payload, "T :");
    strcat(payload, aux);
    strcat(payload, "#");
    if(!ccs.readData()){
      floatAchar(ccs.geteCO2(), aux);
      Serial.print(aux);
      strcat(payload, "CO2: ");
      strcat(payload, aux);
      strcat(payload, "#");
    }
    else{
      Serial.println("Sensor CO2 no disponible");
      delay(1000);
    }
    Serial.println(payload);

  }

  //Envio de mensaje-----------------------------------------------------------------------

  ZBTxRequest mensaje = ZBTxRequest(addr64, (uint8_t*)payload, sizeof(payload));
  xbee.send(mensaje);

  if (xbee.readPacket(500))
  {
    // se obtuvo respuesta
    if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE)
    {
      xbee.getResponse().getZBTxStatusResponse(txStatus);

      // estado del envio
      if (txStatus.getDeliveryStatus() == SUCCESS)
      {

        Serial.println("Logrado");
      }
      else
      {
        //El destinatario no a recibido el mensaje
        Serial.println("Mensaje perdido");
      }
    }

  }
  else if (xbee.getResponse().isError())
  {
    Serial.print("error al leer el paquete, codigo: ");
    Serial.println(xbee.getResponse().getErrorCode());
  }
  else
  {
    Serial.println("Esto no deberia pasar");
  }
  // ------------------------------------------ Limpieza mensaje

  strcpy(payload, "");

  delay(60000);
}
