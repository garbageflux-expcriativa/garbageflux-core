import json
import threading
import os
from dotenv import load_dotenv

from rfid import Rfid
from ultrasonic import Ultrasonic
from subscriber import Subscriber
from publisher import Publisher

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import RFID, RegisteredGarbage, Log
from Engine.register_manage import add_id_to_register, remove_id_from_register, is_id_registered, return_ids, return_rfids, add_rfid_to_register, remove_rfid_from_register

load_dotenv()

def on_rfid_message(session, message, publisher):
    print("Message received from rfid topic!")
    data = json.loads(message.payload)
    rfid = Rfid(data["id"], data["garbageid"])

    publisher.define_topic(os.getenv("ACTUATOR_TOPIC"))
    rfid_verification = rfid.verify_rfid(session)
    publisher.send_message(rfid_verification)
    print(f"Message SENT to {os.getenv('ACTUATOR_TOPIC')}.")

def on_ultrasonic_message(session, message, publisher):
    print("Message received from ultrasonic topic!")
    data = json.loads(message.payload)
    ultrasonic = Ultrasonic(data["distance"], data["garbageid"])

    publisher.define_topic(os.getenv("ACTUATOR_TOPIC"))

    ultrasonicResponse = ultrasonic.verify_distance()

    publisher.send_message(ultrasonicResponse)

    ultrasonicResponse = json.loads(ultrasonicResponse)

    print(f"Message SENT to {os.getenv('ACTUATOR_TOPIC')}.")

    if is_id_registered(session, data["garbageid"]):
        publisher.define_topic(os.getenv("DASHBOARD_TOPIC"))
        data["status"] = ultrasonicResponse["responsecode"]
        publisher.send_message(json.dumps(data))
        print(f"Message {data} SENT to {os.getenv('DASHBOARD_TOPIC')}.")
    else:
        print(f"ID {data['garbageid']} not registered, ignoring {os.getenv('DASHBOARD_TOPIC')} publish.")

def on_register_message(session, message, publisher):
    data = json.loads(message.payload)
    command = data["command"]
    id = data["id"]

    if command == "add":
        if add_id_to_register(session, id):
            print(f"ID {id} added successfully.")
        else:
            print(f"ID {id} is already registered.")
    elif command == "remove":
        if remove_id_from_register(session, id):
            print(f"ID {id} removed successfully.")
        else:
            print(f"ID {id} is not registered.")
    elif command == "request":
        registeredIds = return_ids(session)
        data = json.dumps(registeredIds)
        publisher.define_topic(os.getenv("REQUEST_TOPIC"))
        publisher.send_message(data)
        print(f"Message {data} SENT to {os.getenv('REQUEST_TOPIC')}.")

def on_register_rfid_message(session, message, publisher):
    data = json.loads(message.payload)
    command = data["command"]
    id = data["id"]

    if command == "add":
        if add_rfid_to_register(session, id):
            print(f"ID {id} added successfully.")
        else:
            print(f"ID {id} is already registered.")
    elif command == "remove":
        if remove_rfid_from_register(session, id):
            print(f"ID {id} removed successfully.")
        else:
            print(f"ID {id} is not registered.")
    elif command == "request":
        registeredIds = return_rfids(session)
        data = json.dumps(registeredIds)
        publisher.define_topic(os.getenv("REQUEST_RFID_TOPIC"))
        publisher.send_message(data)
        print(f"Message {data} SENT to {os.getenv('REQUEST_RFID_TOPIC')}.")

def setup_subscriber(topic, on_message_callback):
    subscriber = Subscriber(on_message_callback)
    subscriber.define_topic(topic)
    return subscriber

def run_subscriber(subscriber):
    subscriber.listen_message()

def main():
    Base.metadata.create_all(bind=engine)  # Cria as tabelas se ainda não existirem
    session = SessionLocal()

    publisher1 = Publisher()
    publisher2 = Publisher()
    publisher3 = Publisher()
    publisher4 = Publisher()

    rfid_subscriber = setup_subscriber(os.getenv("RFID_TOPIC"), lambda msg: on_rfid_message(session, msg, publisher1))
    ultrasonic_subscriber = setup_subscriber(os.getenv("ULTRASONIC_TOPIC"), lambda msg: on_ultrasonic_message(session, msg, publisher2))
    register_subscriber = setup_subscriber(os.getenv("REGISTER_TOPIC"), lambda msg: on_register_message(session, msg, publisher3))
    register_rfid_subscriber = setup_subscriber(os.getenv("REGISTER_RFID_TOPIC"), lambda msg: on_register_rfid_message(session, msg, publisher4))

    rfid_thread = threading.Thread(target=run_subscriber, args=(rfid_subscriber,))
    ultrasonic_thread = threading.Thread(target=run_subscriber, args=(ultrasonic_subscriber,))
    dashboard_thread = threading.Thread(target=run_subscriber, args=(register_subscriber,))
    register_rfid_thread = threading.Thread(target=run_subscriber, args=(register_rfid_subscriber,))

    rfid_thread.start()
    ultrasonic_thread.start()
    dashboard_thread.start()
    register_rfid_thread.start()

    rfid_thread.join()
    ultrasonic_thread.join()
    dashboard_thread.join()
    register_rfid_thread.start()

    session.close()

if __name__ == '__main__':
    main()
