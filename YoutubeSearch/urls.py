from django.contrib import admin
from django.urls import path
from .views import getData
from .tasks import fetch_data


urlpatterns = [
    path('get-data/', getData),
    path('put-data/', fetch_data),
]
