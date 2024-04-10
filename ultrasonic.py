from dotenv import load_dotenv
import os

load_dotenv()

from time import time

class Ultrasonic():
    
    def __init__(self, distance, garbage_id):
        self.distance = distance
        self.garbage_id = garbage_id
        self.timestamp = time()

    def verify_distance(self):

        try:

            if (float(self.distance) <= float(os.getenv("DISTANCE"))):
                return 1
            
            return 0
            
        except Exception as e:

            print(f"An exception ocurred: {e}")