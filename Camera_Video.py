import cv2
import time
import os
import shutil
# ---- 攝影機攝取影像尺寸
_CAMERA_WIDTH = 640
_CAMERA_HEIGHT = 480

# ---- 時間


# ---- 儲存影像檔名，格式
file_type = '.mov'

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH,_CAMERA_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,_CAMERA_HEIGHT)

fourcc = cv2.VideoWriter_fourcc(*'avc1')#
FPS = 30


# ---- 環境變數
clear_file = 0 #判斷清除檔案
write_Camera = 0 #判斷寫入模式
write_File = 0 #判斷寫入資料夾
video_counter = 0 #計算影片數量
write_Haar = 0 #判斷偵測人臉
time.sleep(2)

Time = time.localtime()
Min, hour= Time[4], Time[3]

# ---- Haar
faceCascade = cv2.CascadeClassifier(r'/Users/yeshiouwei/opt/anaconda3/pkgs/libopencv-3.4.2-h7c891bd_1/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
def Time():
    Time = time.localtime()
    sec, min, hour, day = Time[5], Time[4], Time[3], Time[2]
    return sec,min,hour,day
def File(hour):
    myder = 'Video'
    if os.path.exists(myder):
        print("已經存在 %s" % myder)
    else:
        os.mkdir(myder)

    myder = 'Video/Hour_' + str(hour) + '/'
    Path = os.getcwd()
    print(Path)
    if os.path.exists(myder):
        print("已經存在 %s" % myder)
    else:
        os.mkdir(myder)
        print("建立%s 資料夾建立成功" % myder)
    address_name = Path + '/' + myder
    return address_name

def Haar(gray):
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces
# ---- 初始時間
sec,min,hour,Day =Time()
# ---- 初始資料夾建立
address_name = File(hour)
Min = min
Hour = hour

while (camera.isOpened()):

    # ---- 畫面讀取
    ret, frame = camera.read()

    if ret == True:

    # ---- 畫面翻轉
        frame = cv2.flip(frame, 1)
        gray = frame.copy()

    # ---- Haar 人臉偵測 + 人臉標記
        faces = Haar(gray)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # ---- 時間
        sec,min,hour,day = Time()


    # ---- 時鐘：管理檔案刪除
        if Hour <= hour:
            clear_file = 0
        else:
            clear_file = 1
        Hour = hour

        if clear_file == 1:
            shutil.rmtree('Video')
            os.mkdir('Video')

    # ---- 分鐘：更改儲存位置
        if Min <= min:
            write_File = 0
            # print("不用修改資料夾")
        else:
            write_File = 1
        Min = min

        if write_File == 1:
            Path = os.getcwd()
            myder = 'Video/Hour_'+str(hour)+'/'
            if os.path.exists(myder):
                print("已經存在 %s" % myder)
            else:
                os.mkdir(myder)
                print("建立%s 資料夾建立成功" % myder)
            address_name = Path +'/Video/Hour_'+str(hour)+'/'

    # ---- 秒鐘：管理錄製檔案
        if 1 <= sec < 59 and write_Camera == 0:
            write_Camera = 1
            save_name = address_name + str(min)+ '分' + file_type #時刻檔名
            out = cv2.VideoWriter(save_name, fourcc, FPS, (_CAMERA_WIDTH, _CAMERA_HEIGHT))
            print('writing to ' + save_name)

        elif sec == 0 and write_Camera == 1:
            write_Camera = 0
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
