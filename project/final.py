
#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time
import serial
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import threading
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer=23
vibration_motor1 = 24
vibration_motor2 = 25
push_btn1 = 22
push_btn2 = 27

GPIO.setup(vibration_motor1,GPIO.OUT)
GPIO.setup(vibration_motor2,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(push_btn1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(push_btn2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ser1 = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
 )

ser2 = serial.Serial(
    port='/dev/ttyUSB3',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
 )

client = mqtt.Client()
client.connect("172.16.116.142",1883,60)

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2) 
chan3 = AnalogIn(ads, ADS.P3)




counter = 0


client = mqtt.Client()
client.connect("172.16.116.142",1883,60)


  
def xbee_output_with_push():

    a = datetime.now()
    while ((datetime.now()-a).total_seconds()<=180):
        
        print("{:>5}\t{:>5}\t\t{:>5}\t{:>5}".format(chan0.value, chan1.value,chan2.value,chan3.value))
        
        bot1 = "N"
        bot2 = "n"
        shoot1 = "A"
        shoot2 = "a"
        buff = 0
        
        #if((chan2.value >30000 and chan3.value>20000) or (chan0.value >30000 and chan1.value>22000)):
         #   buff = 5000
            
        # setting values for bot 1
        
        if GPIO.input(push_btn1) == GPIO.HIGH:
            shoot1 = "S"
        
            
        if GPIO.input(push_btn2) == GPIO.HIGH:
            shoot2 = "s"
        
        #print(shoot1)
        #print(shoot2)    

        
        
        if(chan2.value-buff>17000 and chan3.value-buff<11000):
            bot1 = "R"
        elif(chan2.value-buff>18000 and chan3.value-buff>25000):
            bot1 = "L"
        elif(chan2.value-buff>25000 and chan3.value-buff>17000):
            bot1 = "U"
        elif(chan2.value-buff<10000 and chan3.value-buff>18000):
            bot1 = "B"
        else:
            bot1 = "N"
        
        
        # setting values for bot 2

        
        if(chan0.value-buff>18000 and chan1.value-buff<11000):
            bot2 = "r"
        elif(chan0.value-buff>18000 and chan1.value-buff>25000):
            bot2 = "l"
        elif(chan0.value-buff>25000 and chan1.value-buff>17000):
            bot2 = "u"
        elif(chan0.value-buff<10000 and chan1.value-buff>12000):
            bot2 = "b"
        else:
            bot2 = "n"
 
            
            
        ser1.write(str.encode(shoot1+bot1))
        time.sleep(0.02)    
        ser2.write(str.encode(shoot2+bot2))
        
        time.sleep(0.2)
        

def xbee_output_without_push():

    a = datetime.now()
    while ((datetime.now()-a).total_seconds()<=180):
        
        print("{:>5}\t{:>5}\t\t{:>5}\t{:>5}".format(chan0.value, chan1.value,chan2.value,chan3.value))
         
        bot1 = "N"
        bot2 = "n"
        buff = 0
        
        if(chan2.value-buff>17000 and chan3.value-buff<11000):
            bot1 = "SR"
        elif(chan2.value-buff>18000 and chan3.value-buff>25000):
            bot1 = "SL"
        elif(chan2.value-buff>25000 and chan3.value-buff>17000):
            bot1 = "SU"
        elif(chan2.value-buff<10000 and chan3.value-buff>18000):
            bot1 = "SB"
        else:
            bot1 = "AN"
        
        
        # setting values for bot 2

        
        if(chan0.value-buff>18000 and chan1.value-buff<11000):
            bot2 = "sr"
        elif(chan0.value-buff>18000 and chan1.value-buff>25000):
            bot2 = "sl"
        elif(chan0.value-buff>25000 and chan1.value-buff>17000):
            bot2 = "su"
        elif(chan0.value-buff<10000 and chan1.value-buff>12000):
            bot2 = "sb"
        else:
            bot2 = "an"
 
            
            
        ser1.write(str.encode(bot1))
        time.sleep(0.02)    
        ser2.write(str.encode(bot2))
        
        time.sleep(0.2)

def xbee_input_without_proxy():
    Score_bot1 = 0
    Score_bot2 = 0

    a = datetime.now()
    while((datetime.now()-a).total_seconds()<=180 ):
        x1 = ser1.read(150)
        x2 = ser2.read(150)
        hit1 = 0
        hit2 = 0

        
        y1 = x1.decode("utf-8")
        y2 = x2.decode("utf-8")
        
        print(y1)
        print("Above is y1")
        print(y2)
        
        for char in y2:
            if (char == 'q' or char == 'w') and hit2 == 0:
                if (char == 'q'):
                    Score_bot1 = Score_bot1 + 20
                if (char =='w'):
                    Score_bot1 = Score_bot1+10
                hit2 = 1
                GPIO.output(vibration_motor2,GPIO.HIGH)
                time.sleep(0.075)
                GPIO.output(vibration_motor2,GPIO.LOW)            

                
                
        for char in y1:
            if (char == 'Q' or char == 'W') and hit1 == 0:
                if (char == 'Q'):
                    Score_bot2 = Score_bot2+20
                if (char =='W'):
                    Score_bot2 = Score_bot1+10
                hit1 = 1
                GPIO.output(vibration_motor1,GPIO.HIGH)
                time.sleep(0.075)
                GPIO.output(vibration_motor1,GPIO.LOW)            

        var = "Score bot 1 {}  Score bot 2 {}".format(Score_bot1, Score_bot2)
        client.publish("LaserTankBattle/Score",var);
        client.publish("LaserTankBattle/Score_tank1",Score_bot1)
        client.publish("LaserTankBattle/Score_tank2",Score_bot2)
        time.sleep(1)
    print("Score bot 1 {}  Score bot 2 {}".format(Score_bot1, Score_bot2))



def xbee_input_with_proxy():
    Score_bot1 = 0
    Score_bot2 = 0

    a = datetime.now()
    while((datetime.now()-a).total_seconds()<=180 ):
        x1 = ser1.read(150)
        x2 = ser2.read(150)
        hit1 = 0
        hit2 = 0
        touch1 = 0
        touch2 = 0
        
        y1 = x1.decode("utf-8")
        y2 = x2.decode("utf-8")
        
        print(y1)
        print("Above is y1")
        print(y2)
        
        for char in y2:
            if (char == 'q' or char == 'w') and hit2 == 0:
                if (char == 'q'):
                    Score_bot1 = Score_bot1 + 20
                if (char =='w'):
                    Score_bot1 = Score_bot1+10
                hit2 = 1
                GPIO.output(vibration_motor2,GPIO.HIGH)
                time.sleep(0.075)
                GPIO.output(vibration_motor2,GPIO.LOW)            
            if (char == 'h') and touch2 == 0:
                touch2 = 1
                Score_bot2 = Score_bot2 - 5
                
                
        for char in y1:
            if (char == 'Q' or char == 'W') and hit1 == 0:
                if (char == 'Q'):
                    Score_bot2 = Score_bot2+20
                if (char =='W'):
                    Score_bot2 = Score_bot1+10
                hit1 = 1
                GPIO.output(vibration_motor1,GPIO.HIGH)
                time.sleep(0.075)
                GPIO.output(vibration_motor1,GPIO.LOW)            
            if (char == 'H') and touch1 == 0:
                touch1 = 1
                Score_bot1 = Score_bot1 - 5
        var = "Score bot 1 {}  Score bot 2 {}".format(Score_bot1, Score_bot2)
        client.publish("LaserTankBattle/Score",var);
        client.publish("LaserTankBattle/Score_tank1",Score_bot1)
        client.publish("LaserTankBattle/Score_tank2",Score_bot2)
        time.sleep(1)
    print("Score bot 1 {}  Score bot 2 {}".format(Score_bot1, Score_bot2))

    
if __name__ == "__main__":
    while(True):        
        print("Welcome to Laser Tanks. You have entered the amazing world of Tank Battles.")
        print("Select the Level")
        print("1 : Level 1")
        print("2 : Level 2")
        print("3 : Level 3")
        print("4 : To exit game")
        val = input("Enter the level you want to play: ")
        
        if(val=='1'):
            GPIO.output(buzzer,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzer,GPIO.LOW)
            t1 = threading.Thread(target=xbee_output_without_push) 
            t2 = threading.Thread(target=xbee_input_without_proxy)
            
            # starting thread 1 
            t1.start() 
            # starting thread 2 
            t2.start() 
            
            t1.join()
            t2.join()
            ser1.write(str.encode("AN"))    
            time.sleep(0.015)
            ser2.write(str.encode("an"))
            
            GPIO.output(buzzer,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzer,GPIO.LOW)               
            
        elif(val=='2'):
            GPIO.output(buzzer,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzer,GPIO.LOW)
            
            t1 = threading.Thread(target=xbee_output_with_push) 
            t2 = threading.Thread(target=xbee_input_without_proxy)

            # starting thread 1 
            t1.start() 
            # starting thread 2 
            t2.start() 

            t1.join()
            t2.join()
            ser1.write(str.encode("AN"))    
            time.sleep(0.015)
            ser2.write(str.encode("an"))
            
            GPIO.output(buzzer,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzer,GPIO.LOW)
            
        elif(val=='3'):
            GPIO.output(buzzer,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzer,GPIO.LOW)
            
            t1 = threading.Thread(target=xbee_output_with_push) 
            t2 = threading.Thread(target=xbee_input_with_proxy)

            # starting thread 1 
            t1.start() 
            # starting thread 2 
            t2.start() 

            t1.join()
            t2.join()
            ser1.write(str.encode("AN"))    
            time.sleep(0.015)
            ser2.write(str.encode("an"))
            
            GPIO.output(buzzer,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzer,GPIO.LOW)
        
        elif(val=='4'):
            print("Thanking for playing the Laser Tank Battle Game :)")
            break
        else:
            print("Enter a valid input")
        
    
    client.disconnect()
    ser1.write(str.encode("N"))    
    time.sleep(0.015)
    ser2.write(str.encode("n"))
    

