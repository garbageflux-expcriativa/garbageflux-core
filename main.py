import json
import threading
import os
from dotenv import load_dotenv

from rfid import Rfid
from ultrasonic import Ultrasonic
from subscriber import Subscriber
from publisher import Publisher

load_dotenv()

def on_rfid_message(message):
    data = json.loads(message.payload)
    rfid = Rfid(data["id"], data["garbageid"])

    publisher = Publisher()
    publisher.define_topic(os.getenv("ACTUATOR_TOPIC"))
    publisher.send_message(rfid.verify_rfid())

def on_ultrasonic_message(message):
    data = json.loads(message.payload)
    ultrasonic = Ultrasonic(data["distance"], data["garbageid"])
    
    publisher = Publisher()
    publisher.define_topic(os.getenv("ACTUATOR_TOPIC"))
    publisher.send_message(ultrasonic.verify_distance())

def setup_subscriber(topic, on_message_callback):
    subscriber = Subscriber()
    subscriber.define_topic(topic)
    subscriber.client.on_message = on_message_callback
    return subscriber

def run_subscriber(subscriber):
    subscriber.client.loop_start()
    subscriber.listen_message()

def main():
    rfid_subscriber = setup_subscriber(os.getenv("RFID_TOPIC"), on_rfid_message)
    ultrasonic_subscriber = setup_subscriber(os.getenv("ULTRASONIC_TOPIC"), on_ultrasonic_message)

    rfid_thread = threading.Thread(target=run_subscriber, args=(rfid_subscriber,))
    ultrasonic_thread = threading.Thread(target=run_subscriber, args=(ultrasonic_subscriber,))

    rfid_thread.start()
    ultrasonic_thread.start()

    rfid_thread.join()
    ultrasonic_thread.join()

if __name__ == '__main__':
    main()
