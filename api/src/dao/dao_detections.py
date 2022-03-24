from tokenize import String
from interfaces.IDao import IDao
from pymongo import MongoClient
from datetime import datetime
from functools import reduce
import json

# Load config
with open("api/conf.json", "r") as config:
    data = json.load(config)


class dao_detections(IDao):

    global collection
    client = MongoClient(data["mongodb"])
    db = client['AI_result_database']
    collection = db['Vehicle_tracking_result']

    def find_one(id: int):
        res = collection.find_one({"_id": id})
        return res

    def insert_one(id: int, detections):
        video = id + '.mp4'
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        if("car" not in detections):
            detections["car"] = 0

        if("person" not in detections):
            detections["person"] = 0

        if("truck" not in detections):
            detections["truck"] = 0

        total = reduce(lambda a, b: a+b, detections.values())

        res = collection.insert_one({
            "_id": id,
            "video": video,
            "length": "",
            "status": "Done",
            "cars_detected": "",
            "persons_detected": "",
            "trucks_detected": "",
            "detections": total,
            "date": date
        })
        return res

    def insert_one_task(id: str, status):
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            res = collection.insert_one({
                "_id": id,
                "status": status,
                "date": date
            })
        except Exception as e:
            errorTxt = "Could not insert new task "
            print(errorTxt + str(e))
            return errorTxt
        return res

    def update_one_task(id: str, detection_result):
        video = id + '.mp4'
        cars_detected = detection_result['car'] if 'car' in detection_result else 0
        trucks_detected = detection_result['truck'] if 'truck' in detection_result else 0
        try:

            res = collection.update_one({"_id": id}, {
                "$set": {
                    "video": video,
                    "length": "",
                    "status": "Done",
                    "cars_detected": cars_detected,
                    "trucks_detected": trucks_detected,
                    "total_detections": cars_detected + trucks_detected,
                }
            })
        except Exception as e:
            errorTxt = "Could not update database value"
            print(errorTxt + str(e))
            res = errorTxt
        return res
