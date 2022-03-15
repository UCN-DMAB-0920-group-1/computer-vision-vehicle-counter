from tracking_module.tracking import Tracking
from tracking_module.streams import streams

tracker = Tracking(should_draw=True, custom_model=True, model_path="./models/yolov5m-custom-97.pt",
                   roi_area=[[(0, 250), (520, 90), (640, 90), (640, 719), (0, 719)]])
detections = tracker.track(streams["file-5-sec"])

print("total cars detected: " + str(detections["total"]))
