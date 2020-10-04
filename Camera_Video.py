import cv2
import time
# ---- 攝影機攝取影像尺寸
_CAMERA_WIDTH = 640
_CAMERA_HEIGHT = 480

# ---- 儲存影像檔名，格式
video_name = 'Video_'
file_type = '.mov'

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH,_CAMERA_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,_CAMERA_HEIGHT)

fourcc = cv2.VideoWriter_fourcc(*'avc1')
FPS = 30

# ---- 環境變數
write_Camera = 0 #判斷寫入模式
video_counter = 0 #計算影片數量
time.sleep(2)

# ---- Haar
faceCascade = cv2.CascadeClassifier(r'/Users/yeshiouwei/opt/anaconda3/pkgs/libopencv-3.4.2-h7c891bd_1/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

def Haar(gray):
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces

while (camera.isOpened()):

    # ---- 畫面讀取
    ret, frame = camera.read()

    # ---- 畫面翻轉
    frame = cv2.flip(frame, 1)
    gray = frame.copy()

    # ---- Haar 人臉偵測 + 人臉標記
    faces = Haar(frame)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    sec = time.strftime("%S", time.localtime())
    sec = int(sec)
    if ret == True:

        if 1 <= sec < 59 and write_Camera == 0:
            write_Camera = 1
            save_name = video_name + str(video_counter) + file_type #時刻檔名
            out = cv2.VideoWriter(save_name, fourcc, FPS, (_CAMERA_WIDTH, _CAMERA_HEIGHT))
            print('writing to ' + save_name)

        elif sec == 0 and write_Camera == 1:
            write_Camera = 0
            video_counter += 1
            print('finish')

        elif cv2.waitKey(10) & 0xFF == ord('q'):
            camera.release()
            out.release()
            cv2.destroyAllWindows()
            break

        if (write_Camera == 1):
            out.write(frame)

        cv2.imshow('frame', frame)
    else:
        break
