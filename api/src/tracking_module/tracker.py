import threading
from collections import namedtuple
from functools import reduce
from typing import Iterable, Mapping

import cv2
import norfair
import numpy as np
import progress.bar as Bar
import torch
from norfair import Tracker as NorfairTracker

from norfair_helpers import euclidean_distance, yolo_detections_to_norfair_detections
from util import center_pos, get_stream


class Tracker:
    """class for tracking objects via a videofeed
    """

    def __init__(self,
                 should_draw: bool = True,
                 should_save: bool = True,
                 model_path: str = "yolov5m",  # YOLO version
                 custom_model: bool = False,
                 # How confidence should YOLO be, before labeling
                 confidence_threshold: float = 0.6,
                 track_shape: str = "bbox",  # Can be centroid or bbox
                 label_offset: int = 50,  # Offset from center point to classification label
                 max_distance_between_points: int = 30):

        # Load yolo model
        if (custom_model):
            self.model = torch.hub.load(repo_or_dir='ultralytics/yolov5',
                                        model='custom',
                                        path=model_path,
                                        force_reload=False,
                                        skip_validation=True)
            # self.model = torch.load('yolov5m.pt', map_location=torch.device(
            #     f"{'cuda' if torch.cuda.is_available() else 'cpu'}"))
        else:
            # downloads model to root folder, fix somehow
            self.model = torch.hub.load(repo_or_dir="ultralytics/yolov5",
                                        model=model_path,
                                        force_reload=False,
                                        skip_validation=True)

        self.model.conf = confidence_threshold
        self.model.iou = 0.45

        self.inside_roi = []  # Int array
        self.detections = {}

        self.norfair_tracker = NorfairTracker(
            distance_function=euclidean_distance,
            distance_threshold=max_distance_between_points,
        )

        self.track_shape = track_shape
        self.label_offset = label_offset
        self.should_draw = should_draw
        self.should_save = should_save

    def track(self, content_feed: str, roi: Iterable[list[int]] = None) -> Mapping[str, int]:
        """Tracks objects in a given file within a specified regoin of interest (roi)

        Args:
            content_feed (str): path/url to video
            roi (np.ndarray[int, int], optional): region of interest, as a list og points. Defaults to None.

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """        # setup variables
        detection_map = {}
        inside_roi = []

        # Ready the stream
        stream_url = get_stream(content_feed)

        # Open stream
        video_stream = cv2.VideoCapture(stream_url)

        if(roi is None):
            video_dimension = (int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            roi = np.array(
                [[0, 0], [video_dimension[0], 0], [video_dimension[0], video_dimension[1]], [0, video_dimension[1]]])
        if(len(roi) <= 2):
            raise Exception("roi needs more than 2 points")
        roi = np.array(roi)

        # Get frame count for stream
        stream_frame_count = video_stream.get(cv2.CAP_PROP_FRAME_COUNT)

        # Open file writer
        out = cv2.VideoWriter(
            filename=content_feed + "_processed.mkv",
            fourcc=cv2.VideoWriter_fourcc(*'FMP4'),  # FFMPEG codec
            fps=video_stream.get(cv2.CAP_PROP_FPS),
            frameSize=(int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)),
                       int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        # Get first frame for masking
        if (video_stream.isOpened()):
            ref_frame = video_stream.read()[1]

        # returns (x,y,w,h) of the rect surrounding the ROI
        b_rect = cv2.boundingRect(roi)
        b_rect = [*b_rect[:2], *(x - 1 for x in b_rect[2:])]
        mask, roi_offset = create_mask(ref_frame, roi, b_rect)

        bar = Bar.IncrementalBar('Analyzing', max=stream_frame_count - 1, redirect_stdout=True,
                                 suffix='%(percent).1f%% ETA: %(eta_td)s')

        # As long as the video stream is open, run the YOLO model on the frame, and show the output
        while video_stream.isOpened():
            ret, frame = video_stream.read()

            # Ensures no error occur, even when there is no more frames to check for
            if (not ret):
                break

            # Crop frame to ROI area
            masked_image = mask_image(frame, mask, b_rect)

            try:
                # Detect objects inside the cropped frame
                # yolo_detections = self.model(frame)
                yolo_detections = self.model(masked_image)
            except Exception as e:
                print(str(e))
                break

            # Convert to norfair detections
            # detections = yolo_detections_to_norfair_detections(yolo_detections, track_points=self.track_points)
            detections = yolo_detections_to_norfair_detections(yolo_detections,
                                                               track_points=self.track_shape,
                                                               offset=roi_offset)

            # Update tracker
            tracked_objects = self.norfair_tracker.update(
                detections=detections)

            count_objects(tracked_objects, roi, detection_map, inside_roi)

            if(self.should_draw or self.should_save):
                draw(frame, roi, detections, tracked_objects,
                     self.track_shape, detection_map, inside_roi)

            # Write to filesystem
            if(self.should_save):
                out.write(frame)

            if (self.should_draw):
                # Draw the model classifications on a gui
                cv2.imshow("REALTIME! " + threading.currentThread().getName(),
                           np.squeeze(frame))

            bar.next()

            # Wait for ESC to be pressed (then exit)
            if (cv2.waitKey(1) == 27):
                break

        # Safely disposed any used resources
        video_stream.release()
        out.release()
        # cv2.destroyAllWindows()

        bar.finish()

        return detection_map


class Label:
    def __init__(self,
                 text: str,
                 bbox_location: Iterable,
                 font_face: int = cv2.FONT_HERSHEY_SIMPLEX,
                 font_scale: float = 0.5,
                 font_color: tuple[int, int, int] = (255, 255, 255),
                 font_thickness: int = 1,
                 box_color: tuple[int, int, int] = (0, 0, 255),
                 box_margin: int = 2) -> None:

        self.text = text
        self.bbox_location = bbox_location
        self.font_face = font_face
        self.font_scale = font_scale
        self.font_color = font_color
        self.font_thickness = font_thickness
        self.box_color = box_color
        self.box_margin = box_margin

    def get_text_size(self):
        return cv2.getTextSize(self.text,
                               self.font_face,
                               self.font_scale,
                               self.font_thickness)

    def get_label_location(self):
        # get size of label to draw
        text_size = self.get_text_size()

        # Define tuples
        point = namedtuple("point", ['x', 'y'])
        box = namedtuple("box", ['x_min', 'y_min', 'x_max', 'y_max'])
        text_dimension = namedtuple("text", ['width', 'height'])

        # define label location
        bbox_corner = point(*(int(val) for val in self.bbox_location))
        text_box = text_dimension(*text_size[0])
        label_container = box(bbox_corner.x,
                              bbox_corner.y - text_box.height - self.box_margin * 4,
                              bbox_corner.x + text_box.width + self.box_margin * 2,
                              bbox_corner.y)
        label_text = point(label_container.x_min + self.box_margin,
                           label_container.y_max - self.box_margin * 3)

        return label_container, label_text


def create_mask(image: np.ndarray, roi: np.ndarray, bounding_rect: list[int, int, int, int]) -> tuple[np.ndarray, tuple[int, int]]:
    """Creates mask based on image and ROI
    """
    # mask defaulting to black for 3-channel and transparent for 4-channel
    # Step-by-step guide to understand this wizadry :D
    # 1. slicing and unpacking the bounding box of the roi: [*bounding_rect[3:1:-1]]
    # # slices the tuple (eg. (x=0, y=0, w=1920, h=1080)) beginning from index 3 (height) to index 1 (y) non inclusive.
    # # traverses tuple in reverse order in steps by -1
    # # '*' unpacks the tuple, meaning, automatically replaces [*bounding_rect] with [0, 0, 1920, 1080]
    mask_shape = [*bounding_rect[3:1:-1],  image.shape[2]]
    mask = np.zeros(mask_shape, dtype=np.uint8)
    # mask = np.zeros(image.shape, dtype=np.uint8)

    # automatically find lowest offsets (for later repositioning)
    min_x = min(point[0] for point in roi)
    min_y = min(point[1] for point in roi)
    roi_offset = (min_x, min_y)
    roi_region = ([point[0] - roi_offset[0], point[1] - roi_offset[1]]
                  for point in roi)
    roi_region = np.array([*roi_region])

    # fill the ROI so it doesn't get wiped out when the mask is applied
    channel_count = image.shape[2]  # channel count on image

    # array of white color, sized to channels count
    ignore_mask_color = (255, ) * channel_count

    # draw desired area on mask
    cv2.fillConvexPoly(mask, roi_region, ignore_mask_color)
    # cv2.drawContours(mask, [roi_corners], -1, ignore_mask_color, -1, cv2.LINE_AA)

    return mask, roi_offset


def mask_image(image: np.ndarray, mask: np.ndarray, bounding_rect: tuple[int, int, int, int]) -> np.ndarray:
    """crops the given frame to fit the mask, based on ROI area
    """
    # crop frame to masked area
    cropped_image = image[bounding_rect[1]:bounding_rect[1] + bounding_rect[3],
                          bounding_rect[0]:bounding_rect[0] + bounding_rect[2]]

    # apply the mask
    masked_image = cv2.bitwise_and(cropped_image, mask)

    return masked_image


def count_objects(tracked_objects, roi, detections, inside_roi):
    """counts objects inside tracked inside the ROI
    """
    center_positions = (
        {
            obj.id:
            cv2.pointPolygonTest(
                contour=np.array(roi, np.int32),
                pt=center_pos(obj.estimate[obj.live_points]),
                measureDist=False
            )
        }
        for obj in tracked_objects if obj.live_points.any()
    )

    # Find ROI vehicles
    for obj in tracked_objects:
        if not obj.live_points.any():
            continue

        track_position = center_pos(obj.estimate[obj.live_points])
        # Is this object inside ROI?
        is_inside_roi = cv2.pointPolygonTest(
            np.array(roi, np.int32), track_position, False)

        if (is_inside_roi >= 0):
            if not obj.id in inside_roi:
                inside_roi.append(obj.id)

                if (obj.label in detections):
                    detections[obj.label] += 1
                else:
                    detections[obj.label] = 1
        else:
            if obj.id in inside_roi:
                inside_roi.remove(obj.id)
        # print(detections)


def draw(frame, roi, norfair_detections, tracked_objects, track_shape: str, detections, inside_roi):
    # Draw detected label
    frame_scale = frame.shape[0] / 100
    id_size = frame_scale / 10
    id_thickness = int(frame_scale / 3)

    # Draw detections, ids and center point/ bounding box
    if track_shape == 'centroid':
        norfair.draw_points(frame,
                            norfair_detections,
                            thickness=3,
                            draw_labels=True,
                            label_size=id_size)
    elif track_shape == 'bbox':
        norfair.draw_boxes(frame,
                           norfair_detections,
                           line_width=3,
                           draw_labels=False,
                           label_size=id_size)

    # norfair.draw_tracked_objects(
    #     frame, tracked_objects, id_thickness=2, id_size=id_size, color=[0, 255, 0])

    # Draw ROI
    cv2.polylines(frame, [np.array(roi, np.int32)], True,
                  (15, 220, 10), 6)

    for detection in norfair_detections:
        tracked_object = detection_to_tracked_linker(
            detection, tracked_objects)

        if (tracked_object != None):
            object_id = str(tracked_object.id)
        else:
            object_id = "-1"

        text = "id: {id} type: {label} ({conf})".format(
            id=object_id,
            label=detection.label,
            conf=str(round(detection.scores[0], 2)))

        label = Label(text, detection.points[0])

        draw_label(frame, label)

    # Draw vehicle counter

    total_vehicles = reduce(
        lambda a, b: a + b, detections.values()) if len(detections) > 0 else 0

    cv2.putText(
        img=frame,
        text="total: " + str(total_vehicles),
        org=(25, 100),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=id_size,
        color=[255, 255, 255],  # Dynamic?
        thickness=id_thickness,
        lineType=cv2.LINE_AA,
    )

    cv2.putText(
        img=frame,
        text="now: " + str(len(inside_roi)),
        org=(25, 150),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=id_size,
        color=[255, 255, 255],  # Dynamic?
        thickness=id_thickness,
        lineType=cv2.LINE_AA,
    )


def draw_label(frame, label: Label):

    label_container, label_text = label.get_label_location()

    cv2.rectangle(
        img=frame,
        pt1=(label_container.x_min, label_container.y_min),
        pt2=(label_container.x_max, label_container.y_max),
        color=label.box_color,
        thickness=cv2.FILLED
    )

    cv2.putText(
        img=frame,
        text=label.text,
        org=label_text,
        fontFace=label.font_face,
        fontScale=label.font_scale,
        color=label.font_color,
        thickness=label.font_thickness,
        lineType=cv2.LINE_AA,
    )


def detection_to_tracked_linker(norfair_detetion, tracked_objects):
    for object in tracked_objects:
        if (object.last_detection == norfair_detetion):
            return object
