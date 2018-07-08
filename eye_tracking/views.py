from . import eyeball_direction_detecting as eyeball_direction
from . import eyeball_movement_tracking as eyeball_movement
from rest_framework.decorators import api_view
from django.http import HttpResponse
import eye_game
import time
import json


@api_view(["POST"])
def get_eyeball_direction(request):
    start = time.time()
    cv_img_array = eyeball_direction.store_image(request)
    if cv_img_array is not None:
        try:
            result = eye_game.api.get_eyeball_direction(cv_img_array)
            print("处理总共消耗时间: " + str(time.time() - start))
            result = {"result": result}
            return HttpResponse(json.dumps(result), content_type="application/json")
        except Exception:
            pass
        return HttpResponse(json.dumps({"result": "no face detected"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"result": "image store error"}), content_type="application/json")


@api_view(["POST"])
def get_eyeball_track(request):
    video = eyeball_movement.store_video(request)
