from collections import namedtuple

import numpy as np
import torch
from norfair import Detection


def euclidean_distance(detection: Detection, tracked_object: Detection):
    """calculates the distance between new detections and already tracked objects
    """
    return np.linalg.norm(detection.points - tracked_object.estimate)


def yolo_detections_to_norfair_detections(
    yolo_detections: torch.TensorType,
    track_points: str = 'bbox',  # bbox or centroid
    offset: tuple[int, int] = (0, 0)
) -> list[Detection]:
    """convert detections_as_xywh to norfair detections
    """
    norfair_detections: list[Detection] = []

    point = namedtuple('Point', ['x', 'y'])
    offset = point(*offset)

    if track_points == 'centroid':
        # defines namedtuple to hold relevant values from detection objects xyxy
        detection = namedtuple(
            'detection', ['x', 'y', 'score', 'type'])

        detection_list_xywh = yolo_detections.xywh[0]
        for detection_xywh in detection_list_xywh:
            # create new detection with values from xyxy detection
            object = detection(
                *(tensor.item() for tensor in detection_xywh[:2]),
                *(tensor.item() for tensor in detection_xywh[4:6]))

            # find objects type name, based on type value
            name = yolo_detections.names[int(object.type)]

            centroid = np.array(
                [
                    object.x + offset.x,
                    object.y + offset.y
                ]
            )

            scores = np.array([object.score])

            norfair_detections.append(
                Detection(points=centroid, scores=scores, label=name)
            )
    elif track_points == 'bbox':
        # defines namedtuple to hold relevant values from detection objects xyxy
        detection = namedtuple(
            'detection', ['x_min', 'y_min', 'x_max', 'y_max', 'score', 'type'])

        # convert yolo detections to xyxy format
        detection_list_xyxy = yolo_detections.xyxy[0]
        for detection_xyxy in detection_list_xyxy:
            # create new detection with values from xyxy detection
            object = detection(
                *(tensor.item() for tensor in detection_xyxy[:6]))

            # find objects type name, based on type value
            name = yolo_detections.names[int(object.type)]

            # define bounding box for detected object, based on detection coordinates with given offset
            bbox = np.array(
                [
                    [object.x_min + offset.x, object.y_min + offset.y],
                    [object.x_max + offset.x, object.y_max + offset.y]
                ]
            )

            scores = np.array([object.score, object.score])

            norfair_detections.append(
                Detection(points=bbox, scores=scores, label=name))

    return norfair_detections
