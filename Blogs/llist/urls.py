from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.list_details),
    path('main', views.list_details),
]