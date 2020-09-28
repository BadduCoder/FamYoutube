from django.contrib import admin
from django.urls import path
from .views import ListVideoView


urlpatterns = [
    path('get-data/', ListVideoView.as_view())
]
