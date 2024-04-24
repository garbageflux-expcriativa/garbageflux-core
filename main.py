import json
import threading
import os
from dotenv import load_dotenv

from rfid import Rfid
from ultrasonic import Ultrasonic
from subscriber import Subscriber
from publisher import Publisher

from Engine.register_manage import add_id_to_register, remove_id_from_register, is_id_registered

load_dotenv()

def on_rfid_message(message, publisher):
    print("Message received from rfid topic!")
    data = json.loads(message.payload)
    rfid = Rfid(data["id"], data["garbageid"])

    publisher.define_topic(os.getenv("ACTUATOR_TOPIC"))
    publisher.send_message(rfid.verify_rfid())
    print(f"Message SENT to {os.getenv("ACTUATOR_TOPIC")}.")

def on_ultrasonic_message(message, publisher):
    print("Message received from ultrasonic topic!")
    data = json.loads(message.payload)
    ultrasonic = Ultrasonic(data["distance"], data["garbageid"])
    
    publisher.define_topic(os.getenv("ACTUATOR_TOPIC"))
    publisher.send_message(ultrasonic.verify_distance())
    print(f"Message SENT to {os.getenv("ACTUATOR_TOPIC")}.")

    if is_id_registered(data["garbageid"]):
        publisher.define_topic(os.getenv("DASHBOARD_TOPIC"))
        publisher.send_message(message.payload)
        print(f"Message SENT to {os.getenv("DASHBOARD_TOPIC")}.")
    else:
        print(f"ID {data['garbageid']} not registered, ignoring {os.getenv("DASHBOARD_TOPIC")} publish.")

def on_register_message(message):
    data = json.loads(message.payload)
    command = data["command"]
    id = data["id"]

    if command == "add":
        if add_id_to_register(id):
            print(f"ID {id} added successfully.")
        else:
            print(f"ID {id} is already registered.")
    elif command == "remove":
        if remove_id_from_register(id):
            print(f"ID {id} removed successfully.")
        else:
            print(f"ID {id} is not registered.")

def setup_subscriber(topic, on_message_callback):
    subscriber = Subscriber(on_message_callback)
    subscriber.define_topic(topic)
    return subscriber

def run_subscriber(subscriber):
    subscriber.listen_message()

def main():
    publisher = Publisher()

    rfid_subscriber = setup_subscriber(os.getenv("RFID_TOPIC"), lambda msg: on_rfid_message(msg, publisher))
    ultrasonic_subscriber = setup_subscriber(os.getenv("ULTRASONIC_TOPIC"), lambda msg: on_ultrasonic_message(msg, publisher))
    register_subscriber = setup_subscriber(os.getenv("REGISTER_TOPIC"), lambda msg: on_register_message(msg))

    rfid_thread = threading.Thread(target=run_subscriber, args=(rfid_subscriber,))
    ultrasonic_thread = threading.Thread(target=run_subscriber, args=(ultrasonic_subscriber,))
    dashboard_thread = threading.Thread(target=run_subscriber, args=(register_subscriber,))

    rfid_thread.start()
    ultrasonic_thread.start()
    dashboard_thread.start()

    rfid_thread.join()
    ultrasonic_thread.join()
    dashboard_thread.join()

if __name__ == '__main__':
    main()
