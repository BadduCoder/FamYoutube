from rest_framework import generics
from .models import VideoData
from .serializers import VideoDataSerializer


class ListVideoView(generics.ListAPIView):

    serializer_class = VideoDataSerializer

    def get_queryset(self):
        """
        Returns list of all the youtube videos that match the search criteria
        """
        videos = VideoData.objects.all().order_by('-publishedAt')
        return videos  