import json
import threading
import os
from dotenv import load_dotenv

from rfid import Rfid
from ultrasonic import Ultrasonic
from subscriber import Subscriber
from publisher import Publisher

load_dotenv()

def on_rfid_message(message, publisher):
    data = json.loads(message.payload)
    rfid = Rfid(data["id"], data["garbageid"])

    publisher.define_topic(os.getenv("ACTUATOR_TOPIC"))
    publisher.send_message(rfid.verify_rfid())

def on_ultrasonic_message(message, publisher):
    data = json.loads(message.payload)
    ultrasonic = Ultrasonic(data["distance"], data["garbageid"])
    
    publisher.define_topic(os.getenv("ACTUATOR_TOPIC"))
    publisher.send_message(ultrasonic.verify_distance())

    publisher.define_topic(os.getenv("DASHBOARD_TOPIC"))
    publisher.send_message(ultrasonic.verify_distance())

def setup_subscriber(topic, on_message_callback):
    subscriber = Subscriber(on_message_callback)
    subscriber.define_topic(topic)
    return subscriber

def run_subscriber(subscriber):
    subscriber.listen_message()

def main():
    publisher = Publisher()
    publisher.define_topic(os.getenv("ACTUATOR_TOPIC"))

    rfid_subscriber = setup_subscriber(os.getenv("RFID_TOPIC"), lambda msg: on_rfid_message(msg, publisher))
    ultrasonic_subscriber = setup_subscriber(os.getenv("ULTRASONIC_TOPIC"), lambda msg: on_ultrasonic_message(msg, publisher))

    rfid_thread = threading.Thread(target=run_subscriber, args=(rfid_subscriber,))
    ultrasonic_thread = threading.Thread(target=run_subscriber, args=(ultrasonic_subscriber,))

    rfid_thread.start()
    ultrasonic_thread.start()

    rfid_thread.join()
    ultrasonic_thread.join()

if __name__ == '__main__':
    main()
