import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

load_dotenv()

class Publisher():

    def __init__(self):

        self.broker_address = os.getenv('BROKER_ADDRESS')
        self.port = int(os.getenv('PORT'))
        self.user = os.getenv('MQTT_USER')
        self.password = os.getenv('MQTT_PASSWORD')
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


    def define_topic(self, topic):
        self.topic = topic

    def send_message(self, message):

        try:
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    print("Connected to MQTT Broker!")
                else:
                    print("Failed to connect, return code %d\n", rc)
        except:
            pass
    

        if (self.user != "" or self.user != None):
            self.client.username_pw_set(self.user, password=self.password)

        self.client.on_connect = on_connect
        self.client.connect(self.broker_address, port=self.port)

        self.client.loop_start()
        self.client.publish(self.topic, message)
        self.client.loop_stop()
