
import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2

model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # Change to 5x6!
img = "https://c8.alamy.com/comp/GM42DP/melbournes-traffic-jam-on-m1-freeway-in-melbourne-australia-GM42DP.jpg"

results = model(img)
results.print()
results.show()
