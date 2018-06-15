import FaceRecognition as fr
import cv2
from PIL import Image, ImageDraw
import eyeball_direction_detecting as eyeball_direction

# Create your tests here.

# 图片路径
img = "/root/img/dwj5.jpg"

# 眼部定位
left_eye = [(309, 473), (333, 455), (367, 458), (395, 485), (363, 491), (330, 489)]
right_eye = [(528, 484), (556, 456), (592, 453), (621, 471), (596, 488), (560, 489)]

# 定位结果
direction_result = 4


# 眼部定位测试驱动模块
def eye_location_test(image):
    img = fr.load_image_file(image)
    eyeball_direction.get_eyes_location(img)
    print(left_eye)
    print(right_eye)
    img_draw = Image.open(image)
    ImageDraw.Draw(img_draw).polygon(left_eye, outline="red")
    ImageDraw.Draw(img_draw).polygon(right_eye, outline="red")
    img_draw.save("out.png")


# 眼球方向识别测试驱动模块
def eyeball_direction_test(img):
    left_coordinate = eyeball_direction.rect_eye(left_eye)
    right_coordinate = eyeball_direction.rect_eye(right_eye)

    img = cv2.imread(img)

    left_eyeball = eyeball_direction.get_eyeball_location(img, left_coordinate)
    left_percent = left_eyeball["percent"]
    left_result = left_eyeball["nine_grid_result"]

    right_eyeball = eyeball_direction.get_eyeball_location(img, right_coordinate)
    right_percent = right_eyeball["percent"]
    right_result = right_eyeball["nine_grid_result"]
    print(left_result, left_percent, right_result, right_percent)
    print("方向: " + str(eyeball_direction.result_direction(
        eyeball_direction.judge_direction(left_result, left_percent, right_result, right_percent))))


if __name__ == "__main__":
    print("眼部定位测试驱动模块:")
    eye_location_test(img)

    print("\n眼球方向识别测试驱动模块:")
    eyeball_direction_test(img)
