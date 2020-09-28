from .models import VideoData, Thumbnails
from rest_framework import serializers


class ThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thumbnails
        fields = '__all__'


class VideoDataSerializer(serializers.ModelSerializer):

    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = VideoData
        fields = '__all__'
