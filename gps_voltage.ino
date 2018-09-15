#include <SoftwareSerial.h>
#include <TinyGPS.h>

int analogInput = A7;
float vout = 0.0;
float vin = 0.0;
float R1 = 30000.0; //  
float R2 = 7500.0; // 
int value = 0;

TinyGPS gps;
SoftwareSerial ss(2, 3);

void setup()
{
  pinMode(analogInput, INPUT);
  Serial.begin(9600);
  ss.begin(9600);
}

void loop()
{
  bool newData = false;
  unsigned long chars;
  unsigned short sentences, failed;
   value = analogRead(analogInput);
   vout = (value * 5.0) / 1024.0; // see text
   vin = (vout / (R2/(R1+R2)))-1.2; 
if (vin<=0){
  vin=0;   
}

  for (unsigned long start = millis(); millis() - start < 1000;)
  {
    while (ss.available())
    {
      char c = ss.read();
      if (gps.encode(c))
      newData = true;
    }
  }

  if (newData)
  {
    float flat, flon;
    unsigned long age;
    gps.f_get_position(&flat, &flon, &age);
    Serial.print("$,loc,");
    Serial.print(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6);
    Serial.print("/");
    Serial.print(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6);
//    Serial.print(" SAT=");
//    Serial.print(gps.satellites() == TinyGPS::GPS_INVALID_SATELLITES ? 0 : gps.satellites());
//    Serial.print(" PREC=");
//    Serial.print(gps.hdop() == TinyGPS::GPS_INVALID_HDOP ? 0 : gps.hdop());
  }
  else{
     Serial.print("$,loc,nodata");
   
  }
    //Serial.print("\t");
    Serial.print(",bat,");
    Serial.println(vin,2);
  gps.stats(&chars, &sentences, &failed);
//  Serial.print(" CHARS=");
//  Serial.print(chars);
//  Serial.print(" SENTENCES=");
//  Serial.print(sentences);
//  Serial.print(" CSUM ERR=");
//  Serial.println(failed);
  
  if (chars == 0)
    Serial.println("ERROR GPS");
}
