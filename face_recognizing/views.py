from rest_framework.decorators import api_view
from face_recognizing.face_recognition import *
from django.http import HttpResponse


# @api_view(["GET"])
# def read_from_cache(request):
#     """
#     从cache中读取所有的脸部信息
#     :param request:http请求
#     :return: cache中所有的脸部信息
#     """
#     faces = read_all_from_cache()
#     return HttpResponse(faces)
#
#
# @api_view(["GET"])
# def read_from_db(request):
#     """
#     从数据库中读取所有的脸部信息
#     :param request:http请求
#     :return: 数据库中所有的脸部信息
#     """
#     faces = read_all_from_db()
#     return HttpResponse(faces)


@api_view(["POST"])
def recognize_face(request):
    """
    识别用户的脸部
    :param request: http请求
    :return: 识别结果
    """
    img_path = store_image(request)
    unique_id = request.POST.get("unique_id")
    img_face_encoding = get_face_encodings(img_path)
    if img_face_encoding is not None:
        user_id = recognize(img_face_encoding)
        if user_id is not False:
            # 如果已经添加过, 返回unique_id
            result = {"recognition-result": True, "user-id": user_id}
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            added_result = add_new_face(unique_id, img_face_encoding)
            if added_result is not False:
                added_result = True
            result = {"recognition-result": False, "add": added_result}
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        # 说明图中没有脸
        result = {"recognition-result": "can not detect faces"}
        return HttpResponse(json.dumps(result), content_type="application/json")
