from . import eyeball_direction_detecting as eyeball_direction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image, ImageDraw
import face_recognition as fr
import math
import time
import cv2
import os


def store_video(request):
    """
    提取请求中的视频, url参数名为face_video
    :param request: 携带视频的请求
    :return: 返回提取视频后保存的路径
    """
    video = request.FILES.get('face_video')
    path = default_storage.save('static/videos/' + video.name, ContentFile(video.read()))
    os.path.join(settings.MEDIA_ROOT, path)
    print("receive video: " + video.name + " successfully")
