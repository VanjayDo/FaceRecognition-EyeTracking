from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# FaceRecognition_list = FaceRecognitionViewSet.as_view({
#     "get": 'getCache'
# })
#
# FaceRecognition_create = FaceRecognitionViewSet.as_view({
#     "post": 'UserExits'
# })

urlpatterns = [
    url('list', views.getCache),
    url('create', views.UserExits)
]
