# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish

publish.single("LaserLegoTank/test", "Hello", hostname="test.mosquitto.org")
publish.single("LaserLego/topic", "World!", hostname="test.mosquitto.org")
print("Done")
