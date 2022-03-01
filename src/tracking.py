
import string
from charset_normalizer import detect
from util import get_stream
from streams import streams
import argparse

import numpy as np
import torch
import yolov5
from typing import Union, List, Optional

import norfair
from norfair import Tracker

import cv2
import time

from norfair_helpers import euclidean_distance, yolo_detections_to_norfair_detections


# Defaults
device: str = "cuda"  # Device (CPU or GPU)
detector_path: str = "yolov5n"  # YOLO version
img_size: int = 720
# How confidence should YOLO be, before labeling
confidence_threshold: float = 0.25
iou_threshold: float = 0.45
track_points: str = "bbox"  # Can be centroid or bbox
label_offset: int = 50  # Offset from center point to classification label
max_distance_between_points: int = 30


# Load yolo model
model = torch.hub.load("ultralytics/yolov5", detector_path)


# Ready the stream
stream_url = get_stream(streams["file"])

# Open stream
videoStream = cv2.VideoCapture(stream_url)

# Prepare tracker
tracker = Tracker(
    distance_function=euclidean_distance,
    distance_threshold=max_distance_between_points,
)

# As long as the video stream is open, run the YOLO model on the frame, and show the output
while videoStream.isOpened():
    # time.sleep(0.2)
    ret, frame = videoStream.read()

    # Ensures no error occur, even when there is no more frames to check for
    if(ret is False):
        break

    # Detect objects inside the frame
    yolo_detections = model(frame)

    # Convert to norfair detections
    detections = yolo_detections_to_norfair_detections(
        yolo_detections, track_points=track_points)

    # Update tracker
    tracked_objects = tracker.update(detections=detections)

    # Draw detections, ids and center point/ bounding box
    if track_points == 'centroid':
        norfair.draw_points(frame, detections)
    elif track_points == 'bbox':
        norfair.draw_boxes(frame, detections)

    norfair.draw_tracked_objects(frame, tracked_objects, id_thickness=3)

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
            "x": int((xmin + xmax + label_offset) / 2),
            "y": int((ymin + ymax + label_offset) / 2),
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

    # Draw the model classifications on a gui
    cv2.imshow("REALTIME!", np.squeeze(frame))

    # Wait for Q to be pressed (then exit)
    if(cv2.waitKey(10) == 27):
        break

# Safely disposed any used resources

videoStream.release()
cv2.destroyAllWindows()
