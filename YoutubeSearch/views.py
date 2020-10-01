from rest_framework import generics
from .models import VideoData
from .serializers import VideoDataSerializer
from .constants import DEFAULT_SORT_PROPERTY, SORT_PROPERTIES
from .customPagination import CustomCursorPagination


class ListVideoView(generics.ListAPIView):

    serializer_class = VideoDataSerializer
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        """
        Returns list of all the youtube videos that match the search criteria
        """

        videos = []

        # If query argument is provided
        if 'q' in self.request.GET:
            # Get the query provided by user
            query = self.request.GET.get('q')
            # Filter all records with title and description containing query
            videos = VideoData.objects.filter(title__icontains=query)    
        else:
            videos = VideoData.objects.all()
        
        # If sortby argument is provided
        if 'sortby' in self.request.GET:
            # Get the sortby query provided by user
            sort_by = self.request.GET.get('sortby')

            # Check if it is valid property by which we can sort
            if sort_by in SORT_PROPERTIES:
                videos = videos.order_by(sort_by)
                return videos
        
        # If invalid/no sortby argument provided, sort with default property
        videos = videos.order_by(DEFAULT_SORT_PROPERTY)

        return videos      