from . import tracker
from src.tracking_module import streams
import time

if __name__ == '__main__':
    tracker = tracker.Tracker(should_draw=True,
                              should_save=False,
                              # custom_model=True, model_path="./api/models/yolov5m-custom-97.pt"
                              )

    # start_time = time.time()
    # for i in range(1):
    #     detections = tracker.track(streams.streams["file-5-sec"])
    # print("from object methods")
    # print("--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    for i in range(1):
        detections = tracker.track(streams.streams["file-5-sec"],
                                   roi=[[0, 250], [520, 90], [640, 90], [640, 719], [0, 719]])
    print("from module functions")
    print("--- %s seconds ---" % (time.time() - start_time))

    print(detections)
