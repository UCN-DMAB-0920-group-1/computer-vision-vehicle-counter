from interfaces.IDao import IDao
from pymongo import MongoClient
import json

# Load config
with open("conf.json", "r") as config:
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
        res = collection.insert_one({
            "_id": id,
            "video": video,
            "length": "" ,
            "cars detected": "",
            "persons detected": "",
            "trucks detected": "",
            "Total detections": object['total']
        })
        return res
