#include "Adafruit_CCS811.h"

Adafruit_CCS811 ccs;
int led = 13;

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);
  
  Serial.println("Quemado inicial de sensores CO2");
  if(!ccs.begin()){
    Serial.println("Sensor con fallas... esperando a conectar");
    while(1);
  }

  while(!ccs.available());
}

void loop() {
  digitalWrite(led, LOW);
  if(ccs.available()){
    if(!ccs.readData()){
      digitalWrite(led, HIGH);
      Serial.print("CO2: ");
      Serial.print(ccs.geteCO2());
      Serial.print("ppm, TVOC: ");
      Serial.print(ccs.getTVOC());
      Serial.print(", T°: ");
      Serial.println(ccs.calculateTemperature());
    }
    else{
      Serial.println("ERROR!");
      delay(1000);
    }
  }
  Serial.println("========================");
  delay(1000);
}
