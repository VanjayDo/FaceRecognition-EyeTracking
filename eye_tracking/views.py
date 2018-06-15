from . import eyeball_direction_detecting as eyeball_direction
from . import eyeball_movement_tracking as eyeball_movement
from rest_framework.decorators import api_view
from django.http import HttpResponse
import time


@api_view(["POST"])
def get_eyeball_direction(request):
    start = time.time()
    cv_img_array = eyeball_direction.store_image(request)
    if cv_img_array is not None:
        result = eyeball_direction.eyeball_direction(cv_img_array)
        if result is not None:
            print("left is : " + str(result[0]) + "  left percent is : " + str(result[1]) + "  right is : " + str(
                result[2]) + "  right percent is : " + str(result[3]))
            direction_result = eyeball_direction.judge_direction(result[0], result[1], result[2], result[3])
            print("处理总共消耗时间: " + str(time.time() - start))
            return HttpResponse('result is :' + eyeball_direction.result_direction(direction_result))
        else:
            return HttpResponse("no face detected")
    else:
        return HttpResponse("image store error")


@api_view(["POST"])
def get_eyeball_track(request):
    video = eyeball_movement.store_video(request)
