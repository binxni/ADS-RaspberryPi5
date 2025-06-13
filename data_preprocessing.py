import threading
import time
import mycamera
import cv2

def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height / 2):, :, :]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.resize(image, (200, 66))
    image = cv2.GaussianBlur(image, (5,5), 0)
    image = image/255
    return image

camera = mycamera.MyPiCamera(640, 480)

_, image = camera.read()
image = cv2.flip(image, -1)
imagednn = image
image_ok = 0
image_find_ok = 0

box_size =0
carState="stop"
