from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets
from PIL import Image, ImageDraw
import face_recognition as fr
import numpy
import math
import cv2
import os


def store_image(request):
    image = request.FILES.get('faceImg')
    if 1024 < image.size < 20480000:
        path = default_storage.save('static/faceImg/' + image.name, ContentFile(image.read()))
        os.path.join(settings.MEDIA_ROOT, path)
        print("receive img: " + image.name + " successfully")
        face_location = get_face_location(path)
        print(face_location)

        # 调整图片大小
        if face_location:
            img = cv2.imread(path)
            print(str(img.shape[1]) + "   " + str(img.shape[0]))
            min_val = min(face_location[0][0], face_location[0][3], (img.shape[0] - face_location[0][2]),
                          (img.shape[1] - face_location[0][1]))
            img = img[(face_location[0][0] - min_val):(face_location[0][2] + min_val),
                  (face_location[0][3] - min_val):(face_location[0][1] + min_val)]
            # compress = cv2.resize(img, (250, int((250 / img.shape[1]) * img.shape[0])))
            compress = cv2.resize(img, (250, 250))
            cv2.imwrite(path, compress)
        return path
    else:
        return None


# 传入face_recognition.face_landmarks函数返回的眼部定位六坐标list,
# 返回左上角和右下角的坐标, 构成眼部矩形
def rect_eye(eye):
    """
    :param eye: location of eye like [(193, 251), (205, 242), (223, 244), (235, 258), (220, 261), (203, 259)]
    :return:
    """
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


def get_face_location(img_path):
    """
    :param img: An image (as a numpy array)
    :return: A list of tuples of found face locations in css (top, right, bottom, left) order like [(171, 409, 439, 141)]
    """
    img = fr.load_image_file(img_path)
    face_location = fr.api.face_locations(img)
    return face_location


def get_eyes_location(img):
    """
    :param img: An image (as a numpy array)
    :return: dict include eyes locations
    """
    if fr.api.face_landmarks(img):
        left_eye = fr.api.face_landmarks(img)[0]["left_eye"]
        right_eye = fr.api.face_landmarks(img)[0]["right_eye"]
        eyes_location = {"left_eye": left_eye, "right_eye": right_eye}
        return eyes_location
    else:
        return None


def eye_direction(img_path):
    """
    :param img_path: path of image with face in
    :return: directions of eyes
    """
    fr_img = fr.load_image_file(img_path)
    eyes_location = get_eyes_location(fr_img)
    if eyes_location is not None:
        left_coordinate = rect_eye(eyes_location["left_eye"])
        right_coordinate = rect_eye(eyes_location["right_eye"])

        # 画出眼睛
        img_draw = Image.open(img_path)
        ImageDraw.Draw(img_draw).polygon(eyes_location["left_eye"], outline="red")
        ImageDraw.Draw(img_draw).polygon(eyes_location["right_eye"], outline="red")
        img_draw.save("eyeDraw/out.png")
        # 画眼完毕

        img = cv2.imread(img_path)
        left_roi = img[left_coordinate["y1"]:left_coordinate["y2"], left_coordinate["x1"]:left_coordinate["x2"]]
        left_roi = cv2.cvtColor(left_roi, cv2.COLOR_BGR2GRAY)  # 灰度化
        # ret, left_roi = cv2.threshold(left_roi, 60, 255, cv2.THRESH_BINARY)  # 固定值二值化
        # left_roi = cv2.adaptiveThreshold(left_roi, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)  # 高斯自适应二值化
        left_avg = 0
        left_min = 255
        for i in range(0, left_roi.shape[0]):  # height
            for j in range(0, left_roi.shape[1]):  # width
                left_avg += left_roi[i][j]
                if left_min > left_roi[i][j]:
                    left_min = left_roi[i][j]
        left_avg = int(left_avg / (left_roi.shape[0] * left_roi.shape[1]))

        left_center_x = 0
        left_center_y = 0
        left_counter = 0
        for i in range(0, left_roi.shape[0]):  # height
            for j in range(0, left_roi.shape[1]):  # width
                if left_roi[i][j] <= ((left_avg / 3) * 2):
                    left_center_y += i
                    left_center_x += j
                    left_counter += 1
        if left_counter == 0:
            for i in range(0, left_roi.shape[0]):  # height
                for j in range(0, left_roi.shape[1]):  # width
                    if left_roi[i][j] <= left_min:
                        left_center_y += i
                        left_center_x += j
                        left_counter += 1
        left_center_x = math.ceil(left_center_x / left_counter)
        left_center_y = math.ceil(left_center_y / left_counter)
        center = {"width": left_center_x, "height": left_center_y}
        left_result = nine_grid(left_roi.shape[1], left_roi.shape[0], center)

        right_roi = img[right_coordinate["y1"]:right_coordinate["y2"], right_coordinate["x1"]:right_coordinate["x2"]]
        right_roi = cv2.cvtColor(right_roi, cv2.COLOR_BGR2GRAY)  # 灰度化
        # ret, right_roi = cv2.threshold(right_roi, 60, 255, cv2.THRESH_BINARY)  # 固定值二值化
        # right_roi = cv2.adaptiveThreshold(right_roi, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)  # 高斯自适应二值化
        right_avg = 0
        right_min = 255
        for i in range(0, right_roi.shape[0]):  # height
            for j in range(0, right_roi.shape[1]):  # width
                right_avg += right_roi[i][j]
                if right_min > right_roi[i][j]:
                    right_min = right_roi[i][j]
        right_avg = int(right_avg / (right_roi.shape[0] * right_roi.shape[1]))

        right_center_x = 0
        right_center_y = 0
        right_counter = 0
        for i in range(0, right_roi.shape[0]):  # height
            for j in range(0, right_roi.shape[1]):  # width
                if right_roi[i][j] <= ((right_avg / 3) * 2):
                    right_center_y += i
                    right_center_x += j
                    right_counter += 1
        if right_counter == 0:
            for i in range(0, right_roi.shape[0]):  # height
                for j in range(0, right_roi.shape[1]):  # width
                    if right_roi[i][j] <= right_min:
                        right_center_y += i
                        right_center_x += j
                        right_counter += 1
        right_center_x = math.ceil(right_center_x / right_counter)
        right_center_y = math.ceil(right_center_y / right_counter)
        center = {"width": right_center_x, "height": right_center_y}
        right_result = nine_grid(right_roi.shape[1], right_roi.shape[0], center)
        return [left_result, right_result]
    else:
        return None


def judge(result):
    if result == 0:
        return "左上"
    elif result == 1:
        return "上"
    elif result == 2:
        return "右上"
    elif result == 3:
        return "左"
    elif result == 4:
        return "中"
    elif result == 5:
        return "右"
    elif result == 6:
        return "左下"
    elif result == 7:
        return "下"
    else:
        return "右下"


@api_view(["POST"])
def get_eye_direction(request):
    img_path = store_image(request)
    if img_path is not None:
        result = eye_direction(img_path)
        if result is not None:
            left_result = judge(result[0])
            right_result = judge(result[1])
            return HttpResponse("left is :" + left_result + "  right is :" + right_result)
        else:
            return HttpResponse("no face detected")
    else:
        return HttpResponse("image store error")
