from time import time
import json

class Rfid():
    def __init__(self, id, garbage_id):
        self.id = id
        self.garbage_id = garbage_id
        self.timestamp = time()

    def verify_rfid(self):

        response_dict = dict()

        try:

            with open("rfids.json", "r") as file:

                json_content = file.read()

                data = json.loads(json_content)

                if (self.id in data["rfid"]):

                    response_dict["responsecode"] = "y"
                    response_dict["garbageid"] = self.garbage_id

                    return json.dumps(response_dict)
                
                response_dict["responsecode"] = "n"
                response_dict["garbageid"] = self.garbage_id

                return json.dumps(response_dict)
            
        except Exception as e:

            print(f"An exception ocurred: {e}")