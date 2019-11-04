import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads,ADS.P1)
chan2 = AnalogIn(ads,ADS.P2)
chan3 = AnalogIn(ads,ADS.P3)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}\t\t{:>5}\t{:>5}".format('v1', 'v2', 'v3', 'v4'))

while True:
    print("{:>5}\t{:>5}\t\t{:>5}\t{:>5}".format(chan0.value, chan1.value,chan2.value,chan3.value))
    time.sleep(0.2)
