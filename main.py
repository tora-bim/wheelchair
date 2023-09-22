import RPi.GPIO as GPIO
import cv2

# GPIOピンの設定
left_motor_pin = 17  # 左モーターのGPIOピン番号
right_motor_pin = 18  # 右モーターのGPIOピン番号

# GPIOの初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_motor_pin, GPIO.OUT)
GPIO.setup(right_motor_pin, GPIO.OUT)

# モーターを停止する関数
def stop_motors():
    GPIO.output(left_motor_pin, GPIO.LOW)
    GPIO.output(right_motor_pin, GPIO.LOW)

# ロボットを左に動かす関数
def move_left():
    GPIO.output(left_motor_pin, GPIO.LOW)
    GPIO.output(right_motor_pin, GPIO.HIGH)

# ロボットを右に動かす関数
def move_right():
    GPIO.output(left_motor_pin, GPIO.HIGH)
    GPIO.output(right_motor_pin, GPIO.LOW)

# カメラの初期化
cap = cv2.VideoCapture(0)

# Haar Cascade分類器を使用して顔を検出
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

try:
    while True:
        # フレームを取得
        ret, frame = cap.read()

        # グレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔を検出
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # 顔の中心座標を計算
            face_center_x = x + w // 2

            # 画面中央の座標を取得
            screen_center_x = frame.shape[1] // 2

            # 顔が画面中央よりも左にある場合、左にロボットを動かす
            if face_center_x < screen_center_x:
                move_left()
            # 顔が画面中央よりも右にある場合、右にロボットを動かす
            elif face_center_x > screen_center_x:
                move_right()
            else:
                stop_motors()

        # フレームを表示
        cv2.imshow('Frame', frame)

        # 'q'キーを押して終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Ctrl+Cなどでプログラムを終了したときにモーターを停止し、GPIOを解放
    stop_motors()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
