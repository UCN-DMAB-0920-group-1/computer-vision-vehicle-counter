from tracking_module import Tracking, streams

tracker = Tracking(should_draw=True,
                   track_points='bbox',
                   custom_model=True, model_path="./api/models/yolov5m-custom-97.pt",
                   roi_area=[[(0, 250), (520, 90), (640, 90), (640, 719), (0, 719)]])

detections = tracker.track(streams["file-5-sec"])

print(detections)
