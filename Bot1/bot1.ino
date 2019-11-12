// We'll use SoftwareSerial to communicate with the XBee:
#include <SoftwareSerial.h>

#define RFront  3
#define RBack  4
#define LFront  5 
#define LBack  6
#define Laser 7
#define ProxSensor 2
#define led 1
//For Atmega2560, ATmega32U4, etc.
// XBee's DOUT (TX) is connected to pin 10 (Arduino's Software RX)
// XBee's DIN (RX) is connected to pin 11 (Arduino's Software TX)
SoftwareSerial XBee(10, 11); // RX, TX
char hit = 'X';
int count = -1;
int period = 6;

void setup()
{
  
  XBee.begin(9600);
  //Serial.begin(9600);
   
  pinMode(LFront, OUTPUT);
  pinMode(RFront, OUTPUT);
  pinMode(RBack, OUTPUT);
  pinMode(LBack, OUTPUT);
  pinMode(Laser, OUTPUT);
  pinMode(led, OUTPUT);    
  //Pin 2 is connected to the output of proximity sensor
  pinMode(ProxSensor,INPUT);

}

void loop()
{ 
  
  char touch = 'G';
  
  if(digitalRead(ProxSensor)==HIGH)      //Check the sensor output
  {
    touch = 'H';  
  }
  else
  {
    touch  = 'G';
  }  
  
  int ldr_front_value = analogRead(A0);
  int ldr_left_value = analogRead(A1);
  int ldr_right_value = analogRead(A2);
  
  
  if(ldr_front_value > 930){
    hit = 'Q';
  }
  if(ldr_left_value > 930){
    hit = 'W';
  }
  if(ldr_right_value > 930){
    hit = 'W';
  }
  // Serial.println(ldr_right_value);   
  if(XBee.available()){
    
    count++;
    count %= period;
    
    
    if(hit == 'X'){
      if(count == 0){
      
      digitalWrite(led,LOW);
      
      }
    } 
    
    
    // Serial.println(hit);
    XBee.write(hit);
    
    if(hit == 'Q' || hit == 'W'){
      
      digitalWrite(led,HIGH);
      count = 0;
    
    }
    
    hit = 'X';
    XBee.write(touch);
    char c = XBee.read();
    
    
    //Serial.println(c);
    if(c=='S')
      digitalWrite(Laser,HIGH);
    else if(c == 'A')
      digitalWrite(Laser,LOW);
    else if(c=='U')
    {
        
      digitalWrite(LBack,LOW);
      digitalWrite(RBack,LOW);
      digitalWrite(LFront,HIGH); 
      digitalWrite(RFront,HIGH);
    
    }
    else if(c=='R')
    {
      
      digitalWrite(LBack,LOW);
      digitalWrite(RFront, LOW);    
      digitalWrite(LFront,HIGH);
      digitalWrite(RBack,HIGH);
    
    }
    else if(c=='L')
    {
      
      digitalWrite(LFront,LOW);
      digitalWrite(RBack,LOW);    
      digitalWrite(RFront,HIGH); 
      digitalWrite(LBack,HIGH);
    
    }
    else if(c=='B')
    {
      
      digitalWrite(LFront,LOW);
      digitalWrite(RFront,LOW);
      digitalWrite(LBack,HIGH);
      digitalWrite(RBack,HIGH);
    
    }
    else if(c == 'N')
    {
        
      digitalWrite(LFront,LOW); 
      digitalWrite(RFront,LOW);
      digitalWrite(LBack,LOW);
      digitalWrite(RBack,LOW);
      
    }
    // Serial.println(touch);
    delay(60);    //delay is nessecary to write properly
  
  }
}
