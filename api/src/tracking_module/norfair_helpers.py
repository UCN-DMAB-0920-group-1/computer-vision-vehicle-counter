import numpy as np
import torch
from typing import List
from norfair import Detection


def euclidean_distance(detection, tracked_object):
    return np.linalg.norm(detection.points - tracked_object.estimate)


def yolo_detections_to_norfair_detections(
    yolo_detections: torch.tensor,
    track_points: str = 'bbox',  # bbox or centroid
    offset: tuple[int,int] = (0,0)
) -> List[Detection]:
    """convert detections_as_xywh to norfair detections
    """
    norfair_detections: List[Detection] = []

    if track_points == 'centroid':
        detections_as_xywh = yolo_detections.xywh[0]
        for detection_as_xywh in detections_as_xywh:
            centroid = np.array(
                [
                    detection_as_xywh[0].item(),
                    detection_as_xywh[1].item()
                ]
            )
            scores = np.array([detection_as_xywh[4].item()])
            norfair_detections.append(
                Detection(points=centroid, scores=scores)
            )
    elif track_points == 'bbox':
        detections_as_xyxy = yolo_detections.xyxy[0]
        for detection_as_xyxy in detections_as_xyxy:
            bbox = np.array(
                [
                    [detection_as_xyxy[0].item() + offset[0], detection_as_xyxy[1].item() + offset[1]],
                    [detection_as_xyxy[2].item() + offset[0], detection_as_xyxy[3].item() + offset[1]]
                ]
            )
            scores = np.array([detection_as_xyxy[4].item(),
                              detection_as_xyxy[4].item()])
            norfair_detections.append(
                Detection(points=bbox, scores=scores)
            )

    return norfair_detections
