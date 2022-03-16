from chardet import detect
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
            "cars_detected": detections["car"],
            "persons_detected": detections["person"],
            "trucks_detected": detections["truck"],
            "detections": total,
            "date": date
        })
        return res
