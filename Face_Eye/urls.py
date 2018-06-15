from django.urls import path
from django.contrib import admin
from rest_framework import routers
from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token
from FaceRecognition import views as FaceRecognitionViewsFunction

# from EyeTracking import views as EyeTrackingViewsFunction

# router = routers.DefaultRouter()  # 使用Rest_framework的router
# router.register(r'FaceRecognition_list', FaceRecognitionViewsFunction.getCache,base_name="FaceRecognition_list")  # 脸部识别
# router.register(r'EyeTracking', EyeTrackinagViewsFunction.EyeTrackingViewSet)  # 眼球运动追踪

urlpatterns = [
    # path("", include(router.urls)),
    path('admin', admin.site.urls),
    path('JwtAuth', obtain_jwt_token),  # 获取JWT Token API
    path('FaceRecognition', include('FaceRecognition.urls')),
    path('EyeTracking', include('EyeTracking.urls')),
]
