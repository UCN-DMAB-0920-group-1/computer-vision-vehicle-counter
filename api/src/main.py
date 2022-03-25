from tracking_module import Tracking, streams

tracker = Tracking(should_draw=True,
                   save_file=False,
                   track_points='bbox',
                   # custom_model=True, model_path="./api/models/yolov5m-custom-97.pt",
                   #roi_area=[[0, 250], [520, 90], [640, 90],[640, 719], [0, 719]]
                   roi_area=[[0, 0], [1920, 0], [1920, 1080], [0, 1080]]
                   )

detections = tracker.track(streams["japan-city-night-rain"])

print(detections)
