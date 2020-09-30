import numpy as np
import cv2
import time
import ASVD
frame_count = 0
init = 0
time_count = 1
camera = cv2.VideoCapture(0)
width = 320  #定义摄像头获取图像宽度
height = 240   #定义摄像头获取图像长度
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)  #设置宽度
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
fourcc = cv2.VideoWriter_fourcc(*'avc1')
fps = 20
# filename = '/Users/yeshiouwei/Desktop/專案/學校專題_監視系統/'+time.time()+'.mov'
out = cv2.VideoWriter('filename.mov', fourcc, fps,(width,height))
time.sleep(2)
while(camera.isOpened()):
  # ----從攝影機擷取一張影像
  # out = cv2.VideoWriter('filename.mov', fourcc, fps, (320, 240))
  frame_1 = camera.read()[1]
  frame_2 = camera.read()[1]
  frame_1 = cv2.flip(frame_1, 1)
  frame_2 = cv2.flip(frame_2, 1)
  frame_3 = frame_1.copy()
  frame_3 = ASVD.aug(frame_3)
  gray_image1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
  gray_image2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)
  Image = cv2.absdiff(gray_image1, gray_image2)
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
  Image = cv2.erode(Image, kernel)
  Image = cv2.dilate(Image, kernel)

  # ---- 查看開運算後的數值總和
  np_image = np.sum(Image)
  cv2.imshow("Image", Image)
  # print(np_image)
  if time_count == 1:
      if np_image >= 15000:
          out.write(frame_3)
      else:
          out.release()

  elif time_count < 100:
      out.write(frame_3)
      time_count += 1
  else:
      time_count = 1
  # ----FPS 計算

  if frame_count == 0:
      t_start = time.time()
      FPS = ' '
      frame_count += 1

  elif 0 < frame_count < 10:
      FPS = "FPS=%1f" % (frame_count / (time.time() - t_start))
      frame_count += 1

  else:
      FPS = "FPS=%1f" % (10 / (time.time() - t_start))
      frame_count = 0

  # ----顯示FPS
  cv2.putText(frame_1, FPS, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
  # ----顯示圖片
  cv2.imshow('frame', frame_1)

  # ----若按下 q 鍵則離開迴圈
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
# 釋放攝影機
camera.release()
out.release()
# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()