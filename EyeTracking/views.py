from rest_framework.decorators import api_view
from django.http import HttpResponse
from .eye_direction_detecting import *


@api_view(["POST"])
def get_eye_direction(request):
    start = time.time()
    img_path = store_image(request)
    if img_path is not None:
        result = eye_direction(img_path)
        if result is not None:
            print("left is : " + str(result[0]) + "  left percent is : " + str(result[1]) + "  right is : " + str(
                result[2]) + "  right percent is : " + str(result[3]))
            direction_result = judge_direction(result[0], result[1], result[2], result[3])
            print("处理总共消耗时间: " + str(time.time() - start))
            return HttpResponse('result is :' + result_direction(direction_result))
        else:
            return HttpResponse("no face detected")
    else:
        return HttpResponse("image store error")
