from time import time
import json
from sqlalchemy.orm import Session
from models import RFID, RegisteredGarbage, Log

class Rfid:
    def __init__(self, value, garbage_id):
        self.value = value
        self.garbage_id = garbage_id
        self.timestamp = time()

    def verify_rfid(self, session: Session):
        response_dict = dict()
        try:
            rfid = session.query(RFID).filter(RFID.value == self.value).first()
            if rfid:
                print("RFID is registered. Releasing RFID.  ")
                response_dict["responsecode"] = "y"
                response_dict["garbageid"] = self.garbage_id
            else:
                print("RFID is not registered. The RFID will not be released.")
                response_dict["responsecode"] = "n"
                response_dict["garbageid"] = self.garbage_id
            return json.dumps(response_dict)
        except Exception as e:
            print(f"An exception occurred: {e}")
            response_dict["responsecode"] = "error"
            response_dict["message"] = str(e)
            return json.dumps(response_dict)
