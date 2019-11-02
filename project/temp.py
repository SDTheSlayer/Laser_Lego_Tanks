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

    
while counter <= 200:
    
    # print("{:>5}\t{:>5}\t\t{:>5}\t{:>5}".format(chan0.value, chan1.value,chan2.value,chan3.value))
    
    bot1 = "N"
    bot2 = "N"
    buff = 0
    
    if((chan0.value >28000 and chan1.value>23000) or (chan2.value >28000 and chan3.value>22000)):
        buff = 5000
        
    # setting values for bot 1
    if(chan0.value >28000 and chan1.value>23000):
        bot1 = "S"
    elif(chan0.value-buff>18000 and chan1.value-buff<11000):
        bot1 = "R"
    elif(chan0.value-buff>18000 and chan1.value-buff>25000):
        bot1 = "L"
    elif(chan0.value-buff>25000 and chan1.value-buff>18000):
        bot1 = "U"
    elif(chan0.value-buff<10000 and chan1.value-buff>18000):
        bot1 = "B"
    else:
        bot1 = "N"
    
    # setting values for bot 2
    if(chan2.value >28000 and chan3.value>22000):
        bot2 = "s"
    elif(chan2.value-buff>18000 and chan3.value-buff<11000):
        bot2 = "r"
    elif(chan2.value-buff>18000 and chan3.value-buff>25000):
        bot2 = "l"
    elif(chan2.value-buff>25000 and chan3.value-buff>18000):
        bot2 = "u"
    elif(chan2.value-buff<10000 and chan3.value-buff>15000):
        bot2 = "b"
    else:
        bot2 = "n"
        
        
    ser.write(str.encode(bot1))    
    ser.write(str.encode(bot2))
    
    x=ser.read()
    y=ser.read()
    
    print(x)
    print(y)
    
    if(x=='q'):
        Score_bot1 = Score_bot1 + 2
    if(x=='w'):
        Score_bot1 = Score_bot1 + 1
    if(x=='e'):
        Score_bot1 = Score_bot1 + 1
    
    if(x=='Q'):
        Score_bot2 = Score_bot2 + 2
    if(x=='W'):
        Score_bot2 = Score_bot2 + 1
    if(x=='E'):
        Score_bot2 = Score_bot2 + 1
        
    time.sleep(0.1)
    
    x=ser.read()
    y=ser.read()
    
    print(x)
    print(y)
    
    if(x=='q'):
        Score_bot1 = Score_bot1 + 2
    if(x=='w'):
        Score_bot1 = Score_bot1 + 1
    if(x=='e'):
        Score_bot1 = Score_bot1 + 1
    
    if(x=='Q'):
        Score_bot2 = Score_bot2 + 2
    if(x=='W'):
        Score_bot2 = Score_bot2 + 1
    if(x=='E'):
        Score_bot2 = Score_bot2 + 1
        
    time.sleep(0.1)
    
    x=ser.read()
    y=ser.read()
    
    print(x)
    print(y)
    
    if(x=='q'):
        Score_bot1 = Score_bot1 + 2
    if(x=='w'):
        Score_bot1 = Score_bot1 + 1
    if(x=='e'):
        Score_bot1 = Score_bot1 + 1
    
    if(x=='Q'):
        Score_bot2 = Score_bot2 + 2
    if(x=='W'):
        Score_bot2 = Score_bot2 + 1
    if(x=='E'):
        Score_bot2 = Score_bot2 + 1
        
    time.sleep(0.1)
    
    x=ser.read()
    y=ser.read()
    
    print(x)
    print(y)
    
    if(x=='q'):
        Score_bot1 = Score_bot1 + 2
    if(x=='w'):
        Score_bot1 = Score_bot1 + 1
    if(x=='e'):
        Score_bot1 = Score_bot1 + 1
    
    if(x=='Q'):
        Score_bot2 = Score_bot2 + 2
    if(x=='W'):
        Score_bot2 = Score_bot2 + 1
    if(x=='E'):
        Score_bot2 = Score_bot2 + 1
        
    time.sleep(0.1)
    
    x=ser.read()
    y=ser.read()
    
    print(x)
    print(y)
    
    if(x=='q'):
        Score_bot1 = Score_bot1 + 2
    if(x=='w'):
        Score_bot1 = Score_bot1 + 1
    if(x=='e'):
        
        Score_bot1 = Score_bot1 + 1
    
    if(x=='Q'):
        Score_bot2 = Score_bot2 + 2
    if(x=='W'):
        Score_bot2 = Score_bot2 + 1
    if(x=='E'):
        Score_bot2 = Score_bot2 + 1
        
    time.sleep(0.1)
    
    
    counter += 1

GPIO.output(buzzer,GPIO.HIGH)
time.sleep(1)
GPIO.output(buzzer,GPIO.LOW)
