import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

load_dotenv()

class Subscriber():

    def __init__(self, on_message_callback):

        self.broker_address = os.getenv('BROKER_ADDRESS')
        self.port = int(os.getenv('PORT'))
        self.user = os.getenv('MQTT_USER')
        self.password = os.getenv('MQTT_PASSWORD')
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.on_message_callback = on_message_callback  

    def define_topic(self, topic):
        self.topic = topic
    
    def listen_message(self):
        
        def on_message(client, userdata, message):
            print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")
            self.on_message_callback(message)  # Chama a função de callback

        if (self.user != ""):
            self.client.username_pw_set(self.user, password=self.password)

        self.client.on_message = on_message
        self.client.connect(self.broker_address, port=self.port)
        self.client.subscribe(self.topic)
        self.client.loop_forever()
