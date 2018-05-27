from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework import viewsets
from PIL import Image, ImageDraw
import numpy
import math
import cv2


# 传入face_recognition.face_landmarks函数返回的眼部定位六坐标list,
# 返回左上角和右下角的坐标, 构成眼部矩形
def rect_eye(eye):
    width = eye[3][0] - eye[0][0]
    height = int((eye[4][1] + eye[5][1] - eye[1][1] - eye[2][1]) / 2)
    x = eye[0][0]
    y = int((eye[1][1] + eye[2][1]) / 2)
    return {"x1": x, "y1": y, "x2": x + width, "y2": y + height}


# 传入眼眶矩形的宽度和高度与眼球中心点， 返回眼球中心点在九宫的哪个位置
def nine_grid(width, height, center):
    width_trisection = int(width / 3)
    height_trisection = int(height / 3)
    print("img width is :" + str(width) + "  img height is : " + str(height))
    print("width_trisection is :" + str(width_trisection) + "  height_trisection is : " + str(height_trisection))
    print("center width is : " + str(center["width"]) + "\ncenter height is : " + str(center["height"]))

    if (center["width"] < width_trisection) & (center["height"] < height_trisection):
        return 0
    elif (center["width"] > width_trisection * 2) & (center["height"] < height_trisection):
        return 2
    elif center["height"] < height_trisection:
        return 1
    elif (center["width"] < width_trisection) & (center["height"] > height_trisection * 2):
        return 6
    elif (center["width"] > width_trisection * 2) & (center["height"] > height_trisection * 2):
        return 8
    elif center["height"] > height_trisection * 2:
        return 7
    elif center["width"] < width_trisection:
        return 3
    elif center["width"] > width_trisection * 2:
        return 5
    else:
        return 4


@api_view(["POST"])
def eye_direction(eye, img_path):
    coordinate = rect_eye(eye)
    img = cv2.imread(img_path)
    roi = img[coordinate["y1"]:coordinate["y2"], coordinate["x1"]:coordinate["x2"]]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)  # 灰度化
    # ret, roi = cv2.threshold(roi, 60, 255, cv2.THRESH_BINARY)  # 固定值二值化
    roi = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)  # 高斯自适应二值化
    center_x = 0
    center_y = 0
    counter = 0
    for i in range(0, roi.shape[1]):  # width
        for j in range(0, roi.shape[0]):  # height
            if roi[j][i] < 50:
                center_x += i
                center_y += j
                counter += 1
    center_x = math.ceil(center_x / counter)
    center_y = math.ceil(center_y / counter)
    center = {"width": center_x, "height": center_y}
    result = nine_grid(roi.shape[1], roi.shape[0], center)
    return result
