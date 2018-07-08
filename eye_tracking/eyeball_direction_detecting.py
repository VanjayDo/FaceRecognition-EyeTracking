from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import face_recognition as fr
import cv2
import os


def CV2FR(img_array):
    """
    OpenCV读取的图片转为face_recognition库所能读取的图片
    :param img_array: OpenCV将图片转化成的数组
    :return: face_recognition库中的图片数组
    """
    return cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)


def store_image(request):
    """
    提取请求中的图片, url参数名为face_image
    :param request: 携带图片的请求
    :return: 返回提取图片后保存的路径
    """
    max_image_size = 20971520  # 所接收的图片最大尺寸, 单位为字节, 此处设置为20M
    image = request.FILES.get('face_image')
    if image.size < max_image_size:
        path = default_storage.save('static/images/' + image.name, ContentFile(image.read()))
        os.path.join(settings.MEDIA_ROOT, path)
        print("receive image: " + image.name + " successfully")
        # compress_file = Image.open(path)
        # compress_file.save(path, quality=70)
        img = cv2.imread(path)
        if img.shape[1] > 500:
            img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
        fr_img = CV2FR(img)
        face_location = get_face_location(fr_img)
        # 调整图片大小
        if face_location:
            # min_val为脸部框四周距离图片边框的最小值
            min_val = min(face_location[0][0], face_location[0][3], (img.shape[0] - face_location[0][2]),
                          (img.shape[1] - face_location[0][1]))
            img = img[(face_location[0][0] - min_val):(face_location[0][2] + min_val),
                  (face_location[0][3] - min_val):(face_location[0][1] + min_val)]
            resize = cv2.resize(img, (250, 250))  # 调整图片分辨率为250*250
            return resize
        else:
            return "no face"
    else:
        print("store image error")
        return None


def get_face_location(fr_img):
    """
    :param fr_img: face_recognition库可直接使用的图像数组
    :return: A list of tuples of found face locations in css (top, right, bottom, left) order like [(171, 409, 439, 141)]
    """
    face_location = fr.api.face_locations(fr_img)
    return face_location
