import paho.mqtt.client as mqtt
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

        # Configurando usuário e senha se necessário
        if self.user and self.password:
            self.client.username_pw_set(self.user, password=self.password)
        
        # Definindo o evento de conexão
        self.client.on_connect = self.on_connect
        
        # Conectando ao broker
        self.client.connect(self.broker_address, self.port)
        
        # Iniciando o loop em segundo plano
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {reason_code}\n")

    def define_topic(self, topic):
        self.topic = topic

    def send_message(self, message):
        # Publicando mensagem no tópico definido
        self.client.publish(self.topic, message)

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
