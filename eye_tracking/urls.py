from django.conf.urls import url

from . import views

urlpatterns = [
    url('get-eyeball-direction', views.get_eyeball_direction, name='get-eyeball-direction'),
    url('get-eyeball-track', views.get_eyeball_track, name='get-eyeball-track')
]
