/*
 *  eHealth sensor platform for Arduino and Raspberry from Cooking-hacks.
 *
 *  Description: "The e-Health Sensor Shield allows Arduino and Raspberry Pi 
 *  users to perform biometric and medical applications by using 9 different 
 *  sensors: Pulse and Oxygen in Blood Sensor (SPO2), Airflow Sensor (Breathing),
 *  Body Temperature, Electrocardiogram Sensor (ECG), Glucometer, Galvanic Skin
 *  Response Sensor (GSR - Sweating), Blood Pressure (Sphygmomanometer) and 
 *  Patient Position (Accelerometer)." 
 *  
 *  In this example we are going to get data stored in the blood pressure sensor 
 *  memory and show the result in the serial monitor.   
 *
 *  Copyright (C) 2012 Libelium Comunicaciones Distribuidas S.L.
 *  http://www.libelium.com
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/> .
 *
 *  Version 2.0
 *  Author: Ahmad Saad  & Luis Martin
 */


#include <eHealth.h>

void setup() { 

  eHealth.readBloodPressureSensor();
  Serial.begin(115200);
  delay(100);    
}

void loop() { 

  uint8_t numberOfData = eHealth.getBloodPressureLength();   
  Serial.print(F("Number of measures : "));    
  Serial.println(numberOfData, DEC);   
  delay(100);


  for (int i = 0; i<numberOfData; i++) { 
    // The protocol sends data in this order 
    Serial.println(F("=========================================="));

    Serial.print(F("Measure number "));
    Serial.println(i + 1);

    Serial.print(F("Date -> ")); 
    Serial.print(eHealth.bloodPressureDataVector[i].day); 
    Serial.print(F(" of ")); 
    Serial.print(eHealth.numberToMonth(eHealth.bloodPressureDataVector[i].month));
    Serial.print(F(" of "));
    Serial.print(2000 + eHealth.bloodPressureDataVector[i].year);    
    Serial.print(F(" at "));

    if (eHealth.bloodPressureDataVector[i].hour < 10) {
      Serial.print(0); // Only for best representation.
    }

    Serial.print(eHealth.bloodPressureDataVector[i].hour);
    Serial.print(F(":"));

    if (eHealth.bloodPressureDataVector[i].minutes < 10) {
      Serial.print(0);// Only for best representation.
    }
    Serial.println(eHealth.bloodPressureDataVector[i].minutes);

    Serial.print(F("Systolic value : ")); 
    Serial.print(30+eHealth.bloodPressureDataVector[i].systolic);
    Serial.println(F(" mmHg"));
    
    Serial.print(F("Diastolic value : ")); 
    Serial.print(eHealth.bloodPressureDataVector[i].diastolic);
    Serial.println(F(" mmHg"));
    
    Serial.print(F("Pulse value : ")); 
    Serial.print(eHealth.bloodPressureDataVector[i].pulse);
    Serial.println(F(" bpm"));
  }

  delay(20000);
}



