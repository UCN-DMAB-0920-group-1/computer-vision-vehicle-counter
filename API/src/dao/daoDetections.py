from interfaces.IDao import IDao
from pymongo import MongoClient
from datetime import datetime
import json

# Load config
with open("api/conf.json", "r") as config:
    data = json.load(config)


class daoDetections(IDao):

    global collection
    client = MongoClient(data["mongodb"])
    db = client['AI_result_database']
    collection = db['Vehicle_tracking_result']

    def find_one(id: int):
        res = collection.find_one({"_id": id})
        return res

    def insert_one(id: int, object):
        video = id + '.mp4'
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        res = collection.insert_one({
            "_id": id,
            "video": video,
            "detections": object['total'],
            "date": date
        })
        return res
