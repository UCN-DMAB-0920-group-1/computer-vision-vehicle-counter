from interfaces.IDao import IDao
from pymongo import MongoClient
from env import CONNECTION_STRING


class daoDetections(IDao):

    global collection
    client = MongoClient(CONNECTION_STRING)
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
            "detections": object['total']
        })
        return res