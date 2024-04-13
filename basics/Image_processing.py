import cv2

def imageResize (img):
    height, width, chanels = img.shape
    new_height = int(height/2)
    new_width = int(width/2)
    new_image = cv2.resize(img, (new_width, new_height))
    
    return new_image

def hsvThresholding (img, lower, upper):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    return mask