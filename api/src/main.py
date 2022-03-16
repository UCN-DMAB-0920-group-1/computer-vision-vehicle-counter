from tracking_module import Tracking, streams

tracker = Tracking(
    should_draw=True,
    custom_model=True, model_path="./models/yolov5m-custom-97.pt",
    roi_area=[[(0, 0), (1920, 0), (1920, 1080), (0, 1080)]])

detections = tracker.track(streams["file"])

print(detections)
