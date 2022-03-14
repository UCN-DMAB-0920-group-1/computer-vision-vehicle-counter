import cv2
import time
import torch
import norfair
import numpy as np
import pandas

from norfair import Tracker
from importlib.resources import path
from charset_normalizer import detect
from matplotlib.pyplot import draw

from tracking_module.util import get_stream, centroid
from tracking_module.norfair_helpers import euclidean_distance, yolo_detections_to_norfair_detections


class Tracking:

    def __init__(
        self,
        should_draw: bool = True,
        device: str = "cuda",  # Device (CPU or GPU)
        detector_path: str = "yolov5m6",  # YOLO version
        # How confidence should YOLO be, before labeling
        confidence_threshold: float = 0.5,
        track_points: str = "bbox",  # Can be centroid or bbox
        label_offset:
        int = 50,  # Offset from center point to classification label
        max_distance_between_points: int = 30,
        # TOP LEFT, BOTTOM LEFT, BOTTOM RIGHT, TOP RIGHT,
        roi_area=[(250, 300), (10, 387), (516, 558), (525, 327)]):

        # Load yolo model
        self.model = torch.hub.load(repo_or_dir="ultralytics/yolov5",
                                    model=detector_path)
        self.model.conf = confidence_threshold
        #self.model.

        self.inside_roi = []  # Int array
        self.vehicle_count = 0

        self.tracker = Tracker(
            distance_function=euclidean_distance,
            distance_threshold=max_distance_between_points,
        )

        self.track_points = track_points
        self.label_offset = label_offset
        self.roi_area = roi_area
        self.should_draw = should_draw

    def draw(self, frame, yolo_detections, norfair_detections,
             tracked_objects):
        frame_scale = frame.shape[0] / 100
        id_size = frame_scale / 10
        id_thickness = int(frame_scale / 5)

        # Draw detections, ids and center point/ bounding box
        if self.track_points == 'centroid':
            norfair.draw_points(frame, norfair_detections)
        elif self.track_points == 'bbox':
            norfair.draw_boxes(frame, norfair_detections, line_width=3)

        norfair.draw_tracked_objects(frame, tracked_objects, id_thickness=3)

        # Draw ROI
        cv2.polylines(frame, [np.array(self.roi_area, np.int32)], True,
                      (15, 220, 10), 6)

        # Draw detected label
        frame_scale = frame.shape[0] / 100
        id_size = frame_scale / 10
        id_thickness = int(frame_scale / 5)
        pand = yolo_detections.pandas().xyxy[0]
        length = len(pand.name)

        for i in range(length):
            name = pand.name[i]
            xmin = pand.xmin[i]
            xmax = pand.xmax[i]
            ymin = pand.ymin[i]
            ymax = pand.ymax[i]

            pos = {
                "x": int((xmin + xmax + self.label_offset) / 2),
                "y": int((ymin + ymax + self.label_offset) / 2),
            }

            cv2.putText(
                frame,
                name,
                (pos["x"], pos["y"]),
                cv2.FONT_HERSHEY_SIMPLEX,
                id_size,
                [26, 188, 156],  # Dynamic?
                id_thickness,
                cv2.LINE_AA,
            )

        # Draw vehicle counter
        cv2.putText(
            frame,
            "total: " + str(self.vehicle_count),
            (25, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            id_size,
            [231, 76, 60],  # Dynamic?
            id_thickness,
            cv2.LINE_AA,
        )

        cv2.putText(
            frame,
            "now: " + str(len(self.inside_roi)),
            (25, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            id_size,
            [231, 76, 60],  # Dynamic?
            id_thickness,
            cv2.LINE_AA,
        )

        # Draw the model classifications on a gui
        cv2.imshow("REALTIME!", np.squeeze(frame))

    def track(self, stream_location):

        # Ready the stream
        stream_url = get_stream(stream_location)

        # Open stream
        video_stream = cv2.VideoCapture(stream_url)
        # Open file writer
        fourcc = cv2.VideoWriter_fourcc('F', 'M', 'P', '4')
        out = cv2.VideoWriter(
            stream_location, fourcc, 20.0,
            (int(video_stream.get(3)), int(video_stream.get(4))))
        # As long as the video stream is open, run the YOLO model on the frame, and show the output
        while video_stream.isOpened():
            ret, frame = video_stream.read()

            # Ensures no error occur, even when there is no more frames to check for
            if (ret is False):
                break

            # Detect objects inside the frame
            yolo_detections = self.model(frame)

            # Convert to norfair detections
            detections = yolo_detections_to_norfair_detections(
                yolo_detections, track_points=self.track_points)

            # Update tracker
            tracked_objects = self.tracker.update(detections=detections)

            # Find ROI vehicles
            for obj in tracked_objects:
                if not obj.live_points.any():
                    continue

                track_position = centroid(obj.estimate[obj.live_points])
                # Is this object inside ROI?
                is_inside_roi = cv2.pointPolygonTest(
                    np.array(self.roi_area, np.int32), track_position, False)

                if (is_inside_roi >= 0):
                    if not obj.id in self.inside_roi:
                        self.inside_roi.append(obj.id)
                        self.vehicle_count += 1
                else:
                    if obj.id in self.inside_roi:
                        self.inside_roi.remove(obj.id)
                print(self.inside_roi)

            if (self.should_draw):
                self.draw(frame, yolo_detections, detections, tracked_objects)
            # Wait for ESC to be pressed (then exit)

            # Write file
            out.write(frame)

            if (cv2.waitKey(10) == 27):
                break
        # Safely disposed any used resources
        video_stream.release()
        out.release()
        # cv2.destroyAllWindows()

        return {"total": self.vehicle_count}
