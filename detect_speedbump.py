def detect_speedbump(image):
    # 이미지 하단 크롭 -> 과속방지턱은 밑에 있기 때문
    height, _ , _= image.shape
    crop_img = image[int(height/2):, :, :]
    h,_,_ = crop_img.shape
    img = crop_img[:int(h/2),:,:]

    # 노란색 검출을 위해 HSV 색상 공간으로 변환
    img_hsv =cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_lower = np.array([20, 100, 100])  # 노란색 하한
    yellow_upper = np.array([30, 255, 255])  # 노란색 상한

    # 모폴로지 연산을 위한 커널
    kernel = np.ones((5,5), np.uint8)

    # 노란색 마스크 성
    yellow_mask = cv2.inRange(img_hsv, yellow_lower, yellow_upper)
    yellow_pixel_count = cv2.countNonZero(yellow_mask)
    total_pixel_count = img.shape[0] * img.shape[1]

    # 노란색 픽셀 개수 세서 일정 기준 넘으면 과속방지턱 판단
    if yellow_pixel_count > 100:
        motor_slow(speedSet)
        time.sleep(2)
