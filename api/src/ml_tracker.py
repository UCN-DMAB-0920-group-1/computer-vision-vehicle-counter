from distutils.errors import DistutilsModuleError
from api.src.configuration import Configuration
from src.tracking_module import Tracker, streams
from functools import reduce
from pymongo import MongoClient
import json

actual = 61  # How many cars should be detected

start_distance = 0
increment_interval = 5
end_distance = 100


bestDist = -1
bestDeviation = 99999


global collection
client = MongoClient(Configuration.get("mongodb"))
db = client['AI_result_database']
collection = db['max_distance_statistics_test']

collection.drop()


for distance in range(start_distance, end_distance, increment_interval):
    tracker = Tracker(should_draw=True,
                      track_shape='bbox',
                      # custom_model=True, model_path="./api/models/yolov5m-custom-97.pt",
                      #roi_area=[[0, 250], [520, 90], [640, 90],[640, 719], [0, 719]]
                      max_distance_between_points=distance,
                      roi_area=[[474, 124], [638, 116], [
                          596, 697], [5, 708], [0, 332]]
                      )

    print("Now running with: " + str(distance) + " as distance parameter")
    detections = tracker.track(streams["file-1-min"])
    total = reduce(lambda a, b: a+b, detections.values())
    diff = actual - total

    print("Finished tracking. found ")
    print(detections)

    if(bestDeviation < abs(diff)):
        print("New best! " + str(total))
        bestDist = distance
        bestDeviation = diff

    data_to_send = {
        "total": total,
        "expected": actual,
        "diff": diff,
        "distance": distance,
        "bestDistance": bestDist,
        "bestDeviation": bestDeviation,
    }

    collection.insert_one(data_to_send)


print("Best distance: " + str(bestDist) +
      " with a deviation of " + str(bestDeviation))
