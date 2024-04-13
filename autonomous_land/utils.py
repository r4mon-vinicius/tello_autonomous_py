from djitellopy import Tello
from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("tello_2.pt")
classNames = ["movel", "takeoff"]

def initializeTello():
    tello = Tello()
    tello.connect()
    print(f"Battery: {tello.get_battery()}%")
    tello.streamon()

    return tello

def getFrameTello(tello, size):
    frame = tello.get_frame_read().frame
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = cv2.resize(frame, size)

    return frame

def baseDetect(frame):

    results = model(frame, conf = 0.8)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            cls = int(box.cls[0])
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)

    if len(boxes) != 0:
        return frame, x1, y1, x2, y2, len(boxes)
    else:
        return frame, 0, 0, 0, 0, len(boxes)



