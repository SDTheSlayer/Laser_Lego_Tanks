/*
  Thumb Joystick demo v1.0
  by:http://www.seeedstudio.com
  connect the module to A0&A1 for using;
*/

#define RFront  3
#define RBack  4
#define LFront  5 
#define LBack  6
#define Laser 7
 
void setup()
{
    Serial.begin(9600);
     pinMode(LFront, OUTPUT);
     pinMode(RFront, OUTPUT);
     pinMode(RBack, OUTPUT);
     pinMode(LBack, OUTPUT);
          pinMode(Laser, OUTPUT);
}

void loop()
{
    int joyY = analogRead(A0);
    int joyX = analogRead(A1);
    digitalWrite(LBack,LOW);
    digitalWrite(RFront,LOW);
    digitalWrite(LFront,LOW);
    digitalWrite(RBack,LOW);
    digitalWrite(Laser,LOW);
    Serial.print("The Y and X coordinate is:");
    Serial.print(joyY, DEC);
    Serial.print(",");
    Serial.println(joyX, DEC);
    Serial.println(" ");
    
      if(joyY>600)
      {
          Serial.println("Hit!");
          digitalWrite(Laser,HIGH);
          //delay(100);
          //digitalWrite(Laser,LOW);
      }
    else if( joyY > 500 &&joyY<600)
    {
      digitalWrite(LFront,HIGH); 
      digitalWrite(RFront,HIGH);
       Serial.println("Front");
       digitalWrite(Laser,LOW);
    }
    else if( joyY <200)
    {
      digitalWrite(LBack,HIGH);
      digitalWrite(RBack,HIGH);
      Serial.println("Back");
      digitalWrite(Laser,LOW);
    }
    else if( joyX > 500)
    {
      digitalWrite(RFront,HIGH); 
      digitalWrite(LBack,HIGH);
      Serial.println("Left");
      digitalWrite(Laser,LOW);
    }
    else if( joyX <200)
    {
      digitalWrite(LFront,HIGH);
      digitalWrite(RBack,HIGH);
      Serial.println("Right");
      digitalWrite(Laser,LOW);
    }
    delay(200);
 
}
