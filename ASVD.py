import numpy as np
import cv2

def compute(img, min_percentile, max_percentile):
  # ----np.percentile:計算一個多維數組的小排到大的百分比分位數
  max_percentile_pixel = np.percentile(img, max_percentile)#尋找圖像中最“高”的像素 (99%)
  min_percentile_pixel = np.percentile(img, min_percentile)#尋找圖像中最“低”的像素 (1%)

  return max_percentile_pixel, min_percentile_pixel

def aug(src):
  if get_lightness(src) > 130:
    print("亮度足夠，不需增強")

  max_percentile_pixel, min_percentile_pixel = compute(src, 1, 99)
  # ----修改過曝或是過暗的像素
  src[src >= max_percentile_pixel] = max_percentile_pixel#src矩陣中大於max_percentile_pixel 都變成max_percentile_pixel
  # print(type(src[src >= max_percentile_pixel]),
  #       type(src),
  #       type(max_percentile_pixel))
  src[src <= min_percentile_pixel] = min_percentile_pixel#src矩陣中小於min_percentile_pixel 都變成min_percentile_pixel
  # ----建一個跟src同大小,數據類型的零矩陣
  out = np.zeros(src.shape, src.dtype)
  # ----陣列的數值被平移或縮放到一個指定的範圍，線性歸一化。
  cv2.normalize(src, out, 255 * 0.1, 255 * 0.9, cv2.NORM_MINMAX)

  return out

def get_lightness(src):

  hsv_image = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
  # HSV:RGB色彩模型中的點在圓柱坐標系中的表示法
  # 色相（H）是色彩的基本屬性，就是平常所說的顏色名稱，如紅色、黃色等。
  # 飽和度（S）是指色彩的純度，越高色彩越純，低則逐漸變灰，取0-100%的數值。
  # 明度（V）
  # ----.mean()求平均值，hsv_image[::2].mean() 求明度平均值
  lightness = hsv_image[: : 2].mean()

  return lightness

# src = cv2.imread(r'/Users/yeshiouwei/Desktop/照片/學術/Lenna_Opencv.jpg')
# img = aug(src)
# cv2.imshow('TEST',img)
# https://blog.csdn.net/weixin_44517301/article/details/102710979