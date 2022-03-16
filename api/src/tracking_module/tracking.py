import imp
import cv2
import torch
import norfair
import numpy as np

from norfair import Tracker

from .util import get_stream, center_pos
from .norfair_helpers import euclidean_distance, yolo_detections_to_norfair_detections


class Tracking:
    """class for tracking objects via a videofeed
    """

    def __init__(
        self,
        should_draw: bool = True,
        device: str = "cuda",  # Device (CPU or GPU)
        model_path: str = "yolov5m",  # YOLO version
        custom_model: bool = False,
        # How confidence should YOLO be, before labeling
        confidence_threshold: float = 0.6,
        track_points: str = "bbox",  # Can be centroid or bbox
        label_offset: int = 50,  # Offset from center point to classification label
        max_distance_between_points: int = 30,
        # TOP LEFT, BOTTOM LEFT, BOTTOM RIGHT, TOP RIGHT,
        roi_area: np.ndarray[int, int] = [
            [(0, 250), (520, 90), (640, 90), (640, 719), (0, 719)]]
    ):

        # Load yolo model
        if(custom_model):
            self.model = torch.hub.load(
                repo_or_dir='ultralytics/yolov5',
                model='custom',
                path=model_path)
        else:
            self.model = torch.hub.load(  # downloads model to root folder, fix somehow
                repo_or_dir="ultralytics/yolov5",
                model=model_path)

        self.model.conf = confidence_threshold
        self.model.iou

        self.inside_roi = []  # Int array
        self.vehicle_count = 0

        self.tracker = Tracker(
            distance_function=euclidean_distance,
            distance_threshold=max_distance_between_points,
        )

        self.track_points = track_points
        self.label_offset = label_offset
        self.roi_area = np.array(roi_area, dtype=np.int32)
        self.should_draw = should_draw

    def draw(self, frame, yolo_detections, norfair_detections, tracked_objects):
        frame_scale = frame.shape[0] / 100
        id_size = frame_scale / 10
        id_thickness = int(frame_scale / 5)

        # Draw detected label
        frame_scale = frame.shape[0] / 100
        id_size = frame_scale / 10
        id_thickness = int(frame_scale / 5)
        pand = yolo_detections.pandas().xyxy[0]
        length = len(pand.name)

        # Draw detections, ids and center point/ bounding box
        if self.track_points == 'centroid':
            norfair.draw_points(frame, norfair_detections,
                                thickness=3, draw_labels=True, label_size=id_size)
        elif self.track_points == 'bbox':
            norfair.draw_boxes(frame, norfair_detections,
                               line_width=3, draw_labels=True, label_size=id_size)

        norfair.draw_tracked_objects(
            frame, tracked_objects, id_thickness=2, id_size=id_size, color=[0, 255, 0])

        # Draw ROI
        cv2.polylines(frame, [np.array(self.roi_area, np.int32)], True,
                      (15, 220, 10), 6)

        """
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
                img=frame,
                text=name,
                org=(pos["x"], pos["y"]),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=id_size,
                color=[26, 188, 156],  # Dynamic?
                thickness=id_thickness,
                lineType=cv2.LINE_AA,
            )
        """

        # Draw vehicle counter
        cv2.putText(
            img=frame,
            text="total: " + str(self.vehicle_count),
            org=(25, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=id_size,
            color=[231, 76, 60],  # Dynamic?
            thickness=id_thickness,
            lineType=cv2.LINE_AA,
        )

        cv2.putText(
            img=frame,
            text="now: " + str(len(self.inside_roi)),
            org=(25, 100),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=id_size,
            color=[231, 76, 60],  # Dynamic?
            thickness=id_thickness,
            lineType=cv2.LINE_AA,
        )

        # Draw the model classifications on a gui
        cv2.imshow("REALTIME!", np.squeeze(frame))

    def track(self, stream_location):

        # Ready the stream
        stream_url = get_stream(stream_location)

        # Open stream
        video_stream = cv2.VideoCapture(stream_url)

        # Open file writer
        out = cv2.VideoWriter(
            filename=stream_location + "_processed.mkv",
            # fourcc=int(video_stream.get(cv2.CAP_PROP_FOURCC)), # original codec from video
            fourcc=cv2.VideoWriter_fourcc(*'FMP4'),  # FFMPEG codec
            fps=video_stream.get(cv2.CAP_PROP_FPS),
            frameSize=(
                int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
            ))

        # Get first frame for masking
        if(video_stream.isOpened()):
            ref_frame = video_stream.read()[1]
        mask, roi_offset = self.mask_create(ref_frame)

        # As long as the video stream is open, run the YOLO model on the frame, and show the output
        while video_stream.isOpened():
            ret, frame = video_stream.read()

            # Ensures no error occur, even when there is no more frames to check for
            if(not ret):
                break

            # Crop frame to ROI area
            cropped_image = self.crop_frame(frame, mask)

            # Detect objects inside the cropped frame
            # yolo_detections = self.model(frame)
            yolo_detections = self.model(cropped_image)

            # Convert to norfair detections
            # detections = yolo_detections_to_norfair_detections(yolo_detections, track_points=self.track_points)
            detections = yolo_detections_to_norfair_detections(
                yolo_detections, track_points=self.track_points, offset=roi_offset)

            # Update tracker
            tracked_objects = self.tracker.update(detections=detections)

            self.count_objects(tracked_objects)

            if(self.should_draw):
                self.draw(frame, yolo_detections, detections, tracked_objects)
                # self.draw(cropped_image, yolo_detections, detections, tracked_objects)

            # Write to filesystem
            out.write(frame)

            # Wait for ESC to be pressed (then exit)
            if (cv2.waitKey(1) == 27):
                break
        # Safely disposed any used resources
        video_stream.release()
        out.release()
        # cv2.destroyAllWindows()

        return {"total": self.vehicle_count}

    def count_objects(self, tracked_objects):
        """counts objects inside tracked inside the ROI
        """
        # Find ROI vehicles
        for obj in tracked_objects:
            if not obj.live_points.any():
                continue

            track_position = center_pos(obj.estimate[obj.live_points])
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

    def mask_create(self, image: np.ndarray):
        """Creates mask based on image and ROI
        """
        # mask defaulting to black for 3-channel and transparent for 4-channel
        # (of course replace corners with yours)
        mask = np.zeros(image.shape, dtype=np.uint8)

        # automatically find lowest offsets
        min_x = min(p[0] for p in self.roi_area)[0]
        min_y = min(p[1] for p in self.roi_area)[1]
        roi_offset = (min_x, min_y)

        # fill the ROI so it doesn't get wiped out when the mask is applied
        channel_count = image.shape[2]  # channel count on image

        # array of white color, sized to channels count
        ignore_mask_color = (255,)*channel_count

        # draw desired area on mask
        cv2.fillConvexPoly(mask, self.roi_area, ignore_mask_color)
        # cv2.drawContours(mask, [roi_corners], -1, ignore_mask_color, -1, cv2.LINE_AA)

        return mask, roi_offset

    def crop_frame(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """crops the gives frame to fit the mask, based on ROI area
        """
        # apply the mask
        masked_image = cv2.bitwise_and(frame, mask)

        # crop frame to masked area
        # returns (x,y,w,h) of the rect
        b_rect = cv2.boundingRect(self.roi_area)
        cropped_image = masked_image[b_rect[1]: b_rect[1] + b_rect[3],
                                     b_rect[0]: b_rect[0] + b_rect[2]]

        return cropped_image
