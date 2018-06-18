from face_recognizing.models import FaceCharacteristic
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.cache import cache
from django.conf import settings
import face_recognition as fr
import json
import os


def recognize(unknown_face_encodings):
    """
    识别脸部信息是否已经存在数据库
    :param unknown_face_encodings: face_recognition.face_encodings()的返回值(numpy.ndarray类型)
    :return: True/False
    """
    result = False
    try:
        data = read_all_from_db()
        results = fr.compare_faces(data["faces"], unknown_face_encodings)
        if True in results:
            index = results.index(True)
            result = data["unique_ids"][index]
        return result
    except Exception as e:
        print(e)


# def add_new_face(unknown_face_encodings):
def add_new_face(unique_id, unknown_face_encodings):
    """
    添加脸部信息
    :param unique_id: 唯一身份id
    :param unknown_face_encodings: face_recognition.face_encodings()的返回值(numpy.ndarray类型)
    """
    try:
        unknown_face_encodings = unknown_face_encodings.tolist()  # numpy.ndarray转list类型
        unknown_face_encodings = json.dumps(unknown_face_encodings)  # list转json
        new_face = FaceCharacteristic(unique_id=unique_id, characteristic_value=unknown_face_encodings)  # 赋值持久化
        new_face.save()
    except Exception as e:
        print(e)
        return False


def store_image(request):
    """
    保存请求中的图片
    :param request: 携带图片的请求
    :return: 保存后图片的地址
    """
    image = request.FILES.get('face_image')
    if 1024 < image.size < 20480000:
        path = default_storage.save('static/images/' + image.name, ContentFile(image.read()))
        os.path.join(settings.MEDIA_ROOT, path)
        print("receive img: " + image.name + " successfully")
        return path
    else:
        return None


def get_face_encodings(img_path):
    """
    得到图片中人脸的特征值
    :param img_path: 图片路径
    :return:face_recognition.face_encodings()返回值中的第一个数组
    """
    try:
        img = fr.load_image_file(img_path)
        face_encodings = fr.face_encodings(img)
        return face_encodings[0]  # 返回list中第一个数组
    except Exception as e:
        print(e)


# class FaceRecognitionViewSet(viewsets.ModelViewSet):
#     queryset = FaceCharacteristic.objects.all().order_by('-date_joined')
#     serializer_class = FaceCharacteristicSerializer


def read_from_cache_by_unique_id(unique_id):
    """
    根据unique_id从cache中读取信息
    :param unique_id:唯一身份id
    :return:cache中的指定unique_id的脸部信息
    """
    data = cache.get("unique_id:" + unique_id)
    if data is not None:
        return json.loads(data)
    else:
        return None


def read_all_from_cache():
    """
    从cache中读取所有脸部信息
    :return: cache中的所有脸部信息
    """
    known_faces_list = cache.keys("*")
    faces = []
    unique_ids = []
    for i in known_faces_list:
        unique_id = str(i).split(":1:unique_id:")[-1]
        unique_ids.append(unique_id)
        print(unique_id)
        print("直接读取的类型" + str(type(cache.get(i))))
        face_encodings = json.loads(cache.get(i))
        print("json.loads后的类型" + str(type(face_encodings)))
        faces.append(face_encodings)
    data = {"unique_ids": unique_ids, "faces": faces}
    return data


def read_all_from_db():
    """
    从数据库中读取所有的脸部信息
    :return: 数据库中所有的脸部信息
    """
    all_data = FaceCharacteristic.objects.all()
    faces = []
    unique_ids = []
    for face in all_data:
        unique_id = face.unique_id
        unique_ids.append(unique_id)
        face_encodings = json.loads(face.characteristic_value)
        faces.append(face_encodings)
    data = {"unique_ids": unique_ids, "faces": faces}
    return data
