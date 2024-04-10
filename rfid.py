from time import time
import json

class Rfid():
    def __init__(self, id, garbage_id):
        self.id = id
        self.garbage_id = garbage_id
        self.timestamp = time()

    def verify_rfid(self):

        try:

            with open("rfids.json") as file:

                data = json.loads(file)

                if (self.id in data["rfids"]):
                    return 1
                
                return 0
            
        except Exception as e:

            print(f"An exception ocurred: {e}")