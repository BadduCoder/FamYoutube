from django.db import models
from .constants import THUMBNAIL_CHOICES


class VideoData(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    title = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField()
    publishedAt = models.DateTimeField(blank=False, null=False, db_index=True)
    channelTitle = models.CharField(max_length=128)

    def __str__(self):
        return f"({self.id}) {self.title}"


class Thumbnails(models.Model):
    video = models.ForeignKey(VideoData, related_name='thumbnails', on_delete=models.CASCADE)
    thumbnail_type = models.CharField(max_length=2, choices=THUMBNAIL_CHOICES)
    height = models.IntegerField()
    width = models.IntegerField()
    url = models.URLField()

    class Meta:
        unique_together = ('video', 'thumbnail_type')

    def __str__(self):
        return f"{self.video.title} ({self.thumbnail_type})"

