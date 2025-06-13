import threading
import time
import mycamera
import cv2
import numpy as np
import tensorflow as tf
from keras.metrics import MeanSquaredError
from tensorflow.keras.models import load_model
from gpiozero import DigitalOutputDevice, PWMOutputDevice
from detect_speedbump import detect_speedbump
from detect_traffic_sign import detect_traffic_sign

def main():
    global image, imagednn, image_ok, image_find_ok
    global carState

    # 학습한 차선인식 모델 로드
    model_path = "/home/pi/AI_CAR/model/lane_navigation_final.h5"
    model = load_model(model_path, custom_objects={'mse': MeanSquaredError()})

    # 학습한 교통표지판 감지 모델 로드
    traffic_sign_model_path = "/home/pi/AI_CAR/model/traffic_sign_model.h5"
    traffic_sign_model = load_model(traffic_sign_model_path)

    try:
      while True:
        keValue = cv2.waitKey(1)

        if keValue == ord('q'):
          break
        # 위쪽 화살표 누르면 시작
        elif keValue == 82:
          print("go")
          carState = "go"
        # 아래쪽 화살표 누르면 시작
        elif keValue == 84:
          print("stop")
          carState = "stop"

        # 카메라 이미지 초기화
        image_ok = 0

        _, image = camera.read()
        image = cv2.flip(image, -1)
        image_ok = 1

        # 과속방지턱 감지 함수
        detect_speedbump(image)

        # 교통 표지판 감지 함수
        detect_traffic_sign(image, traffic_sign_model)

        preprocessed = img_preprocess(image)
        cv2.imshow('pre', preprocessed)

        # 원본 이미지 창을 띄워서 상황 파악
        cv2.imshow("imagednn", imagednn)

        X = np.asarray([preprocessed])

        # 차선 추적 모델을 사용하여 조향각 예측
        steering_angle = int(model.predict(X)[0][0])
        print("predict angle:", steering_angle)

        # 일정 조향각 넘어가면 좌/우회전 실행
        if carState == "go":
            if steering_angle >=85 and steering_angle <= 109:
                print("go")
                motor_go(speedSet)
            elif steering_angle > 110:
                print("right")
                motor_right(speedSet)
            elif steering_angle < 84:
                print("left")
                motor_left(speedSet)
        elif carState == "stop":
            motor_stop()

    except KeyboardInterrupt:
        pass

if __name__=='__main__':
    task1 = threading.Thread(target=opencvdnn_thread)
    task1.start()
    main()
    cv2.destroyAllWindows()
