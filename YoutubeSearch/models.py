from django.db import models
from .constants import thumbnail_choice


class VideoData(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    title = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField()
    publishedAt = models.CharField(max_length=20)
    channelTitle = models.CharField(max_length=128)

    def __str__(self):
        return f"({self.id}) {self.title}"


class Thumbnails(models.Model):
    video = models.ForeignKey(VideoData, related_name='thumbnails', on_delete=models.CASCADE)
    thumbnail_type = models.CharField(max_length=2, choices=thumbnail_choice)
    height = models.IntegerField()
    width = models.IntegerField()
    url = models.URLField()

    def __str__(self):
        return f"{self.video.title} ({self.thumbnail_type})"

