from django.conf.urls import url

from . import views

urlpatterns = [
    url('get-eye-direction', views.get_eye_direction, name='get-eye-direction'),
]
