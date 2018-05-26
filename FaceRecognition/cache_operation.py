from django.core.cache import cache
import json


# read cache user id
def read_from_cache_by_unionId(unionId):
    data = cache.get("id:" + unionId)
    if data is not None:
        return json.loads(data)
    else:
        return False


def read_from_cache_all_faces():
    knownFacesList = cache.keys("*")
    faces = []
    for i in knownFacesList:
        faceEncoding = json.loads(cache.get(i))
        faces.append(faceEncoding)
    return faces
