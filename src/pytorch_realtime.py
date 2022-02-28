import torch
import numpy as np
import cv2
import sys


from util import get_stream

stream_url = get_stream("sources/highway.mp4")  # highway file stream


# Parse stream link, to do some additional filtering (see util.py)
# stream_url = get_stream("")  # DR live TV

#stream_url = get_stream("https://www.youtube.com/watch?v=HIPNVm6lNfM")

# Open video stream, using the given stream url
videoStream = cv2.VideoCapture(stream_url)


# Download or load cached pytorch model.
model = torch.hub.load("ultralytics/yolov5", "yolov5n")
model.conf = 0.55


# As long as the video stream is open, run the YOLO model on the frame, and show the output
while videoStream.isOpened():
    ret, frame = videoStream.read()

    # Ensures no error occur, even when there is no more frames to check for
    if(ret is False):
        break

    # Run the YOLO model on the frame
    result = model(frame)

    result.print()  # Additional logging
    # Draw the model classifications on a gui
    cv2.imshow("REALTIME!", np.squeeze(result.render()))

    # Wait for Q to be pressed (then exit)
    if(cv2.waitKey(10) & 0XFF == ord("q")):
        break

# Safely disposed any used resources

videoStream.release()
cv2.destroyAllWindows()
