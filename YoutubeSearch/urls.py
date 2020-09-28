from django.contrib import admin
from django.urls import path
from .views import ListVideoView
from .tasks import fetch_data


urlpatterns = [
    path('get-data/', ListVideoView.as_view())
]
