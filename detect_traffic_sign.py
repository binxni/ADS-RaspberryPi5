# 전처리한 데이터의 라벨링을 직관적으로 변경
TRAFFIC_SIGN_LABELS = {
    0: 'left',   # Index for left turn
    1: 'right',  # Index for right turn
    2: 'stop'    # Index for stop sign
}

def detect_traffic_sign(image, model):
    """
    Detect traffic signs (left, right, stop) and control motor accordingly.
    """
    global carState

    # 교통 표지판 이미지 전처리
    image_resized = cv2.resize(image, (64, 64))  #이미지 리사이
    image_normalized = image_resized / 255.0
    image_input = np.expand_dims(image_normalized, axis=0)  # 배치 차원 추가

    # 훈련된 모델을 사용하여 교통 표지판 예측
    prediction = traffic_sign_model.predict(image_input)
    predicted_label = np.argmax(prediction)  #가장 높은 확률의 레이블 인덱스 가져옴

    traffic_sign = TRAFFIC_SIGN_LABELS.get(predicted_label, None)
    confidence = np.max(prediction)  #예측 신뢰도 확인

    x, y, w, h = get_traffic_sign_bounding_box(image)  #교통 표지판의 경계 상자 좌표 파

    # 감지된 표지판의 영역 크기와 이미지 전체 영역 대비 비율 계산
    sign_area = w * h
    image_area = image.shape[0] * image.shape[1]
    occupied_ratio = sign_area / image_area

    # 표지판이 충분히 크고, 신뢰도가 70%이상일 때 표지판 인식 실
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
