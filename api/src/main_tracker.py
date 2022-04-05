from tracking_module import streams, tracking
import time

if __name__ == '__main__':
    tracker = tracking.Tracking(should_draw=True,
                                should_save=False,
                                track_points='bbox',
                                # custom_model=True, model_path="./api/models/yolov5m-custom-97.pt",
                                roi_area=[[0, 250], [520, 90], [
                                    640, 90], [640, 719], [0, 719]]
                                #roi_area=[[0, 0], [1920, 0],[1920, 1080], [0, 1080]]
                                )

    # start_time = time.time()
    # for i in range(1):
    #     detections = tracker.track(streams.streams["file-5-sec"])
    # print("from object methods")
    # print("--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    for i in range(1):
        detections = tracking.track(streams.streams["file-5-sec"], tracker.model, tracker.tracker,
                                    tracker.roi_area, tracker.track_points, tracker.should_draw, tracker.should_draw)
    print("from module functions")
    print("--- %s seconds ---" % (time.time() - start_time))

    print(detections)
