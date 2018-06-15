from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin', admin.site.urls),
    path('jwt-auth', obtain_jwt_token),  # 获取JWT Token API
    path('face-recognizing', include('face_recognizing.urls')),
    path('eye-tracking', include('eye_tracking.urls')),
]
