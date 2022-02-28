
from charset_normalizer import detect
from util import get_stream
import argparse

import numpy as np
import torch
import yolov5
from typing import Union, List, Optional

import norfair
from norfair import Detection, Tracker, Video

import cv2
import time

max_distance_between_points: int = 30


class YOLO:
    def __init__(self, model_path: str, device: Optional[str] = None):
        if device is not None and "cuda" in device and not torch.cuda.is_available():
            raise Exception(
                "Selected device='cuda', but cuda is not available to Pytorch."
            )
        # automatically set device if its None
        elif device is None:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
        # load model
        self.model = yolov5.load(model_path, device=device)

    def __call__(
        self,
        img: Union[str, np.ndarray],
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45,
        image_size: int = 720,
        classes: Optional[List[int]] = None
    ) -> torch.tensor:

        self.model.conf = conf_threshold
        self.model.iou = iou_threshold
        if classes is not None:
            self.model.classes = classes
        detections = self.model(img, size=image_size)
        return detections


def euclidean_distance(detection, tracked_object):
    return np.linalg.norm(detection.points - tracked_object.estimate)


def yolo_detections_to_norfair_detections(
    yolo_detections: torch.tensor,
    track_points: str = 'bbox'  # bbox or centroid
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
                    [detection_as_xyxy[0].item(), detection_as_xyxy[1].item()],
                    [detection_as_xyxy[2].item(), detection_as_xyxy[3].item()]
                ]
            )
            scores = np.array([detection_as_xyxy[4].item(),
                              detection_as_xyxy[4].item()])
            norfair_detections.append(
                Detection(points=bbox, scores=scores)
            )

    return norfair_detections


parser = argparse.ArgumentParser(description="Track objects in a video.")

parser.add_argument("--detector_path", type=str,
                    default="yolov5m6.pt", help="YOLOv5 model path")
parser.add_argument("--img_size", type=int, default="720",
                    help="YOLOv5 inference size (pixels)")
parser.add_argument("--conf_thres", type=float, default="0.25",
                    help="YOLOv5 object confidence threshold")
parser.add_argument("--iou_thresh", type=float, default="0.45",
                    help="YOLOv5 IOU threshold for NMS")
parser.add_argument('--classes', nargs='+', type=int,
                    help='Filter by class: --classes 0, or --classes 0 2 3')
parser.add_argument("--device", type=str, default=None,
                    help="Inference device: 'cpu' or 'cuda'")
parser.add_argument("--track_points", type=str, default="centroid",
                    help="Track points: 'centroid' or 'bbox'")
args = parser.parse_args()

# model = YOLO(args.detector_path, device=args.device)
model = torch.hub.load("ultralytics/yolov5", "yolov5n")

# Vores kode

stream_url = get_stream("sources/highway.mp4")  # highway file stream
videoStream = cv2.VideoCapture(stream_url)


tracker = Tracker(
    distance_function=euclidean_distance,
    distance_threshold=max_distance_between_points,
)

# As long as the video stream is open, run the YOLO model on the frame, and show the output
while videoStream.isOpened():
    time.sleep(0.2)
    ret, frame = videoStream.read()

    # Ensures no error occur, even when there is no more frames to check for
    if(ret is False):
        break

    yolo_detections = model(
        frame,
        # conf_threshold=args.conf_thres,
        # iou_threshold=args.iou_thresh,
        # image_size=args.img_size,
    )

    detections = yolo_detections_to_norfair_detections(
        yolo_detections, track_points=args.track_points)

    tracked_objects = tracker.update(detections=detections)

    if args.track_points == 'centroid':
        norfair.draw_points(frame, detections)
    elif args.track_points == 'bbox':
        norfair.draw_boxes(frame, detections)

    norfair.draw_tracked_objects(frame, tracked_objects)

    # print(tracked_objects)

    # print(yolo_detections.pandas().xyxy[0])
    xyxy = yolo_detections.xyxy[0]
    pand = yolo_detections.pandas()
    pandxyxy = pand.xyxy[0]

    length = len(pand.xyxy[0].name)
    print("LENGHT: " + str(length))

    for i in range(length):
        name = pand.xyxy[0].name[i]
        xmin = pand.xyxy[0].xmin[i]
        xmax = pand.xyxy[0].xmax[i]
        ymin = pand.xyxy[0].ymin[i]
        ymax = pand.xyxy[0].ymax[i]

        pos = [xmin + xmax, ymin + ymax]

        frame_scale = frame.shape[0] / 100
        id_size = frame_scale / 10
        id_thickness = int(frame_scale / 5)

        cv2.putText(
            frame,
            name,
            (int(pos[0]/2), int(pos[1]/2)),
            cv2.FONT_HERSHEY_SIMPLEX,
            id_size,
            [26, 188, 156],
            id_thickness,
            cv2.LINE_AA,
        )

    # Draw the model classifications on a gui
    cv2.imshow("REALTIME!", np.squeeze(frame))

    # Wait for Q to be pressed (then exit)
    if(cv2.waitKey(10) & 0XFF == ord("q")):
        break

# Safely disposed any used resources

videoStream.release()
cv2.destroyAllWindows()
