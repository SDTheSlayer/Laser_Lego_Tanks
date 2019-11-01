// We'll use SoftwareSerial to communicate with the XBee:
#include <SoftwareSerial.h>

#define RFront  3
#define RBack  4
#define LFront  5 
#define LBack  6
#define Laser 7

//For Atmega2560, ATmega32U4, etc.
// XBee's DOUT (TX) is connected to pin 10 (Arduino's Software RX)
// XBee's DIN (RX) is connected to pin 11 (Arduino's Software TX)
SoftwareSerial XBee(10, 11); // RX, TX



void setup()
{
  // Set up both ports at 9600 baud. This value is most important
  // for the XBee. Make sure the baud rate matches the config
  // setting of your XBee.
  XBee.begin(9600);
  Serial.begin(9600);
  
  pinMode(LFront, OUTPUT);
  pinMode(RFront, OUTPUT);
  pinMode(RBack, OUTPUT);
  pinMode(LBack, OUTPUT);
  pinMode(Laser, OUTPUT);
}

void loop()
{  
  int ldr_front_value = analogRead(A0);
  //int ldr_left_value = analogRead(A1);
  //int ldr_right_value = analogRead(A2);
  
  if(XBee.available()){
    XBee.write(ldr_front_value);
    char c = XBee.read();
    Serial.println(c);
    if(c=='S')
       digitalWrite(Laser,HIGH);
    else if(c=='U')
     {
        digitalWrite(LFront,HIGH); 
        digitalWrite(RFront,HIGH);
        digitalWrite(Laser,LOW);
     }
    else if(c=='R')
    {
      digitalWrite(LFront,HIGH);
      digitalWrite(RBack,HIGH);
      digitalWrite(Laser,LOW);
    }
    else if(c=='L')
    {
      digitalWrite(RFront,HIGH); 
      digitalWrite(LBack,HIGH);
      digitalWrite(Laser,LOW);
    }
    else if(c=='B')
    {
      digitalWrite(LBack,HIGH);
      digitalWrite(RBack,HIGH);
      digitalWrite(Laser,LOW);
    }
    else if(c=='N')
    {
      digitalWrite(LFront,LOW); 
      digitalWrite(RFront,LOW);
      digitalWrite(LBack,LOW);
      digitalWrite(RBack,LOW);
      digitalWrite(Laser,LOW);
    }
    delay(200);    //delay is nessecary to write properly
    
  }
}
