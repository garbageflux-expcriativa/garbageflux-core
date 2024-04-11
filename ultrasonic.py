from dotenv import load_dotenv
import os
import json

load_dotenv()

from time import time

class Ultrasonic():
    
    def __init__(self, distance, garbage_id):
        self.distance = distance
        self.garbage_id = garbage_id
        self.timestamp = time()

    def verify_distance(self):

        response_dict = dict()

        try:

            if (float(self.distance) <= float(os.getenv("DISTANCE"))):

                response_dict["responsecode"] = "1"
                response_dict["garbageid"] = self.garbage_id

                return json.dumps(response_dict)
            
            response_dict["responsecode"] = "0"
            response_dict["garbageid"] = self.garbage_id

            return json.dumps(response_dict)
            
        except Exception as e:

            print(f"An exception ocurred: {e}")