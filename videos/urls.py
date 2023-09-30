from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path("video/", views.ScreenRecorderAPIView.as_view(), name="video"),
]
