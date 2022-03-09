from tracking import Tracking
from streams import streams

tracker = Tracking(should_draw=False, roi_area=[
                   (100, 300), (10, 387), (516, 558), (525, 327)])
detections = tracker.track(streams["highway"])

print("total cars detected: " + str(detections["total"]))
