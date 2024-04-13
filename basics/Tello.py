from djitellopy import Tello
from Image_processing import imageResize
from Image_processing import hsvThresholding
import numpy as np
import cv2

tello = Tello()

tello.connect()
tello.streamon()

lower = np.array([27,20,135])
upper = np.array([115,179,213])

while True:
    image = tello.get_frame_read().frame
    image = imageResize(image)
    img = hsvThresholding(image, lower, upper)

    cv2.imshow("Tello", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.streamoff()
cv2.destroyAllWindows()
