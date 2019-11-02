#!/usr/bin/env python3
 
import paho.mqtt.client as mqtt
broker_address = "172.16.116.142"

# This is the subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("LaserLegoTank/test")
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.payload == "Hello":
        print("Received message #1, do something")
        # Do something


    if msg.payload == "World!":
        print("Received message #2, do something else")
        # Do something else
 
# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.connect(broker_address, 1883, 60)
client.on_connect = on_connect
client.on_message = on_message
 

client.loop_forever()
