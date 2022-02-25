import torch
import numpy as np
import cv2


from util import get_stream

# stream_url = get_stream("sources/highway.mp4") # highway file stream
# highway live stream
stream_url = get_stream("https://www.youtube.com/watch?v=ffsC9km5xDY")


videoStream = cv2.VideoCapture(stream_url)


model = torch.hub.load("ultralytics/yolov5", "yolov5n")

while videoStream.isOpened():
    ret, frame = videoStream.read()

    if(ret is False):
        break

    result = model(frame)
    result.print()
    cv2.imshow("REALTIME!", np.squeeze(result.render()))

    if(cv2.waitKey(10) & 0XFF == ord("q")):
        break

videoStream.release()
cv2.destroyAllWindows()
