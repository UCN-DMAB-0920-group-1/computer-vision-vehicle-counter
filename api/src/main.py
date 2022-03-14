from tracking_module.tracking import Tracking
from tracking_module.streams import streams

tracker = Tracking(should_draw=True, roi_area=[
                   (100, 300), (10, 387), (516, 558), (525, 327)])
detections = tracker.track(streams["highway"])

print("total cars detected: " + str(detections["total"]))