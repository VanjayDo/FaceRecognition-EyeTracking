from django.conf.urls import url

from . import views

urlpatterns = [
    url('eye-direction', views.eye_direction, name='eye-direction'),
]
