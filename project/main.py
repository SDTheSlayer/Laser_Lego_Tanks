#!/usr/bin/env python
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
GPIO.setup(buzzer,GPIO.OUT)

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
 )

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2) 
chan3 = AnalogIn(ads, ADS.P3)

Score_bot1 = 0
Score_bot2 = 0

GPIO.output(buzzer,GPIO.HIGH)
time.sleep(1)
GPIO.output(buzzer,GPIO.LOW)

counter = 0


def xbee_output():

    a = datetime.now()
    while ((datetime.now()-a).total_seconds()<=60):
        
        print("{:>5}\t{:>5}\t\t{:>5}\t{:>5}".format(chan0.value, chan1.value,chan2.value,chan3.value))
        
        bot1 = "N"
        bot2 = "N"
        buff = 0
        
        if((chan2.value >28000 and chan3.value>20000) or (chan0.value >28000 and chan1.value>22000)):
            buff = 5000
            
        # setting values for bot 1
        if(chan2.value >28000 and chan3.value>20000):
            bot1 = "S"
        elif(chan2.value-buff>17000 and chan3.value-buff<11000):
            bot1 = "R"
        elif(chan2.value-buff>18000 and chan3.value-buff>25000):
            bot1 = "L"
        elif(chan2.value-buff>25000 and chan3.value-buff>18000):
            bot1 = "U"
        elif(chan2.value-buff<10000 and chan3.value-buff>18000):
            bot1 = "B"
        else:
            bot1 = "N"
        
        # setting values for bot 2
        if(chan0.value >28000 and chan1.value>22000):
            bot2 = "s"
        elif(chan0.value-buff>18000 and chan1.value-buff<11000):
            bot2 = "r"
        elif(chan0.value-buff>18000 and chan1.value-buff>25000):
            bot2 = "l"
        elif(chan0.value-buff>25000 and chan1.value-buff>18000):
            bot2 = "u"
        elif(chan0.value-buff<10000 and chan1.value-buff>12000):
            bot2 = "b"
        else:
            bot2 = "n"
            
            
        ser.write(str.encode(bot1))    
        ser.write(str.encode(bot2))
        
        time.sleep(0.25)
        
        

def xbee_input():
    a = datetime.now()
    while((datetime.now()-a).total_seconds()<=60 ):
        x= ser.read(50)
        hit1 = 0
        hit2 = 0
        touch1 = 0
        touch2 = 0
        print(x)
        for char in x:
            if (char == 'q' or char == 'w') and hit2 == 0:
                hit2 = 1
                if (char == 'q'):
                    Score_bot1 += 20
                if (char2 =='w'):
                    Score_bot1 += 10
            if (char == 'Q' or char == 'W') and hit1 == 0:
                hit1 = 1
                if (char == 'Q'):
                    Score_bot2 += 20
                if (char2 =='W'):
                    Score_bot2 += 10
            if (char == 'h') and touch2 == 0:
                touch2 = 1
                Score_bot2 -= 5
            if (char == 'H') and touch1 == 0:
                touch1 = 1
                Score_bot1 -= 5
        
        time.sleep(1)

        
        
if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=xbee_output) 
    t2 = threading.Thread(target=xbee_input)
    
    # starting thread 1 
    t1.start() 
    # starting thread 2 
    t2.start() 
    
    t1.join()
    t2.join()
    print("Score bot 1 {}  Score bot 2 {}".format(Score_bot1, Score_bot2))
    
GPIO.output(buzzer,GPIO.HIGH)
time.sleep(1)
GPIO.output(buzzer,GPIO.LOW)
