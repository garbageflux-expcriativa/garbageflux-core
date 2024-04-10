import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

load_dotenv()

class Subscriber():

    def __init__(self):

        self.broker_address = os.getenv('BROKER_ADDRESS')
        self.port = int(os.getenv('PORT'))
        self.user = os.getenv('MQTT_USER')
        self.password = os.getenv('MQTT_PASSWORD')
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    
    def define_topic(self, topic):
        self.topic = topic
    
    def listen_message(self):
        
        def on_message( nt, userdata, message):
            print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

        # Configura credenciais
        if (self.user != "" or self.user != None):
            self.client.username_pw_set(self.user, password=self.password)

        # Define os callbacks
        self.client.on_message = on_message

        # Conecta ao broker
        self.client.connect(self.broker_address, port=self.port)

        # Assina o tópico
        self.client.subscribe(self.topic)

        # Inicia o loop para esperar por mensagens
        self.client.loop_forever()
