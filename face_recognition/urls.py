from django.conf.urls import url
from . import views

urlpatterns = [
    # url('cache/faces', views.read_from_cache, name="list"),
    # url('db/faces', views.read_from_db, name="db-list"),
    url('recognize-face', views.recognize_face, name="recognize-face")
]
