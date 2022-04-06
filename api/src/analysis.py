from distutils.errors import DistutilsModuleError

from matplotlib.pyplot import draw
from tracking_module import Tracker, streams
from functools import reduce
from pymongo import MongoClient
import json


class Analysis:
    """class for tracking objects via a videofeed
    """

    def __init__(
        self,
        db_collection,
        url: str,
        increment_interval: int = 5,
        start_value: int = 5,
        end_value: int = 100,
        expected: int = 61,
        roi=[[798, 149], [1238, 261], [577, 805], [389, 498], [389, 344]]
    ):
        bestDeviation = 9999
        bestValue = -1
        for value in range(start_value, end_value, increment_interval):
            tracker = Tracker(
                track_shape='bbox',
                max_distance_between_points=value,
                # confidence_threshold=(value/100),
                roi_area=roi,
                should_draw=False
            )

            print("Now running with: " + str(value) + " as distance parameter")
            detections = tracker.track(url)
            # reduce(lambda a, b: a+b, detections.values())
            total = detections["car"]
            diff = expected - total

            print("Finished tracking. found ")
            print(detections)

            if(bestDeviation < abs(diff)):
                print("New best! " + str(total))
                bestValue = value
                bestDeviation = diff

            data_to_send = {
                "total": total,
                "expected": expected,
                "diff": diff,
                "value": value,
                "bestValue": bestValue,
                "bestDeviation": bestDeviation,
            }

            db_collection.insert_one(data_to_send)


with open("api/conf.json", "r") as config:
    data = json.load(config)

global collection
client = MongoClient(data["mongodb"])
db = client['AI_result_database']
collection = db['cloudyday_distance_statistics_test']
collection.drop()

Analysis(db_collection=collection, url=streams["tokyo"], expected=46)
