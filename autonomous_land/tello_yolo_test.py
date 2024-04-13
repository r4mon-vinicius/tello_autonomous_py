from ultralytics import YOLO
import cv2
from djitellopy import Tello
import time
import random


def random_moves():
    
    lr = random.randint(-40, 40)
    fb = random.randint(-40, 40)
    ud = random.randint(0, 20)
    yaw = random.randint(-40, 40)

    return [lr, fb, ud, yaw]


speed = 30
tello = Tello()
tello.connect()
print(f"Bateria: {tello.get_battery} %")
tello.streamon()
tello.takeoff()
tello.send_rc_control(0, 0, 0, 0)

model = YOLO("weights/tello_2.pt")
classNames = ["movel", "takeoff"]

num_frames = 0
start_time = time.time()
fps = 0
font = cv2.FONT_HERSHEY_SIMPLEX

count = 0
values = []
while count <= 5:
    values = random_moves()
    tello.send_rc_control(values[0], values[1], values[2], values[3])
    print(f"COUNT: {count}")
    count += 1
    
    time.sleep(1.5)

while True: 
    tello.send_rc_control(0, 0, 0, speed)
    frame = tello.get_frame_read().frame
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = cv2.resize(frame, (544, 306))
    results = model(frame, conf=0.80)

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
        
    if len(boxes) >= 1:
        speed = 0
        print("PAREI DE GIRAR")
        
    num_frames += 1
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1:
        fps = num_frames // elapsed_time
        num_frames = 0
        start_time = time.time()

    cv2.putText(frame, f"FPS: {fps}", (30, 30), font, 1, (0, 255, 0), 2)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) == ord('q'):
        break

tello.land()
tello.streamoff()
cv2.destroyAllWindows()