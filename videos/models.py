from django.db import models


class RecordedVideo(models.Model):
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recorded Video {self.id}"
    
