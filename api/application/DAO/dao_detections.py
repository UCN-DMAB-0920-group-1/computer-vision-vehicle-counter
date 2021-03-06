from .idao.i_dao_detections import IDaoDetections
from pymongo import MongoClient
from datetime import datetime
from functools import reduce


class DaoDetections(IDaoDetections):

    def __init__(
        self,
        mongoClient: MongoClient,
    ):
        db = mongoClient['AI_result_database']
        self.collection = db['Vehicle_tracking_result']

    def find(self, key, value):
        res = list(self.collection.find({key: value}))
        return res

    def find_one(self, id: int):
        res = self.collection.find_one({"_id": id})
        return res

    def insert_one(self, id: int, detections):
        video = id + '.mp4'
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        if ("car" not in detections):
            detections["car"] = 0

        if ("person" not in detections):
            detections["person"] = 0

        if ("truck" not in detections):
            detections["truck"] = 0

        total = reduce(lambda a, b: a + b, detections.values())

        res = self.collection.insert_one({
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

    def insert_one_task(self, id: str, status: str, UUID: str):
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            res = self.collection.insert_one({
                "_id": id,
                "status": status,
                "date": date,
                "UUID": UUID
            })
        except Exception as e:
            errorTxt = "Could not insert new task "
            print(errorTxt + str(e))
            return errorTxt
        return res

    def update_one(self, id: str, detection_result):
        video = id + '.mp4'
        cars_detected = detection_result[
            'car'] if 'car' in detection_result else 0
        trucks_detected = detection_result[
            'truck'] if 'truck' in detection_result else 0
        try:

            res = self.collection.update_one({"_id": id}, {
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

    def delete_one(id: int):  # should delete one object with id
        pass

    def insert_many(
        object: dict
    ):  # should insert all objects with key as id and value as object
        pass
