import threading
import time
import mycamera
import cv2
import numpy as np
import tensorflow as tf
from keras.metrics import MeanSquaredError
from tensorflow.keras.models import load_model
from gpiozero import DigitalOutputDevice, PWMOutputDevice

# 전처리한 데이터의 라벨링을 직관적으로 변경
TRAFFIC_SIGN_LABELS = {
    0: 'left',   # Index for left turn
    1: 'right',  # Index for right turn
    2: 'stop'    # Index for stop sign
}
def traffic_cnn(input_shape=(64, 64, 3), num_classes=3):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))
    return model
	
def detect_traffic_sign(image, model):
    global carState

    # 이미지 전처리
    image_resized = cv2.resize(image, (64, 64))
    image_normalized = image_resized / 255.0
    image_input = np.expand_dims(image_normalized, axis=0)

    # 예측
    prediction = model.predict(image_input)
    predicted_label = np.argmax(prediction)
    confidence = np.max(prediction)
    traffic_sign = TRAFFIC_SIGN_LABELS.get(predicted_label, None)

    # 더미 경계 상자 (향후 실제 탐지 로직으로 대체 가능)
    x, y, w, h = get_traffic_sign_bounding_box(image)
    sign_area = w * h
    image_area = image.shape[0] * image.shape[1]
    occupied_ratio = sign_area / image_area

    # 조건 만족 시 모터 제어
    if occupied_ratio > 0.7 and confidence > 0.7:
        if traffic_sign == 'left':
            print("Detected: Left Turn")
            carState = "go"
            motor_left(speedSet)

        elif traffic_sign == 'right':
            print("Detected: Right Turn")
            carState = "go"
            motor_right(speedSet)

        elif traffic_sign == 'stop':
            print("Detected: Stop Sign")
            carState = "stop"
            motor_stop()
    else:
        print("No relevant traffic sign detected.")
	    
def get_traffic_sign_bounding_box(image):
  """
  Dummy function to return bounding box coordinates for the traffic sign.
  Replace with actual detection logic (e.g., using a pre-trained model or a simple classifier).
  """
  # Example: Assuming the traffic sign is detected with some bounding box (x, y, w, h)
  # Replace with your actual detection code (e.g., OpenCV DNN, Haar cascades, etc.)
  return (50, 50, 100, 100)  # (x, y, width, height)
