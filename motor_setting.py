PWMA = PWMOutputDevice(18)
AIN1 = DigitalOutputDevice(22)
AIN2 = DigitalOutputDevice(27)

PWMB = PWMOutputDevice(23)
BIN1 = DigitalOutputDevice(25)
BIN2 = DigitalOutputDevice(24)

#직진
def motor_go(speed):
  AIN1.value = 0
  AIN2.value = 1
  PWMA.value = speed
  BIN1.value = 0
  BIN2.value = 1
  PWMB.value = speed

#후진
def motor_back(speed):
  AIN1.value = 1
  AIN2.value = 0
  PWMA.value = speed
  BIN1.value = 1
  BIN2.value = 0
  PWMB.value = speed

#좌회전
def motor_left(speed):
  AIN1.value = 1
  AIN2.value = 0
  PWMA.value = 0.0
  BIN1.value = 0
  BIN2.value = 1
  PWMB.value = speed

#우회전
def motor_right(speed):
  AIN1.value = 0
  AIN2.value = 1
  PWMA.value = speed
  BIN1.value = 1
  BIN2.value = 0
  PWMB.value = 0.0

#정지
def motor_stop():
  AIN1.value = 0
  AIN2.value = 1
  PWMA.value = 0.0
  BIN1.value = 0
  BIN2.value = 1
  PWMB.value = 0.0

#속도 제어
def motor_slow(speed):
  AIN1.value = 0
  AIN2.value = 1
  PWMA.value = speed/3
  BIN1.value = 0
  BIN2.value = 1
  PWMB.value = speed/3

  speedSet = 0.6
