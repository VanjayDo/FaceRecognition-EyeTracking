from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from FaceRecognition.models import FaceCharacteristic
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import face_recognition as fr
import os
import json
import FaceRecognition.cache_operation as cache_operation
from FaceRecognition.serializer import FaceCharacteristicSerializer


def readFromCacheByUnionId(unionid):
    data = cache_operation.read_from_cache_by_unionId(unionid)
    return data


def storeImg(request):
    image = request.FILES.get('faceImg')
    if 1024 < image.size < 20480000:
        path = default_storage.save('static/faceImg/' + image.name, ContentFile(image.read()))
        os.path.join(settings.MEDIA_ROOT, path)
        print("receive img: " + image.name + " successfully")
        return path
    else:
        return None


def getFaceEncoding(request):
    imgPath = storeImg(request)
    if imgPath is not None:
        img = fr.load_image_file(imgPath)
        faceEncoding = fr.face_encodings(img)
        return faceEncoding[0]  # 返回list中第一个数组
    else:
        return None


# 识别脸部信息是否已经存在数据库
def recognizeFace(unknownFaceEncoding):
    result = False
    try:
        faces = cache_operation.read_from_cache_all_faces()
        results = fr.compare_faces(faces, unknownFaceEncoding)
        # 如果没有, 是否还要在从数据库读?#############################################################
        if True in results:
            result = True
        return result
    except Exception as e:
        print(e)


# 添加脸部信息, unknownFaceEncoding为numpy.ndarray类型
# def addNewFace(unionid, faceEncoding):
def addNewFace(unknownFaceEncoding):
    try:
        unknownFaceEncoding = unknownFaceEncoding.tolist()  # numpy.ndarray转list类型
        unknownFaceEncoding = json.dumps(unknownFaceEncoding)  # list转json
        new = FaceCharacteristic(characteristic_value=unknownFaceEncoding)  # 赋值持久化
        new.save()
    except Exception as e:
        print(e)


# class FaceRecognitionViewSet(viewsets.ModelViewSet):
#     queryset = FaceCharacteristic.objects.all().order_by('-date_joined')
#     serializer_class = FaceCharacteristicSerializer

@api_view(["GET"])
def getCache(request):
    faces = cache_operation.read_from_cache_all_faces()
    return HttpResponse(faces)


@api_view(["POST"])
def UserExits(request):
    # unionid = request.GET["unionid"]
    imgFaceEncoding = getFaceEncoding(request)
    if imgFaceEncoding is not None:
        added = recognizeFace(imgFaceEncoding)
        print(added)
        if added is None:
            # 如果已经添加过,则应该找出其unionID
            # pass
            return HttpResponse("Added before")
        else:
            # 说明没有添加
            # data = readFromCacheByUnionId(unionid)
            # 应该判断该上传用户是否已经授权并进入数据库
            # if data is not False:
            # 说明该用户添加过
            # 返回不认识该图片中的脸
            # pass
            # else:
            # 添加用户和脸部信息
            # addNewFace(unionid, imgFaceEncoding)
            # imgFaceEncoding=imgFaceEncoding.tolist()
            # imgFaceEncoding=json.dumps(imgFaceEncoding)
            addNewFace(imgFaceEncoding)
            return HttpResponse("Added success")
    else:
        # 说明图中没有脸
        return "can not detect faces"

# class FaceRecognitionAPI(APIView):
#     def findById(self, pk):
#         try:
#             return FaceCharacteristic.objects.get(id__exact=pk)
#         except FaceCharacteristic.DoesNotExist as e:
#             return HttpResponse("no such id" + e)
#
#     def get(self, request, pk, format=None):
#         all = self.findById(pk)
#         return HttpResponse(all.characteristic_value)
