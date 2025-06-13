import threading
import time
import mycamera
import cv2
import numpy as np
import tensorflow as tf
from keras.metrics import MeanSquaredError
from tensorflow.keras.models import load_model
from gpiozero import DigitalOutputDevice, PWMOutputDevice

# 사전학습된 사물인식 모델이 감지할 수 있는 클래스 정의 -> 사람만 인식할 예정
classNames = {
    0: 'background', 1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle',
    5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck', 9: 'boat',
    10: 'traffic light', 11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter',
    15: 'bench', 16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep',
    21: 'cow', 22: 'elephant', 23: 'bear', 24: 'zebra', 25: 'giraffe',
    27: 'backpack', 28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase',
    34: 'frisbee', 35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite',
    39: 'baseball bat', 40: 'baseball glove', 41: 'skateboard', 42: 'surfboard',
    43: 'tennis racket', 44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork',
    49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple',
    54: 'sandwich', 55: 'orange', 56: 'broccoli', 57: 'carrot', 58: 'hot dog',
    59: 'pizza', 60: 'donut', 61: 'cake', 62: 'chair', 63: 'couch',
    64: 'potted plant', 65: 'bed', 67: 'dining table', 70: 'toilet', 72: 'tv',
    73: 'laptop', 74: 'mouse', 75: 'remote', 76: 'keyboard', 77: 'cell phone',
    78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink', 82: 'refrigerator',
    84: 'book', 85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear',
    89: 'hair drier', 90: 'toothbrush'
}

def opencvdnn_thread():
    global image, imagednn, image_ok, image_find_ok
    global box_size
    global carState
    global person_detected
    # 기존에 OpenCV에서 제공하는 사물인식 모듈을 다운받아 사용함
    model = cv2.dnn.readNetFromTensorflow("/home/pi/AI_CAR/OpencvDnn/models/frozen_inference_graph.pb", "/home/pi/AI_CAR/OpencvDnn/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt")

    while True:
      if image_ok == 1:
        imagednn = image

        image_height, image_width, _ = imagednn.shape

        model.setInput(cv2.dnn.blobFromImage(imagednn, size=(250, 250), swapRB=True))
        output = model.forward()

        # 사람인식 플래그 일단 False 세팅
        person_detected = False

        for detection in output[0, 0, :, :]:
            confidence = detection[2]
            if confidence > 0.5:
                class_id = int(detection[1])
                class_name = id_class_name(class_id, classNames)
                # 90개의 사물 중 사람만 인식하도록 세팅
                if class_name is "person":
                    print(str(str(class_id) + " " + str(detection[2]) + " " + class_name))
                    box_x = detection[3] * image_width
                    box_y = detection[4] * image_height
                    box_width = detection[5] * image_width
                    box_height = detection[6] * image_height
                    box_size = box_width * box_height
                    print("box_size:", box_size)

                    carState = "stop"
                    print("auto stop")

                    # 사람인식 플래그 True 변화
                    person_detected = True

                    cv2.rectangle(imagednn, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
                    cv2.putText(imagednn, class_name, (int(box_x), int(box_y+.05*image_height)), cv2.FONT_HERSHEY_SIMPLEX,(.005*image_width), (0, 0, 255))

        # 사람을 감지한 후, 더이상 사람을 감지하지 않는다면 5초뒤 다시 움직이도록 세팅
        if not person_detected:
            if carState == "stop":
                print("No person detected, resuming after 5 seconds.")
                time.sleep(5)
                carState = "go"

        image_find_ok = 1
